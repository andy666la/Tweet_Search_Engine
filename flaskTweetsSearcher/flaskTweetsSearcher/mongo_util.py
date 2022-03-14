import pymongo


class MongoUtil:
    def __init__(self):
        self.__mongo = ''
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["runoobdb"]
        dblist = client.list_database_names()
        # dblist = myclient.database_names()
        if "runoobdb" in dblist:
            print("数据库已存在！")
