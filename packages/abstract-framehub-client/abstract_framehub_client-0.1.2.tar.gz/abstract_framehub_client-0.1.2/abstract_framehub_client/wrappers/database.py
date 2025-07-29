from .collection import CollectionClient


class DatabaseClient:
    def __init__(self, parent, database: str):
        self._client = parent
        self._database = database
    
    def collection(self, collection: str) :
        return CollectionClient(self._client,self._database, collection)

    def create(self) -> bool : 
        return self._client.create_database(self._database)
        
    def drop(self) -> bool :
        return self._client.drop_database(self._database)