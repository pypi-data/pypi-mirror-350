import lz4.frame
import pandas as pd
import os
import threading
import json
import requests
import lz4
import bson
import hashlib
import pymongo
import time

from SharedData.IO.MongoDBClient import MongoDBClient
from SharedData.IO.AWSKinesis import KinesisStreamProducer
from SharedData.Logger import Logger


class WorkerPool:

    """
    '''
    Manages a pool of worker jobs, supporting job creation, consumption, and status updates.
    
    This class facilitates job distribution and coordination either via a Kinesis stream or a REST API backed by shared data endpoints. It handles job queuing, sending, receiving, and status management with thread-safe operations.
    
    Attributes:
        kinesis (bool): Flag to determine if Kinesis stream is used.
        jobs (dict): Dictionary storing jobs keyed by target worker names.
        lock (threading.Lock): Lock to ensure thread-safe access to shared resources.
        stream_buffer (list): Buffer to hold streamed jobs.
        producer: Either a KinesisStreamProducer instance or self for REST API posting.
    
    Methods:
        acquire(): Acquire the internal thread lock.
        release(): Release the internal thread lock.
        produce(record, partitionkey=None): Send a job record to the worker pool endpoint or Kinesis stream.
        new_job(record): Add a new job record to the local job queue.
        consume(fetch_jobs=0): Fetch jobs from the shared endpoint and buffer them locally.
        get_jobs(workername): Retrieve and clean up jobs assigned to a specific worker.
        update_jobs_status(): Periodically update job statuses from NEW/WAITING to PENDING if due and dependencies are met.
    """
    def __init__(self, kinesis=False):
        """
        Initializes the object with optional Kinesis streaming support.
        
        Parameters:
            kinesis (bool): If True, initializes a KinesisStreamProducer using the
                            'WORKERPOOL_STREAM' environment variable. If False, checks
                            for 'SHAREDDATA_ENDPOINT' and 'SHAREDDATA_TOKEN' in the
                            environment variables and sets the producer to self.
        
        Attributes initialized:
            kinesis (bool): Flag indicating whether Kinesis streaming is enabled.
            jobs (dict): Dictionary to store job information.
            lock (threading.Lock): A lock to synchronize access to shared resources.
            stream_buffer (list): Buffer to hold stream data.
            producer: Either a KinesisStreamProducer instance or self, depending on kinesis.
        
        Raises:
            Exception: If kinesis is False and required environment variables are missing.
        """
        self.kinesis = kinesis
        self.jobs = {}
        self.lock = threading.Lock()
        self.stream_buffer = []

        if kinesis:
            self.producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])
        else:
            if not 'SHAREDDATA_ENDPOINT' in os.environ:
                raise Exception('SHAREDDATA_ENDPOINT not in environment variables')            

            if not 'SHAREDDATA_TOKEN' in os.environ:
                raise Exception('SHAREDDATA_TOKEN not in environment variables')            

            self.producer = self

    def acquire(self):
        """
        Acquire the lock associated with this object.
        
        This method blocks until the lock is successfully acquired.
        """
        self.lock.acquire()
    
    def release(self):
        """
        Releases the acquired lock.
        
        This method releases the lock held by the current thread, allowing other threads to acquire it. It should only be called when the lock is currently held.
        """
        self.lock.release()

    def produce(self, record, partitionkey=None):
        """
        Sends a compressed and encoded record to a remote server endpoint.
        
        The method validates that the record contains the required keys: 'sender', 'target', and 'job'. It then encodes the record using BSON, compresses it with LZ4, and sends it as a POST request to a predefined server endpoint with appropriate headers, including an authorization token retrieved from environment variables. The method uses locking mechanisms to ensure thread safety during the send operation. If the request fails or required keys are missing, an exception is raised or an error message is printed.
        
        Args:
            record (dict): The data record to be sent. Must contain 'sender', 'target', and 'job' keys.
            partitionkey (optional): Not used in this implementation.
        
        Raises:
            Exception: If 'sender', 'target', or 'job' keys are missing in the record.
        """
        if not 'sender' in record:
            raise Exception('sender not in record')
        if not 'target' in record:
            raise Exception('target not in record')
        if not 'job' in record:
            raise Exception('job not in record')
        try:            
            self.acquire()
            bson_data = bson.encode(record)
            compressed = lz4.frame.compress(bson_data)
            headers = {
                'Content-Type': 'application/octet-stream',
                'Content-Encoding': 'lz4',
                'X-Custom-Authorization': os.environ['SHAREDDATA_TOKEN'],
            }
            response = requests.post(
                os.environ['SHAREDDATA_ENDPOINT']+'/api/workerpool',
                headers=headers,
                data=compressed,
                timeout=15
            )
            response.raise_for_status()
        except Exception as e:
            # self.handleError(record)
            print(f"Could not send command to server:{record}\n {e}")
        finally:            
            self.release()

    def new_job(self, record):
        """
        Add a new job record to the job queue for a specified target.
        
        Parameters:
            record (dict): A dictionary containing job details. Must include the keys 'sender', 'target', and 'job'.
                           Optionally, it can include a 'date' key; if absent, the current UTC timestamp is added.
        
        Raises:
            Exception: If 'sender', 'target', or 'job' keys are missing from the record.
        
        Returns:
            bool: True if the job was successfully added to the queue.
        
        This method ensures thread-safe addition of jobs by acquiring and releasing a lock during the update.
        """
        if not 'sender' in record:
            raise Exception('sender not in record')
        if not 'target' in record:
            raise Exception('target not in record')
        if not 'job' in record:
            raise Exception('job not in record')
        
        targetkey = str(record['target']).upper()
        if not targetkey in self.jobs.keys():
            self.jobs[targetkey] = []

        if not 'date' in record:
            record['date'] = pd.Timestamp.utcnow().tz_localize(None)
        try:
            self.acquire()
            self.jobs[targetkey].append(record)
        except Exception as e:
            Logger.log.error(f"Could not add job to workerpool:{record}\n {e}")
        finally:
            self.release()
        
        return True
    
    def consume(self, fetch_jobs=0):
        """
        Consumes jobs from a remote worker pool API and appends them to the internal stream buffer.
        
        Attempts to acquire a lock before making a GET request to the worker pool endpoint, using
        environment variables for authentication and configuration. Optionally fetches a specified
        number of jobs if `fetch_jobs` is greater than zero. The response content is expected to be
        LZ4 compressed BSON data, which is decompressed and decoded before extending the internal
        `stream_buffer` with the retrieved jobs.
        
        Returns:
            bool: True if the request was successful and jobs were processed or no content was returned,
                  False otherwise.
        
        Parameters:
            fetch_jobs (int): Optional number of jobs to fetch from the worker pool. Defaults to 0.
        """
        success = False
        try:
            self.acquire()
            workername = os.environ['USER_COMPUTER']
            headers = {                
                'Accept-Encoding': 'lz4',                
                'X-Custom-Authorization': os.environ['SHAREDDATA_TOKEN'],
            }
            params = {
                'workername': workername,                
            }
            if fetch_jobs > 0:
                params['fetch_jobs'] = fetch_jobs
            response = requests.get(
                os.environ['SHAREDDATA_ENDPOINT']+'/api/workerpool',
                headers=headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            success = True
            if response.status_code == 204:
                return success
            response_data = lz4.frame.decompress(response.content)
            record = bson.decode(response_data)            
            self.stream_buffer.extend(record['jobs'])            
        except Exception as e:
            Logger.log.error(f"Could not consume workerpool:{e}")            
        finally:
            self.release()
        return success
    
    def get_jobs(self, workername):
        """
        Retrieve and return the list of current jobs assigned to a specific worker.
        
        This method performs the following steps:
        - Acquires a lock to ensure thread-safe access to the jobs data structure.
        - Converts the provided worker name to uppercase.
        - Cleans up and removes any broadcast jobs older than 60 seconds for the specified worker and for the 'ALL' broadcast queue.
        - Collects all valid jobs assigned directly to the worker.
        - Collects broadcast jobs from the 'ALL' queue that the worker has not yet acknowledged, marking them as acknowledged with a timestamp.
        - Releases the lock after processing.
        - Returns a list of jobs currently assigned or broadcast to the worker.
        
        Parameters:
            workername (str): The name of the worker to retrieve jobs for.
        
        Returns:
            list: A list of job dictionaries assigned or broadcast to the specified worker.
        """
        try:
            self.acquire()
            tnow = pd.Timestamp.utcnow().tz_localize(None)
            _jobs = []
            workername = str(workername).upper()
            if workername in self.jobs.keys():
                # Clean up broadcast jobs older than 60 seconds
                self.jobs[workername] = [
                    job for job in self.jobs[workername]
                    if 'date' in job and tnow - pd.Timestamp(job['date']) < pd.Timedelta(seconds=60)
                ]
                for job in self.jobs[workername]:                    
                    _jobs.append(job)
                
                # Clear the jobs for this worker
                self.jobs[workername] = []
                        
            
            if 'ALL' in self.jobs.keys():
                # Clean up broadcast jobs older than 60 seconds
                self.jobs['ALL'] = [
                    job for job in self.jobs['ALL']
                    if 'date' in job and tnow - pd.Timestamp(job['date']) < pd.Timedelta(seconds=60)
                ]
                for job in self.jobs['ALL']:                    
                    if not 'workers' in job.keys():
                        job['workers'] = {}
                    if not workername in job['workers'].keys():
                        job['workers'][workername] = pd.Timestamp.utcnow().tz_localize(None)
                        _jobs.append(job)                
        except Exception as e:
            Logger.log.error(f"Could not get jobs from workerpool:{e}")
        finally:
            self.release()
        return _jobs
                
    @staticmethod
    def update_jobs_status() -> None:
        """
        Periodically updates job statuses in the MongoDB collection from 'NEW' or 'WAITING' to 'PENDING' if the job's due date has passed and all its dependencies have been completed.
        
        This method runs indefinitely, performing the update every 5 seconds. If an error occurs during the update process, it logs the error and waits 60 seconds before retrying.
        
        The update is performed using a MongoDB aggregation pipeline that:
        - Filters jobs with status 'NEW' or 'WAITING' and a due date earlier than the current time.
        - Looks up the job dependencies and checks if all dependencies have status 'COMPLETED'.
        - Updates the status of eligible jobs to 'PENDING' and sets the modification time to the current timestamp.
        """
        while True:
            try:
                now = pd.Timestamp('now', tz='UTC')
                pipeline = [
                    {
                        '$match': {
                            'status': {'$in': ['NEW', 'WAITING']},
                            'date': {'$lt': now}
                        }
                    },
                    {
                        '$lookup': {
                            'from': 'Text/RT/WORKERPOOL/collection/JOBS',
                            'localField': 'dependencies',
                            'foreignField': 'hash',
                            'as': 'deps'
                        }
                    },
                    {
                        '$addFields': {
                            'all_deps_completed': {
                                '$cond': [
                                    {'$gt': [{'$size': {'$ifNull': ['$dependencies', []]}}, 0]},
                                    {
                                        '$allElementsTrue': {
                                            '$map': {
                                                'input': "$deps",
                                                'as': "d",
                                                'in': {'$eq': ["$$d.status", "COMPLETED"]}
                                            }
                                        }
                                    },
                                    True
                                ]
                            }
                        }
                    },
                    {
                        '$match': {'all_deps_completed': True}
                    },
                    {
                        "$project": {"date": 1, "hash": 1}
                    }
                ]
                pipeline.append({
                    "$merge": {
                        "into": "Text/RT/WORKERPOOL/collection/JOBS",
                        "whenMatched": [
                            {"$set": {"status": "PENDING", "mtime": now}}
                        ],
                        "whenNotMatched": "discard"
                    }
                })

                mongodb = MongoDBClient(user='master')
                coll = mongodb['Text/RT/WORKERPOOL/collection/JOBS']
                coll.aggregate(pipeline)

                time.sleep(5)
            except Exception as e:
                Logger.log.error(f"Error in update_jobs_status: {e}")
                time.sleep(60)  # Wait before retrying in case of error
        
    @staticmethod
    def fetch_job(workername, njobs=1):
        """
        Fetches and atomically reserves a specified number of pending jobs from a MongoDB collection for a given worker.
        
        Parameters:
            workername (str): The worker identifier in the format 'user@computer'.
            njobs (int, optional): The number of jobs to fetch. Defaults to 1.
        
        Returns:
            list: A list of job documents that have been fetched and marked as 'FETCHED' for the specified worker.
        
        The method filters jobs by matching the user and computer fields (or 'ANY'), and only considers jobs with status 'PENDING'.
        Each fetched job's status is updated to 'FETCHED', the target is set to the worker, and the modification time is updated to the current UTC timestamp.
        Jobs are fetched in descending order by their 'date' field.
        """
        user = workername.split('@')[0]
        computer = workername.split('@')[1]
        mongodb= MongoDBClient(user='master')
        coll = mongodb['Text/RT/WORKERPOOL/collection/JOBS']

        filter_query = {
            'user': {'$in': [user, 'ANY']},
            'computer': {'$in': [computer, 'ANY']},
            'status': 'PENDING'  # Only fetch jobs that are in 'PENDING' status
        }

        # Define the update operation to set status to 'FETCHED'
        update_query = {
            '$set': {
                'status': 'FETCHED',
                'target': user+'@'+computer,
                'mtime': pd.Timestamp('now', tz='UTC')
            }
        }

        sort_order = [('date', pymongo.DESCENDING)]

        fetched_jobs = []
        for _ in range(njobs):
            # Atomically find and update a single job
            job = coll.find_one_and_update(
                filter=filter_query,
                update=update_query,
                sort=sort_order,
                return_document=pymongo.ReturnDocument.AFTER
            )

            if job:
                fetched_jobs.append(job)
            else:
                # No more jobs available
                break
        
        return fetched_jobs