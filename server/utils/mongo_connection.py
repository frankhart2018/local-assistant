import pymongo
from typing import Dict, Any
from bson.objectid import ObjectId

from .constants import CONN_STRING, DB_NAME


class MongoDB:
    def __init__(self, collection):
        self.__client = pymongo.MongoClient(CONN_STRING)
        self.__db = self.__client[DB_NAME]
        self.__collection = self.__db[collection]

    def find_one(self, query_dict: Dict[Any, Any]):
        return self.__collection.find_one(query_dict)

    def insert_one(self, insertion_data: Dict[Any, Any]):
        res = self.__collection.insert_one(insertion_data)
        return str(res.inserted_id)

    def find_by_id(self, id: str):
        object_id = ObjectId(id)
        return self.find_one({"_id": object_id})
