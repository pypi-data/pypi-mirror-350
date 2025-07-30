import os
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional


class MongoDBClient:
    """
    Singleton class for managing a MongoDB client connection.

    Ensures only one client instance per application process.
    Provides dictionary-like access to collections, namespaced by 'SharedData' or a specific user.

    Attributes:
        _instance (Optional[MongoDBClient]): Singleton instance (class variable).
        _client (MongoClient): The MongoDB client connection.
        _user (Optional[str]): The user scope for accessing the database, or None for shared data.
    """
    _instance: Optional["MongoDBClient"] = None
    _user: Optional[str] = None  # Ensures _user attribute always exists
    _initialized: bool = False   # To prevent re-initialization

    def __new__(cls, user: Optional[str] = None) -> "MongoDBClient":
        """
        Creates (if needed) and returns the singleton instance of MongoDBClient.
        If the singleton already exists, the user context cannot be changed.

        Args:
            user (Optional[str]): Optional user to scope database access.

        Returns:
            MongoDBClient: The singleton instance.

        Raises:
            RuntimeError: If an attempt is made to change the user on the singleton.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_client(user)
            cls._initialized = True
        else:
            # Prevent changing user context for safety
            if user != cls._instance._user:
                raise RuntimeError(
                    f"MongoDBClient singleton already initialized with user '{cls._instance._user}', cannot change to '{user}'."
                )
        return cls._instance

    def _init_client(self, user: Optional[str]) -> None:
        """
        Initializes the MongoDB client and sets the user.

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

    def __getitem__(self, collection_name: str) -> Collection:
        """
        Access a MongoDB collection by name, scoped by user or shared namespace.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection object.
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