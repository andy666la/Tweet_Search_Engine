import pymongo


class MongoUtil:
    def __init__(self):
        self.__mongo = ''
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["runoobdb"]
