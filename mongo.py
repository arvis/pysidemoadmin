# -*- coding: utf-8 -*-

"""
class for easy accessing MongoDb databases

"""


class MongoAccess(object):
    """class for easy accessing MongoDb databases

    """
    def __init__(self, arg):
        super(MongoAccess, self).__init__()
        self.arg = arg


    def connect(self,host,port):
        """ connect to database """
        pass

    def set_database(self,db_name):
        pass

    def get_all(self,table_name):
        pass

    def get_one(self,table_name,id):
        pass

    def insert_row(self,table_name,row_data):
        pass


    def update_row(self,table_name,row_data):
        """
        updates one row
        row_data: array tuple


        """
        pass

    def delete_one(self,table_name, id):
        pass


