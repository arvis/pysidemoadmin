# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtCore, QtGui, QtSql 
import pymongo

#class Test(QtGui.QWidget):
"""

Trying to get grid working
good explanation:
http://stackoverflow.com/questions/10610804/design-of-the-model-for-qtableview-in-pyside-sqlalchemy
documentation: http://www.pyside.org/docs/pyside/PySide/QtGui/QTableView.html


"""

class MainWindow(QtGui.QWidget):
    #def __init__(self, rows):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.table = QtGui.QTableWidget()
        self.table_list=QtGui.QListWidget()

        #getting db data
        self.connect_db()
        self.set_db("truckroutes")
        self.table_data=self.db.drivers

        tbls=self.get_table_list()
        self.set_table_list(tbls)

        self.table_list.clicked.connect(self.item_clicked)

        #FIXME: checking how many rows are returned
        if self.table_data.find().count()==0:
            #return
            pass

        headers=self.table_data.find()[0].keys()
        self.set_headers(headers)

        self.table.setRowCount(self.table_data.find().count())
        for col_index,row in enumerate(self.table_data.find()):
            #print col_index,row
            for row_index, row_val in enumerate(row.values()):
                self.add_table_cell(str(row_val), row_index,col_index)



        self.setWindowTitle("MongoDb browser");
        vbox = QtGui.QHBoxLayout()
        self.setLayout(vbox)

        mid_layout=QtGui.QHBoxLayout()
        mid_layout.addWidget(self.table_list)
        mid_layout.addWidget(self.table)
        vbox.addLayout(mid_layout)


    def item_clicked(self, item):
        print self.table_list.selectedItems()[0].text()


    def item_dblclicked(self, item):
        print "itemDoubleClicked"

    def changeDb(self,db_name):
        self.set_db(db_name)
        #TODO: change all items in database


    def get_all(self,table_name):
        """  """
        pass

    def set_table_list(self, tables):
        for table in tables:
            table_item = QtGui.QListWidgetItem(table)
            self.table_list.addItem(table_item)

    def add_table_cell(self,item_text,row,col):
        table_item = QtGui.QTableWidgetItem(item_text)
        self.table.setItem(col,row, table_item)



    def set_headers(self,headers):
        #self.table.setHorizontalHeaderLabels(("First Name", "Last Name", "Address"))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(tuple(headers))


    def set_row_count(self,row_count=0):
        self.table.setRowCount(row_count)




    def connect_db(self):
        self.connection = pymongo.Connection('localhost', 27017)
        #self.db = connection['truckroutes']

    def set_db(self,db_name):
        self.db = self.connection[db_name]
        return True


    def get_table_list(self):
        return self.db.collection_names()


    def get_table_data(self, table_name):
        pass


if __name__ == "__main__":
    # ...
    rows = []
    # Here I have to fill it in an array, because you need to know the number of rows before adding... There might be a better solution though.
    app = QtGui.QApplication(sys.argv)
    test = MainWindow()
    test.show()
    app.exec_()
