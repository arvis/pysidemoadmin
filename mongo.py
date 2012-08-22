# -*- coding: utf-8 -*-

"""
class for easy accessing MongoDb databases

"""
#import pymongo
import json
#from bson import BSON
from bson import json_util
import pymongo


class MongoAccess(object):
    """class for easy accessing MongoDb databases

    """
    def __init__(self, host="localhost",port=27017):
        super(MongoAccess, self).__init__()
        #self.host = host
        #self.port=port
        self.table_name=""
        self.connection=None
        self.db=None

        self.connect(host,port)

    def connect(self, host="localhost",port=27017):
        """ connect to database """
        self.connection = pymongo.Connection(host, port)

    def setDatabase(self,db_name):
        self.db = self.connection[db_name]

    def setTable(self,table_name):
        self.table_name=table_name

    def getDbList(self):
        data= self.connection.database_names()
        return data

    def getTableList(self,db_name=None):
        data=[]
        if db_name is not None:
            self.setDatabase(db_name)

        if self.db is not None:
            data= self.db.collection_names()
            data.remove("system.indexes")

        return data

    def getTableColumns(self,table_name):

        from bson.code import Code

        map_function=Code("function(){for (var key in this) { emit(key, null); }}")
        reduce_function=Code("function(key, stuff) { return null; }")

        mr=self.db[table_name].map_reduce(map_function,reduce_function, "things" + "_keys")

        #TODO: fund better functions to get all column data
        col_names=[]
        for doc in mr.find():
            col_names.append(doc["_id"])

        return col_names

    def getAll(self,table_name="",data_filter={}):

        if self.connection is None:
            print "cannot get connection"
            return None

        if self.db is None:
            # TODO: write to log or somewher
            #print "cannot get db"
            return None

        if table_name=="":
            table_name=self.table_name

        data=self.db[table_name].find()
        return data



    def getOne(self,table_name,data_filter={}):
        if self.db is None:
            print "cannot get connection"
            return None

        data=self.db[table_name].find_one(data_filter)
        return data

    def insert(self,table_name,row_data):
        # TODO: exception handling
        if self.db is None:
            print "cannot get connection"
            return None

        return self.db[table_name].save(row_data)

    def save(self,table_name,row_data):
        """inserts or updates data if _id is not given"""
        if self.db is None:
            print "cannot get connection"
            return None

        return self.db[table_name].save(row_data)


    def update(self,table_name,row_data):
        if self.db is None:
            print "cannot get connection"
            return None

        return self.db[table_name].update({"_id":row_data["_id"]}, row_data)

    def deleteOne(self,table_name, row_data):
        row_id=row_data["_id"]
        self.db[table_name].remove(row_id)

    def delete(self,table_name, data_filter):
        self.db[table_name].remove(data_filter)


    def dropTable(self,table_name):
        if self.db is None:
            return None
        self.db.drop_collection(table_name)

    def dropDatabase(self,db_name):
        self.connection.drop_database(db_name)

    def asJSON(self,data, sort_keys=True, indent=4):
        
        return json.dumps(list(data), default=json_util.default)



