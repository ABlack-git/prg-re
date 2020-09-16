import pymongo


class MongoRepository:
    def __init__(self, host, port, database):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client.get_database(database)

    def delete(self):
        pass

    def read_checkpoint(self):
        pass

    def save_checkpoint(self):
        pass

    def insert_one(self, collection, data):
        return self.db.get_collection(collection).insert_one(data)
