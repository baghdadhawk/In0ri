import os
import pymongo

connection = pymongo.MongoClient(
    "mongodb://"
    + os.environ["MONGODB_USERNAME"]
    + ":"
    + os.environ["MONGODB_PASSWORD"]
    + "@"
    + os.environ["MONGODB_HOSTNAME"]
    + ":27017/"
)
database = connection["deface"]


class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.collection = database[database_name]

    def insert_data(self, data):
        document = self.collection.insert_one(data)
        return document.inserted_id

    def get_single_data(self, data):
        data = self.collection.find_one(data)
        return data

    def get_multiple_data(self):
        data = self.collection.find()
        return list(data)

    def update_existing(self, unique, data):
        document = self.collection.update_one(unique, {"$set": data})
        return document.acknowledged

    def update_noexiting(self, unique, data):
        document = self.collection.update_one(unique, {"$set": data}, upsert=True)
        return document.acknowledged

    def update_empty(self, unique, data):
        # Remove specified keys from the document. ``data`` should provide the
        # fields to unset, the values are ignored by MongoDB when using
        # ``$unset``.
        unset_fields = {key: "" for key in data.keys()}
        document = self.collection.update_one(unique, {"$unset": unset_fields})
        return document.acknowledged

    def remove_data(self, data):
        document = self.collection.delete_one(data)
        return document.acknowledged
