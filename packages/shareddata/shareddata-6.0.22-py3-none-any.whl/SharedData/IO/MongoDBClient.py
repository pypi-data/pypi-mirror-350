import os
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional


class MongoDBClient:
    
    def __init__(self, user = 'SharedData'):
        self._user = user
        mongodb_conn_str = (
            f'mongodb://{os.environ["MONGODB_USER"]}:'
            f'{os.environ["MONGODB_PWD"]}@'
            f'{os.environ["MONGODB_HOST"]}:'
            f'{os.environ["MONGODB_PORT"]}/'
        )
        self._client = MongoClient(mongodb_conn_str)
        

    def __getitem__(self, collection_name: str) -> Collection:        
        return self._client[self._user][collection_name]

    @property
    def client(self) -> MongoClient:        
        return self._client

    @client.setter
    def client(self, value: MongoClient) -> None:        
        self._client = value