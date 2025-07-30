import json
import bson
from bson import json_util
from bson.objectid import ObjectId
import requests
import os
import pandas as pd
import numpy as np
import time
import lz4.frame
import lz4.frame as lz4f
import math
import datetime
import os
import logging
import threading


from SharedData.IO.SyncTable import SyncTable
from SharedData.Logger import Logger
from SharedData.Database import *


class ClientAPI:

    """
    '''
    ClientAPI provides a comprehensive interface for interacting with a remote data service via HTTP API calls. It supports operations for retrieving, publishing, subscribing, and patching tabular and collection-based data, with built-in handling for compression, pagination, and data serialization.
    
    Key functionalities include:
    - raise_for_status: Raises exceptions for HTTP client and server errors with detailed messages.
    - table_subscribe_thread: Continuously subscribes to updates on a specified table, decompressing and merging incoming data.
    - table_publish_thread: Continuously publishes local table updates to the remote API, respecting bandwidth and rate limits.
    - records2df / df2records: Convert between numpy structured arrays and pandas DataFrames, handling encoding and datetime conversions.
    - get_table / post_table: Retrieve and post tabular data with support for pagination, compression, and metadata handling.
    - serialize / is_empty: Recursively serialize Python objects to JSON-compatible structures, omitting empty or sentinel values.
    - flatten_dict / unflatten_dict: Utilities to flatten nested dictionaries into single-level dicts with compound keys and vice versa.
    - documents2df / df2documents: Convert between lists of documents (dicts) and pandas DataFrames, with optional flattening and empty field removal.
    - get_collection / post_collection / patch
    """
    @staticmethod
    def raise_for_status(response):
        
        """
        Checks the HTTP response status code and raises an exception for client or server errors.
        
        If the response status code indicates a client error (4xx) or a server error (5xx),
        this method extracts the error message from the response JSON (using the "message" key if available,
        otherwise falling back to the response reason) and raises an Exception with a detailed error message
        including the status code, error reason, and the URL of the request.
        
        Parameters:
            response (requests.Response): The HTTP response object to check.
        
        Raises:
            Exception: If the response status code is in the 4xx or 5xx range, with a message describing the error.
        """
        if 400 <= response.status_code < 500:
            reason = response.json().get("message", response.reason)
            http_error_msg = (
                f"{response.status_code} Client Error: {reason} for url: {response.url}"
            )
            raise Exception(http_error_msg)
        
        elif 500 <= response.status_code < 600:
            reason = response.json().get("message", response.reason)
            http_error_msg = (
                f"{response.status_code} Server Error: {reason} for url: {response.url}"
            )
            raise Exception(http_error_msg)
        else:
            return

    @staticmethod
    def table_subscribe_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False,
            bandwidth=1e6, protocol='http'):

        """
        '''
        Subscribe to a data table and continuously fetch updates from a remote API endpoint.
        
        This static method establishes a subscription to a specified table on a remote server,
        retrieving historical data based on lookback parameters and then continuously polling
        for new records. Data is fetched in compressed form, decompressed, and integrated into
        the local table's records, either by upserting or extending depending on the table's index.
        
        Parameters:
            table (object): The table object containing metadata and records to update.
            host (str): The hostname or IP address of the API server.
            port (int): The port number of the API server.
            lookbacklines (int, optional): Number of past records to retrieve initially. Default is 1000.
            lookbackdate (str or datetime, optional): Specific date to start lookback from. Overrides lookbacklines if provided.
            snapshot (bool, optional): Whether to request a snapshot of the current data state. Default is False.
            bandwidth (float, optional): Bandwidth limit parameter for the API request. Default is 1e6.
            protocol (str, optional): Protocol to use for the API request ('http' or 'https'). Default is 'http'.
        
        Behavior:
            - Constructs the API URL based
        """
        apiurl = f"{protocol}://{host}:{port}"
        
        records = table.records
        
        params = {                    
            'token': os.environ['SHAREDDATA_TOKEN'],            
        }

        tablename = table.tablename
        tablesubfolder = None
        if '/' in table.tablename:
            tablename = table.tablename.split('/')[0]
            tablesubfolder = table.tablename.split('/')[1] 

        url = apiurl+f"/api/subscribe/{table.database}/{table.period}/{table.source}/{tablename}"
        
        lookbackid = records.count - lookbacklines
        if tablesubfolder:
            params['tablesubfolder'] = tablesubfolder        
        if lookbacklines:
            params['lookbacklines'] = lookbacklines
        if lookbackdate:
            params['lookbackdate'] = lookbackdate
            lookbackdate = pd.Timestamp(lookbackdate)            
            loc = records.get_date_loc_gte(lookbackdate)
            if len(loc)>0:
                lookbackid = min(loc)
        if bandwidth:
            params['bandwidth'] = bandwidth
                
        hasindex = records.table.hasindex           
        lastmtime = pd.Timestamp('1970-01-01')
        if hasindex:
            lastmtime = np.max(records[lookbackid:]['mtime'])
            lastmtime = pd.Timestamp(np.datetime64(lastmtime))
        while True:
            try:
                params['page'] = 1
                if hasindex:
                    params['mtime'] = lastmtime
                params['count'] = records.count
                params['snapshot'] = snapshot
                snapshot = False

                response = requests.get(url, params=params)
                if response.status_code != 200:
                    if response.status_code == 204:
                        time.sleep(1)
                        continue
                    else:
                        raise Exception(response.status_code, response.text)
                
                data = lz4.frame.decompress(response.content)
                buffer = bytearray()
                buffer.extend(data)
                if len(buffer) >= records.itemsize:
                    # Determine how many complete records are in the buffer
                    num_records = len(buffer) // records.itemsize
                    # Take the first num_records worth of bytes
                    record_data = buffer[:num_records *
                                                records.itemsize]
                    # And remove them from the buffer
                    del buffer[:num_records *
                                        records.itemsize]
                    # Convert the bytes to a NumPy array of records
                    rec = np.frombuffer(
                        record_data, dtype=records.dtype)
                    if hasindex:
                        recmtime = pd.Timestamp(np.max(rec['mtime']))
                        if recmtime > lastmtime:
                            lastmtime = recmtime
                        
                    if records.table.hasindex:
                        # Upsert all records at once
                        records.upsert(rec)
                    else:
                        # Extend all records at once
                        records.extend(rec)

                pages = int(response.headers['Content-Pages'])
                if pages > 1:
                    # paginated response
                    for i in range(2, pages+1):
                        params['page'] = i                        
                        response = requests.get(url, params=params)
                        if response.status_code != 200:
                            raise Exception(response.status_code, response.text)
                        data = lz4.frame.decompress(response.content)
                        buffer = bytearray()
                        buffer.extend(data)
                        if len(buffer) >= records.itemsize:
                            # Determine how many complete records are in the buffer
                            num_records = len(buffer) // records.itemsize
                            # Take the first num_records worth of bytes
                            record_data = buffer[:num_records *
                                                        records.itemsize]
                            # And remove them from the buffer
                            del buffer[:num_records *
                                                records.itemsize]
                            # Convert the bytes to a NumPy array of records
                            rec = np.frombuffer(
                                record_data, dtype=records.dtype)
                            if hasindex:
                                recmtime = pd.Timestamp(np.max(rec['mtime']))
                                if recmtime > lastmtime:
                                    lastmtime = recmtime
                                
                            if records.table.hasindex:
                                # Upsert all records at once
                                records.upsert(rec)
                            else:
                                # Extend all records at once
                                records.extend(rec)
                        time.sleep(0.5)

                time.sleep(1)

            except Exception as e:
                msg = 'Retrying API subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)


    @staticmethod
    def table_publish_thread(table, host, port, lookbacklines, 
        lookbackdate, snapshot,bandwidth, protocol='http', max_requests_per_minute=100):

        """
        '''
        Continuously publishes data from a given table to a remote server via HTTP(S) API.
        
        This static method repeatedly checks for new records in the specified table and uploads them
        to a remote endpoint, handling rate limiting, compression, and retries on failure.
        
        Parameters:
            table (object): The table object containing records and metadata to publish.
            host (str): The hostname or IP address of the remote server.
            port (int or None): The port number of the remote server; if None, default protocol port is used.
            lookbacklines (int or None): Number of previous lines to include in the publish request.
            lookbackdate (str or pandas.Timestamp or None): Date string or timestamp to look back from.
            snapshot (bool): Flag indicating whether to publish a snapshot of the table.
            bandwidth (float or None): Maximum bandwidth in bytes per second for data transfer.
            protocol (str): Protocol to use for the connection ('http' or 'https'). Default is 'http'.
            max_requests_per_minute (int): Maximum number of API requests allowed per minute. Default is 100.
        
        Behavior:
            - Constructs the API URL based on the host, port, and protocol.
            - Retrieves remote table metadata (modification time and
        """
        if port is None:
            apiurl = f"{protocol}://{host}"
        else:
            apiurl = f"{protocol}://{host}:{port}"
        
        while True:
            try:
                records = table.records
                
                params = {                    
                    'token': os.environ['SHAREDDATA_TOKEN'],            
                }

                tablename = table.tablename
                tablesubfolder = None
                if '/' in table.tablename:
                    tablename = table.tablename.split('/')[0]
                    tablesubfolder = table.tablename.split('/')[1] 

                url = apiurl+f"/api/publish/{table.database}/{table.period}/{table.source}/{tablename}"
                                
                if tablesubfolder:
                    params['tablesubfolder'] = tablesubfolder        
                if lookbacklines:
                    params['lookbacklines'] = lookbacklines
                if lookbackdate:
                    params['lookbackdate'] = lookbackdate
                    lookbackdate = pd.Timestamp(lookbackdate)            
                if bandwidth:
                    params['bandwidth'] = bandwidth
                
                
                # ask for the remote table mtime and count

                response = requests.get(url, params=params)

                if response.status_code != 200:
                    raise Exception(response.status_code, response.text)

                response = response.json()
                remotemtime = None
                if 'mtime' in response:
                    remotemtime = pd.Timestamp(response['mtime']).replace(tzinfo=None)
                remotecount = response['count']

                client = {}
                client.update(params)
                if 'mtime' in response:
                    client['mtime'] = remotemtime.timestamp()
                client['count'] = remotecount
                client = SyncTable.init_client(client,table)

                while True:
                    try:
                        time.sleep(60/max_requests_per_minute)
                        
                        client, ids2send = SyncTable.get_ids2send(client)
                        if len(ids2send) == 0:
                            time.sleep(0.001)                            
                        else:
                            rows2send = len(ids2send)
                            sentrows = 0
                            msgsize = min(client['maxrows'], rows2send)
                            bandwidth = client['bandwidth']
                            tini = time.time_ns()
                            bytessent = 0
                            while sentrows < rows2send:
                                t = time.time_ns()
                                message = records[ids2send[sentrows:sentrows +
                                                        msgsize]].tobytes()
                                compressed = lz4f.compress(message)
                                msgbytes = len(compressed)
                                bytessent+=msgbytes                        
                                msgmintime = msgbytes/bandwidth                        
                                
                                # create a post request
                                response = requests.post(url, params=params, data=compressed)
                                if response.status_code != 200:
                                    raise Exception('Failed to publish data remote!=200 !')

                                sentrows += msgsize
                                msgtime = (time.time_ns()-t)*1e-9
                                ratelimtime = max(msgmintime-msgtime, 0)
                                if ratelimtime > 0:
                                    time.sleep(ratelimtime)

                            totalsize = (sentrows*records.itemsize)/1e6
                            totaltime = (time.time_ns()-tini)*1e-9
                            if totaltime > 0:
                                transfer_rate = totalsize/totaltime
                            else:
                                transfer_rate = 0
                            client['transfer_rate'] = transfer_rate
                            client['upload'] += msgbytes
                        
                    except:
                        break

            except Exception as e:
                msg = 'Retrying API publish %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                        table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)

    @staticmethod
    def records2df(records, pkey):
        """
        Convert a list of record dictionaries into a pandas DataFrame with a specified primary key index.
        
        Parameters:
            records (list of dict): List of records where each record is a dictionary representing a row.
            pkey (str or list): Column name(s) to set as the DataFrame index.
        
        Returns:
            pandas.DataFrame: DataFrame constructed from the records with the specified index set.
            Object and byte string columns are decoded to UTF-8 strings where possible.
        """
        df = pd.DataFrame(records, copy=False)
        dtypes = df.dtypes.reset_index()
        dtypes.columns = ['tag', 'dtype']
        # convert object to string
        string_idx = pd.Index(['|S' in str(dt) for dt in dtypes['dtype']])
        string_idx = (string_idx) | pd.Index(dtypes['dtype'] == 'object')
        tags_obj = dtypes['tag'][string_idx].values
        for tag in tags_obj:
            try:
                df[tag] = df[tag].str.decode(encoding='utf-8', errors='ignore')
            except:
                pass
        df = df.set_index(pkey)
        return df
    
    @staticmethod
    def df2records(df, pkeycolumns, recdtype=None):
        """
        Convert a pandas DataFrame into a numpy structured array (records) with optional custom record dtype.
        
        Parameters:
            df (pandas.DataFrame): The input DataFrame to convert.
            pkeycolumns (list of str): List of column names that must match the DataFrame's index names in order.
            recdtype (numpy.dtype or None): Optional numpy dtype for the output structured array. If None, dtype is inferred.
        
        Returns:
            numpy.ndarray: A numpy structured array representing the DataFrame records.
        
        Raises:
            Exception: If the DataFrame's index names do not match pkeycolumns.
            Exception: If conversion to binary format fails due to unsupported object types.
        
        Details:
        - Validates that the DataFrame's index names match the provided primary key columns.
        - Resets the DataFrame index before conversion.
        - Converts timezone-aware datetime columns to UTC naive datetime.
        - Converts object columns to UTF-8 encoded byte strings when recdtype is None.
        - When recdtype is provided, attempts to cast columns to the specified dtype, filling NaNs in integer columns with zero.
        - Logs errors encountered during type conversions but continues processing other columns.
        """
        check_pkey = True
        if len(pkeycolumns) == len(df.index.names):
            for k in range(len(pkeycolumns)):
                check_pkey = (check_pkey) & (
                    df.index.names[k] == pkeycolumns[k])
        else:
            check_pkey = False
        if not check_pkey:
            raise Exception('First columns must be %s!' % (pkeycolumns))
        
        if recdtype is None:
            df = df.reset_index()
            dtypes = df.dtypes.reset_index()
            dtypes.columns = ['tag', 'dtype']
        
            # Convert datetime columns with timezone to UTC naive datetime
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    if df[col].dt.tz is not None:
                        df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
            
            # convert object to string
            tags_obj = dtypes['tag'][dtypes['dtype'] == 'object'].values
            for tag in tags_obj:
                try:
                    df[tag] = df[tag].astype(str)
                    df[tag] = df[tag].str.encode(encoding='utf-8', errors='ignore')
                except Exception as e:
                    Logger.log.error(f'df2records(): Could not convert {tag} : {e}!')
                df[tag] = df[tag].astype('|S')
                
            rec = np.ascontiguousarray(df.to_records(index=False))
            type_descriptors = [field[1] for field in rec]
            if '|O' in type_descriptors:
                errmsg = 'df2records(): Could not convert type to binary'
                Logger.log.error(errmsg)
                raise Exception(errmsg)
                    
            return rec
        else:
            df = df.reset_index()
            # Convert datetime columns with timezone to UTC naive datetime
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    if df[col].dt.tz is not None:
                        df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
            
            dtypes = recdtype
            
            rec = np.full((df.shape[0],), fill_value=np.nan, dtype=dtypes)
            for col in dtypes.names:
                try:
                    if col in df.columns:
                        if pd.api.types.is_integer_dtype(dtypes[col])\
                            or pd.api.types.is_unsigned_integer_dtype(dtypes[col]):
                            df[col] = df[col].fillna(0)
                            
                        rec[col] = df[col].astype(dtypes[col])
                        
                except Exception as e:
                    Logger.log.error('df2records(): Could not convert %s!\n%s' % (col, e))

            return rec

    @staticmethod
    def get_table(database, period, source, tablename, 
            endpoint=None,
            startdate=None, enddate=None, 
            symbols=None, portfolios=None, tags=None, query=None,
            columns=None, output_dataframe=True,
            page=None, per_page=None, load_all_pages=False,
            token=None, user=None):
            
        """
        '''
        Fetches tabular data from a specified API endpoint, supporting pagination, filtering, and output formatting.
        
        Parameters:
            database (str): The database name to query.
            period (str): The period or timeframe for the data.
            source (str): The data source identifier.
            tablename (str): The name of the table to retrieve, optionally including a subfolder separated by '/'.
            endpoint (str, optional): Custom API endpoint URL. Defaults to environment variable 'SHAREDDATA_ENDPOINT' if not provided.
            startdate (str, optional): Filter data starting from this date (inclusive).
            enddate (str, optional): Filter data up to this date (inclusive).
            symbols (list or str, optional): Filter by one or more symbols.
            portfolios (list or str, optional): Filter by one or more portfolios.
            tags (list or str, optional): Filter by one or more tags.
            query (dict, optional): Additional query parameters as a dictionary, serialized to JSON.
            columns (list or str, optional): Specific columns to retrieve.
            output_dataframe (bool, optional): If True, returns a pandas DataFrame; otherwise returns a numpy structured array. Defaults to True.
            page (int, optional):
        """
        url = os.environ['SHAREDDATA_ENDPOINT'] if not endpoint else endpoint

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/table/{database}/{period}/{source}/{tablename}'
        url += route
        
        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if startdate:
            params['startdate'] = startdate
        if enddate:
            params['enddate'] = enddate
        if symbols:
            params['symbols'] = symbols
        if portfolios:
            params['portfolios'] = portfolios
        if tags:
            params['tags'] = tags
        if user:
            params['user'] = user
        if query:
            params['query'] = json.dumps(query)
        if per_page:
            params['per_page'] = per_page
        if page:
            params['page'] = page
        if columns:
            params['columns'] = columns
        
        params['format'] = 'bin'

        # Make the GET request
        # Request LZ4-encoded response
        headers = {
            'Accept-Encoding': 'lz4'
        }

        if load_all_pages:
            # Start with page 1 to get total pages from headers
            params['page'] = 1
            response = requests.get(url, params=params, headers=headers)
            ClientAPI.raise_for_status(response)
            

            if response.status_code == 204:
                return pd.DataFrame([])

            # Get total pages from headers
            total_pages = int(response.headers.get('Content-Pages', 1))
            
            # Process first page
            names = json.loads(response.headers.get('Meta-Field-Names'))
            formats = json.loads(response.headers.get('Meta-Field-Formats'))
            pkey = json.loads(response.headers.get('Meta-Field-Pkey'))
            dtype = np.dtype(list(zip(names, formats)))
            decompressed = lz4f.decompress(response.content)
            all_recs = np.frombuffer(decompressed, dtype=dtype)

            # Fetch remaining pages if there are more
            for current_page in range(2, total_pages + 1):
                params['page'] = current_page
                response = requests.get(url, params=params, headers=headers)
                ClientAPI.raise_for_status(response)
                
                if response.status_code != 204:
                    decompressed = lz4f.decompress(response.content)
                    page_recs = np.frombuffer(decompressed, dtype=dtype)
                    all_recs = np.concatenate((all_recs, page_recs))

            if not output_dataframe:
                return all_recs
                    
            # Convert combined records to DataFrame
            df = ClientAPI.records2df(all_recs, pkey)            
            return df.sort_index()
        else:
            # Original single page request logic
            response = requests.get(url, params=params, headers=headers)
            ClientAPI.raise_for_status(response)

            if response.status_code == 204: 
                return pd.DataFrame([])
            
            # Read field metadata from headers
            names = json.loads(response.headers.get('Meta-Field-Names'))
            formats = json.loads(response.headers.get('Meta-Field-Formats'))
            pkey = json.loads(response.headers.get('Meta-Field-Pkey'))

            # Rebuild dtype
            dtype = np.dtype(list(zip(names, formats)))

            # Decompress LZ4 payload
            decompressed = lz4f.decompress(response.content)

            # Reconstruct numpy structured array
            recs = np.frombuffer(decompressed, dtype=dtype)
            if not output_dataframe:
                return recs
                    
            # Convert to DataFrame
            df = ClientAPI.records2df(recs, pkey)
            return df.sort_index()

    @staticmethod
    def post_table(database, period, source, tablename, 
            endpoint=None, 
            names = None, formats=None, size=None,
            value=None, overwrite=False,
            token=None, user=None):
            
        """
        '''
        Post data to a specified table in a remote database via an HTTP POST request.
        
        Parameters:
            database (str): The target database name.
            period (str): The period identifier for the data.
            source (str): The data source identifier.
            tablename (str): The target table name, optionally including a subfolder separated by '/'.
            endpoint (str, optional): The base URL endpoint for the API. Defaults to the environment variable 'SHAREDDATA_ENDPOINT'.
            names (list of str, optional): List of field names for the data schema.
            formats (list of str, optional): List of data formats corresponding to the field names.
            size (int, optional): Size parameter for the data.
            value (pandas.DataFrame or numpy.ndarray, optional): The data to post. If a DataFrame is provided, it is converted to a structured array.
            overwrite (bool, optional): Whether to overwrite existing data. Defaults to False.
            token (str, optional): Authentication token. If not provided, fetched from environment variable 'SHAREDDATA_TOKEN'.
            user (str, optional): User identifier for the request.
        
        Returns:
            int: HTTP status code of the POST request response.
        
        Raises:
            Exception: If
        """
        url = os.environ['SHAREDDATA_ENDPOINT'] if not endpoint else endpoint

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/table/{database}/{period}/{source}/{tablename}'
        url += route
        
        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')
        
        if user:
            params['user'] = user
        if names:
            params['names'] = json.dumps(names)
        if formats:
            params['formats'] = json.dumps(formats)
        if size:
            params['size'] = int(size)
        if overwrite:
            params['overwrite'] = overwrite
        
        if not value is None:
            if isinstance(value, pd.DataFrame):
                if names and formats:
                    hdrdtype = np.dtype({'names': names, 'formats': formats})
                    value = ClientAPI.df2records(value,DATABASE_PKEYS[database],recdtype=hdrdtype)
                else:
                    value = ClientAPI.df2records(value,DATABASE_PKEYS[database])
            elif isinstance(value, np.ndarray):
                pass
            else:
                raise Exception('value must be a pandas DataFrame')
                        
            meta_names = list(value.dtype.names)
            meta_formats = [value.dtype.fields[name][0].str for name in meta_names]
            compressed = lz4f.compress(value.tobytes())
            responsebytes = len(compressed)
            
            headers = {}
            headers['Content-Encoding'] = 'lz4'
            headers['Content-Length'] = json.dumps(responsebytes)
            headers['Meta-Field-Names'] = json.dumps(meta_names)
            headers['Meta-Field-Formats'] = json.dumps(meta_formats)
            headers['Meta-Field-Pkey'] = json.dumps(DATABASE_PKEYS[database])

            # Make the POST request
            response = requests.post(
                url,
                params=params,
                data=compressed,
                headers=headers
            )
        else:
            response = requests.post(url, params=params)

        ClientAPI.raise_for_status(response)
        
        return response.status_code
    

    @staticmethod
    def serialize(obj, iso_dates=False):
        """
        Recursively serialize a Python object into nested dictionaries and lists,
        omitting values considered "empty" as defined by the is_empty() method.
        
        Supports special handling for pandas Timestamps, datetime objects, dictionaries,
        pandas DataFrames, lists, tuples, sets, objects with __dict__, and ObjectId instances.
        
        Parameters:
            obj (any): The Python object to serialize.
            iso_dates (bool): If True, convert datetime and Timestamp objects to ISO 8601 strings.
        
        Returns:
            dict, list, str, or None: A serialized representation of the input object with empty values removed,
            or None if the object or its contents are empty.
        """

        # 1) Special-case Timestamps so they don't get recursed:
        if isinstance(obj, pd.Timestamp):
            # Return None if it's considered 'empty' (e.g. NaT),
            # otherwise treat it as a scalar (string, raw Timestamps, etc.)
            if iso_dates:
                return None if ClientAPI.is_empty(obj) else obj.isoformat()
            else:
                return None if ClientAPI.is_empty(obj) else obj

        # # Handle Python datetime.datetime objects
        if isinstance(obj, datetime.datetime):
            if iso_dates:        
                return None if ClientAPI.is_empty(obj) else obj.isoformat()
            else:
                return None if ClientAPI.is_empty(obj) else obj
        
        # 2) Dict
        if isinstance(obj, dict):
            new_dict = {}
            for k, v in obj.items():
                # Recurse
                serialized_v = ClientAPI.serialize(v, iso_dates)
                # Only keep non-empty values
                if serialized_v is not None and not ClientAPI.is_empty(serialized_v):
                    new_dict[k] = serialized_v

            # If the resulting dict is empty, return None instead of {}
            return new_dict if new_dict else None

        # 3) DataFrame
        if isinstance(obj, pd.DataFrame):
            records = obj.to_dict(orient='records')
            # Each record is a dict, so we re-serialize it
            return [
                r for r in (ClientAPI.serialize(rec, iso_dates) for rec in records)
                if r is not None and not ClientAPI.is_empty(r)
            ]

        # 4) List/tuple/set
        if isinstance(obj, (list, tuple, set)):
            new_list = [
                ClientAPI.serialize(item, iso_dates)
                for item in obj
                if not ClientAPI.is_empty(item)
            ]
            # If the list ends up empty, return None
            return new_list if new_list else None

        # 5) For other objects with __dict__, treat them like a dict
        if hasattr(obj, "__dict__"):
            return ClientAPI.serialize(vars(obj), iso_dates)
        
        # 6) Convert ObjectId to string for JSON serialization
        if isinstance(obj, ObjectId):
            return str(obj)

        # 7) Otherwise, just return the raw value if it's not "empty"
        return obj if not ClientAPI.is_empty(obj) else None

    EMPTY_VALUES = {
        str: ["", "1.7976931348623157E308", "0.0", "nan", "NaN",],
        int: [0, 2147483647],
        float: [0.0, 1.7976931348623157e+308, np.nan, np.inf, -np.inf],
        datetime.datetime: [datetime.datetime(1, 1, 1, 0, 0)],
        pd.Timestamp: [pd.Timestamp("1970-01-01 00:00:00")],
        pd.NaT: [pd.NaT],
        pd.Timedelta: [pd.Timedelta(0)],
        pd.Interval: [pd.Interval(0, 0)],
        type(None): [None],
        bool: [False],
    }

    @staticmethod
    def is_empty(value):
        """
        Determine if the given value should be considered empty or a sentinel.
        
        This method checks for various conditions that signify emptiness, including:
        - Floating point NaN, infinity, zero, and maximum float values.
        - Pandas Timestamp objects that are NaT.
        - Values contained in predefined empty sets specific to their type.
        - Empty containers such as lists, tuples, sets, and dictionaries.
        - Pandas NaTType instances.
        
        Parameters:
            value (any): The value to check for emptiness.
        
        Returns:
            bool: True if the value is considered empty or a sentinel, False otherwise.
        """
        # Special handling for floats
        if isinstance(value, float):
            if math.isnan(value) or math.isinf(value):
                return True
            if value in (0.0, 1.7976931348623157e+308):
                return True

        # If it's a Timestamp and is NaT, treat as empty
        if isinstance(value, pd.Timestamp):
            if pd.isna(value):  # True for pd.NaT
                return True

        # Check if value is in our known empty sets
        value_type = type(value)
        if value_type in ClientAPI.EMPTY_VALUES:
            if value in ClientAPI.EMPTY_VALUES[value_type]:
                return True

        # Empty containers
        if isinstance(value, (list, tuple, set)) and len(value) == 0:
            return True
        if isinstance(value, dict) and len(value) == 0:
            return True
        if isinstance(value, pd._libs.tslibs.nattype.NaTType):
            return True

        return False

    @staticmethod
    def flatten_dict(d, parent_key='', sep='->'):
        """
        Recursively flattens a nested dictionary by concatenating keys.
        
        Parameters:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string to prepend to keys (used in recursion).
            sep (str): The separator between concatenated keys.
        
        Returns:
            dict: A new dictionary with nested keys flattened into single-level keys joined by the separator.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(ClientAPI.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def unflatten_dict(d, sep='->'):
        """
        Convert a flat dictionary with compound keys into a nested dictionary.
        
        Each key in the input dictionary `d` is split by the specified separator `sep` to create a hierarchy of nested dictionaries. The values are assigned to the innermost keys.
        
        Parameters:
            d (dict): The flat dictionary with compound keys.
            sep (str): The separator string used to split keys into nested levels. Default is '->'.
        
        Returns:
            dict: A nested dictionary constructed from the flat dictionary.
        """
        result = {}
        for key, value in d.items():
            parts = key.split(sep)
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                    current = current[part]

                else:
                    if not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
            current[parts[-1]] = value
        return result
            
    @staticmethod
    def documents2df(documents, database, flatten=True, drop_empty=True, serialize=True):
        """
        Convert a list of document dictionaries into a pandas DataFrame with optional serialization, flattening, and cleaning.
        
        Parameters:
            documents (list): A list of document dictionaries to convert.
            database (str): The name of the database, used to determine primary key columns.
            flatten (bool, optional): If True, flatten nested dictionaries in each document. Default is True.
            drop_empty (bool, optional): If True, drop columns that contain only None values. Default is True.
            serialize (bool, optional): If True, serialize ObjectId and datetime objects in the documents. Default is True.
        
        Returns:
            pandas.DataFrame: A DataFrame representation of the documents with the primary key columns set as the index if present.
        """
        if len(documents) == 0:
            return pd.DataFrame()
        # Serialize ObjectId and datetime objects
        if serialize:
            documents = ClientAPI.serialize(documents)
        # Flatten each document
        if flatten:
            documents = [ClientAPI.flatten_dict(doc) for doc in documents]
        
        # Convert the list of dictionaries into a DataFrame 
        df = pd.DataFrame(documents)
        
        if drop_empty:
            # Remove columns with all None values
            df = df.dropna(axis=1, how='all')
        
        # Set primary key as index        
        pkey_columns = DATABASE_PKEYS[database]
        if all(col in df.columns for col in pkey_columns):
            df.set_index(pkey_columns, inplace=True)

        return df
    
    @staticmethod
    def df2documents(df, database, unflatten=True, drop_empty=True):
        """
        Convert a pandas DataFrame into a list of dictionary documents suitable for database insertion.
        
        Parameters:
            df (pandas.DataFrame): The DataFrame to convert.
            database (str): The target database name, used to validate primary key columns.
            unflatten (bool, optional): If True, unflatten nested keys in the documents. Defaults to True.
            drop_empty (bool, optional): If True, drop rows and columns that are completely empty and remove empty fields from documents. Defaults to True.
        
        Returns:
            list of dict: A list of documents representing the DataFrame rows, with cleaned and optionally unflattened fields.
        
        Raises:
            ValueError: If the DataFrame's initial columns do not match the expected primary key columns for the specified database.
        """
        if df.empty:
            return []
        # Retrieve the expected primary key columns for this database
        pkey_columns = DATABASE_PKEYS[database]
        # Convert index to columns
        df = df.reset_index()
        if len(df.columns) >= len(pkey_columns):
            for icol, col in enumerate(pkey_columns):
                if df.columns[icol]!=pkey_columns[icol]:
                    raise ValueError(f"df2documents:Expected primary key column {pkey_columns}!")


        # MongoDB does not allow '.' in field names, so replace them with spaces
        df.columns = [str(s).replace('.','') for s in df.columns]

        # Drop rows and columns with all None/NaN values
        if drop_empty:
            df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')

        # Convert DataFrame to list of dictionaries
        documents = df.to_dict(orient='records')

        if drop_empty:
            # Remove empty fields in the documents
            for doc in documents:
                keys_to_remove = [key for key, value in doc.items() if ClientAPI.is_empty(value)]
                for key in keys_to_remove:
                    del doc[key]

        # Unflatten the documents if needed
        if unflatten:
            documents = [ClientAPI.unflatten_dict(doc) for doc in documents]

        return documents
    
    @staticmethod
    def get_collection(database, period, source, tablename, 
                        endpoint=None, query=None, sort=None,columns=None, 
                        page=None, per_page=None,load_all_pages=False,
                        output_dataframe=True, 
                        token=None, user=None):
        
        """
        '''
        Retrieve a collection of data from a specified database, period, source, and table via an API endpoint.
        
        Parameters:
        - database (str): The name of the database to query.
        - period (str): The time period for the data.
        - source (str): The data source identifier.
        - tablename (str): The name of the table to retrieve data from. Can include a subfolder separated by '/'.
        - endpoint (str, optional): Custom API endpoint URL. Defaults to environment variable 'SHAREDDATA_ENDPOINT' if not provided.
        - query (dict, optional): A query filter to apply to the data.
        - sort (dict, optional): Sorting instructions for the data.
        - columns (list, optional): List of columns to retrieve.
        - page (int, optional): Page number for paginated results.
        - per_page (int, optional): Number of records per page.
        - load_all_pages (bool, optional): If True, fetches all pages of data by iterating through pagination. Defaults to False.
        - output_dataframe (bool, optional): If True, returns the data as a pandas DataFrame; otherwise returns raw data list. Defaults to True.
        - token (str, optional): Authentication token. If not provided, attempts to use
        """
        url = os.environ['SHAREDDATA_ENDPOINT'] if not endpoint else endpoint

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/collection/{database}/{period}/{source}/{tablename}'
        url += route

        if not token is None:
            params['token'] = token
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if user:
            params['user'] = user
        if sort:
            params['sort'] = json_util.dumps(sort)
        if query:
            params['query'] = json_util.dumps(query)
        if columns:
            params['columns'] = json_util.dumps(columns)

        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page  
        
        params['format'] = 'bson'
        if load_all_pages:
            all_data = []
            current_page = 1
            while True:
                if not per_page:
                    per_page = 50000

                params['page'] = current_page
                params['per_page'] = per_page
                
                # Make the API request for the current page
                response = requests.get(url, params=params)
                ClientAPI.raise_for_status(response)

                if response.status_code == 204:
                    break

                decompressed_content = lz4f.decompress(response.content)
                bson_data = bson.BSON(decompressed_content).decode()
                data = bson_data.get('data', [])
                
                if not data:
                    break

                all_data.extend(data)

                # If less data than per_page is returned, we have reached the last page
                if len(data) < per_page:
                    break
                
                current_page += 1
            
            if not output_dataframe:
                return all_data
            
            return ClientAPI.documents2df(all_data, database)

        else:

            response = requests.get(url, params=params)
            ClientAPI.raise_for_status(response)

            if response.status_code == 204: 
                if not output_dataframe:
                    return []
                else:
                    return pd.DataFrame()
            
            decompressed_content = lz4f.decompress(response.content)
            bson_data = bson.BSON(decompressed_content).decode()  # Decode BSON to a dictionary

            data = bson_data.get('data', [])
            if not output_dataframe:
                return data
            
            df = ClientAPI.documents2df(data,database)
            return df

    @staticmethod
    def post_collection(database, period, source, tablename, 
            endpoint=None, 
            value=None, 
            token=None, user=None, hasindex=True):
            
        """
        Post a collection of data to a specified API endpoint.
        
        Parameters:
            database (str): The name of the database to post to.
            period (str): The period identifier for the data.
            source (str): The source identifier of the data.
            tablename (str): The name of the table to post data to. Can include a subfolder separated by '/'.
            endpoint (str, optional): The base URL of the API endpoint. Defaults to the environment variable 'SHAREDDATA_ENDPOINT' if not provided.
            value (pd.DataFrame or any): The data to be posted. If a DataFrame, it will be serialized after resetting its index.
            token (str, optional): Authentication token. Defaults to the environment variable 'SHAREDDATA_TOKEN' if not provided.
            user (str, optional): User identifier to include in the request parameters.
            hasindex (bool, optional): Indicates if the data includes an index. Defaults to True.
        
        Returns:
            dict: The JSON response from the API after posting the data.
        
        Raises:
            Exception: If no token is provided and 'SHAREDDATA_TOKEN' is not found in environment variables.
            HTTPError: If the HTTP request returns an unsuccessful status code.
        """
        url = os.environ['SHAREDDATA_ENDPOINT'] if not endpoint else endpoint

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/collection/{database}/{period}/{source}/{tablename}'
        url += route

        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if user:
            params['user'] = user
        
        params['hasindex'] = hasindex

        if isinstance(value, pd.DataFrame):            
            value = ClientAPI.serialize(value.reset_index())
        else:
            value = ClientAPI.serialize(value)
        bson_data = bson.encode({'data': value})
        compressed_data = lz4f.compress(bson_data)
        headers = {}
        headers['Content-Encoding'] = 'lz4'
        headers['Content-Type'] = 'application/octet-stream'

        # Make the POST request
        response = requests.post(url, headers=headers, params=params, data=compressed_data)
        ClientAPI.raise_for_status(response)

        return response.json()
    
    @staticmethod
    def patch_collection(database, period, source, tablename, 
            filter, update, endpoint=None,
            token=None, user=None, sort=None):     
        
        """
        '''
        Patch documents in a specified collection of a remote database via an HTTP PATCH request.
        
        Parameters:
            database (str): The name of the database.
            period (str): The period identifier for the data.
            source (str): The data source name.
            tablename (str): The name of the table or collection to patch. Can include a subfolder separated by '/'.
            filter (dict): A dictionary specifying the filter criteria to select documents to update.
            update (dict): A dictionary specifying the update operations to apply to the filtered documents.
            endpoint (str, optional): The base URL of the API endpoint. Defaults to environment variable 'SHAREDDATA_ENDPOINT' if not provided.
            token (str, optional): Authentication token for the API. Defaults to environment variable 'SHAREDDATA_TOKEN' if not provided.
            user (str, optional): Username associated with the request.
            sort (dict, optional): Sorting criteria for the documents.
        
        Returns:
            pandas.DataFrame: A DataFrame containing the updated documents indexed by their primary key. Returns an empty DataFrame if no data is returned or if the response status is 204 (No Content).
        
        Raises:
            Exception: If the authentication token is not found or if the HTTP request fails
        """
        url = os.environ['SHAREDDATA_ENDPOINT'] if not endpoint else endpoint

        params = {}
        if '/' in tablename:
            tablename_split = tablename.split('/')
            tablename = tablename_split[0]
            params['tablesubfolder'] = tablename_split[1]

        route = f'/api/collection/{database}/{period}/{source}/{tablename}'
        url += route

        if not token is None: 
            params['token'] = token 
        else:
            params['token'] = os.getenv('SHAREDDATA_TOKEN')
            if not params['token']:
                raise Exception('SHAREDDATA_TOKEN not found in environment variables')

        if user:
            params['user'] = user
        
        params['filter'] = json.dumps(filter)  # Convert filter to JSON string
        params['update'] = json.dumps(update)  # Convert update to JSON string
        if sort:
            params['sort'] = json.dumps(sort)  # Convert sort to JSON string

        try:
            response = requests.patch(url, params=params)
            ClientAPI.raise_for_status(response)  # Raise HTTPError for bad responses (4xx or 5xx)

            if response.status_code == 200:
                # Default to JSON
                rjson = json.loads(response.content)
                if not 'data' in rjson:
                    return pd.DataFrame([])
                df = pd.DataFrame([json.loads(rjson['data'])])
                if df.empty:
                    return df
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                pkey = rjson['pkey']
                df = df.set_index(pkey).sort_index()
                
                return df
            elif response.status_code == 204:
                return pd.DataFrame([])
        
        except Exception as e:
            Logger.log.error(f"ClientAPI patch_collection Error: {e}")
            raise e



