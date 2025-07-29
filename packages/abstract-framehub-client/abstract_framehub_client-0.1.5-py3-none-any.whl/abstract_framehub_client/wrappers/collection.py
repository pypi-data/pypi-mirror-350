from typing import Any, Dict, List

class CollectionClient:
    def __init__(self, parent, database: str, collection: str):
        self._client = parent
        self._database = database
        self._collection = collection

    def schema(self, jsonSchema: Dict[str,Any])  -> bool :
        doc = {"database" : self._database, "collection": self._collection, "jsonSchema" : jsonSchema}
        return self._client.schemas(doc)

    def transform(self, transformSchema: Dict[str,Any]) -> bool :
        doc = {"database" : self._database, "collection": self._collection, "transformSchema" : jsonSchema}
        return self._client.transforms(doc)

    def insert_one(self, document: Dict[str, Any]) -> str:
        return self._client.insert_one(self._database, self._collection, document)

    def insert_many(self, documents: List) -> str:
        return self._client.insert_many(self._database, self._collection, documents)

    def find(self, filter: Dict[str, Any] = {}, options: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        return self._client.find(self._database, self._collection, filter, options)

    def find_one(self, filter: Dict[str, Any]) -> Dict[str, Any]:
        return self._client.find_one(self._database, self._collection, filter)

    def update_one(self, filter: Dict[str, Any], update: Dict[str, Any]) -> int:
        return self._client.update_one(self._database, self._collection, filter, update)

    def delete_one(self, filter: Dict[str, Any]) -> int:
        return self._client.delete_one(self._database, self._collection, filter)

    def delete_many(self, filter: Dict[str, Any]) -> int:
        return self._client.delete_many(self._database, self._collection, filter)