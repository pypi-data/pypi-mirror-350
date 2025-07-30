from pymongo import MongoClient
from pymongo.collection import Collection

from ed_infrastructure.persistence.interfaces.abc_db_client import ABCDbClient

UUID_REPRESENTATION = "standard"


class DbClient(ABCDbClient):
    def __init__(self, connection_string: str, db_name: str):
        self._client = MongoClient(
            connection_string,
            uuidRepresentation=UUID_REPRESENTATION,
        )
        self._db = self._client[db_name]

    def get_collection(self, collection_name: str) -> Collection:
        return self._db[collection_name]

    def start(self): ...

    def stop(self):
        self._client.close()
