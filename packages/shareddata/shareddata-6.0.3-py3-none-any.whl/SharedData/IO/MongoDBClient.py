import os
from pymongo import MongoClient
from typing import Optional

class MongoDBClient:
    """
    Singleton class for managing a MongoDB client connection.

    Ensures only one client instance per application process.
    Provides dictionary-like access to collections, namespaced by 'SharedData' or a specific user.

    Attributes:
        _instance (Optional[MongoDBClient]): Singleton instance.
        _client (MongoClient): The MongoDB client connection.
        _user (Optional[str]): The user scope for accessing the database, or None for shared data.
    """
    _instance: Optional["MongoDBClient"] = None

    def __new__(cls, user: Optional[str] = None) -> "MongoDBClient":
        """
        Create or return the singleton instance of MongoDBClient.

        Args:
            user (Optional[str]): Optional user to scope database access.

        Returns:
            MongoDBClient: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_client(user)
        return cls._instance

    def _init_client(self, user: Optional[str]) -> None:
        """
        Initializes MongoDB client and sets the user.

        Args:
            user (Optional[str]): The user scope to associate with this client instance.
        """
        mongodb_conn_str = (
            f'mongodb://{os.environ["MONGODB_USER"]}:'
            f'{os.environ["MONGODB_PWD"]}@'
            f'{os.environ["MONGODB_HOST"]}:'
            f'{os.environ["MONGODB_PORT"]}/'
        )
        self._client = MongoClient(mongodb_conn_str)
        self._user = user

    def __getitem__(self, collection_name: str):
        """
        Access a MongoDB collection by name.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection object, namespaced by user or shared.
        """
        db_name = self._user if self._user else 'SharedData'
        return self._client[db_name][collection_name]

    @property
    def client(self) -> MongoClient:
        """
        Get the underlying MongoClient object.

        Returns:
            MongoClient: The active MongoDB client.
        """
        return self._client

    @client.setter
    def client(self, value: MongoClient) -> None:
        """
        Set the underlying MongoClient object.

        Args:
            value (MongoClient): The new MongoDB client instance.
        """
        self._client = value
