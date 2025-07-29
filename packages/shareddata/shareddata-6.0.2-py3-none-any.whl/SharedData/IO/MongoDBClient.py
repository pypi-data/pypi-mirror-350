import os

from pymongo import MongoClient, errors
from pymongo import ASCENDING, DESCENDING

class MongoDBClient:
    """
    Singleton class for managing a MongoDB client connection.
    
    This class ensures that only one instance of the MongoDB client exists per user.
    It initializes the MongoDB client using connection details from environment variables.
    The client provides access to MongoDB collections via dictionary-style access.
    
    Attributes:
        _instance (MongoDBClient): The singleton instance of the class.
        _user (str): The username associated with the MongoDB client.
    
    Methods:
        __new__(cls, user=None):
            Creates or returns the singleton instance, initializing the client if necessary.
        __getitem__(self, collection_name):
            Provides access to a MongoDB collection for the specified user or shared data.
        client (property):
            Gets the underlying MongoClient instance.
        client (setter):
            Sets the underlying MongoClient instance.
    """
    _instance = None
    _user = None

    def __new__(cls, user=None):
        """
        Create a singleton instance of MongoDBClient, initializing the MongoDB client connection if it doesn't already exist.
        
        Parameters:
            user (optional): A user object to associate with the client instance if not already set.
        
        Returns:
            MongoDBClient: The singleton instance of the MongoDBClient class with an active MongoDB connection.
        
        Behavior:
        - If the class-level _user attribute is None, it sets it to the provided user.
        - If the class-level _instance attribute is None, it creates a new instance of MongoDBClient.
        - Constructs the MongoDB connection string using environment variables:
          MONGODB_USER, MONGODB_PWD, MONGODB_HOST, and MONGODB_PORT.
        - Initializes a MongoClient with the constructed connection string and assigns it to the instance.
        - Returns the singleton instance.
        """
        if cls._user is None:
            cls._user = user

        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            mongodb_conn_str = (f'mongodb://{os.environ["MONGODB_USER"]}:'
                                f'{os.environ["MONGODB_PWD"]}@'
                                f'{os.environ["MONGODB_HOST"]}:'
                                f'{os.environ["MONGODB_PORT"]}/')
            cls._instance.client = MongoClient(mongodb_conn_str)
        return cls._instance

    def __getitem__(self, collection_name):
        """
        Retrieve a collection by name from the database client.
        
        If a user is specified, the collection is retrieved from the user's namespace.
        Otherwise, the collection is retrieved from the 'SharedData' namespace.
        
        Args:
            collection_name (str): The name of the collection to retrieve.
        
        Returns:
            Collection: The requested collection object.
        """
        if self._user is None:
            return self._client['SharedData'][collection_name]
        else:
            return self._client[self._user][collection_name]

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        """
        Setter method for the 'client' attribute.
        
        Parameters:
            value: The new value to set for the 'client' attribute.
        """
        self._client = value        