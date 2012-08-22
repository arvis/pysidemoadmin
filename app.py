#!/usr/bin/python
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

from mongo import MongoAccess

class MainWindow(QtGui.QWidget):
    #def __init__(self, rows):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.table = QtGui.QTableWidget()
        self.db_list=QtGui.QComboBox()
        self.table_list=QtGui.QListWidget()


        self.db=MongoAccess()


        self.setWindowTitle("MongoDb browser")
        self.resize(800, 600)
        vbox = QtGui.QHBoxLayout()
        self.setLayout(vbox)

        mid_layout=QtGui.QVBoxLayout()

        mid_layout.addWidget(self.db_list)
        mid_layout.addWidget(self.table_list)
        #mid_layout.addWidget(self.table)
        vbox.addLayout(mid_layout)
        vbox.addWidget(self.table)

        #setting up events
        self.db_list.currentIndexChanged.connect(self.dbChanged)
        self.table_list.currentRowChanged.connect(self.tableChanged)

        #getting db data
        self.getDbList()


    def connectDb(self,host,port):
        self.db.connect(host,port)

        #self.connection = pymongo.Connection('localhost', 27017)


    def getDbList(self):
        db_list=self.db.getDbList()
        if db_list is not None:
            self.table_list.clear()
            self.db_list.addItems(db_list)


    def dbChanged(self,combo_index):
        self.table_list.clear()
        #self.table_list.adjustSize()
        self.table.clear()
        self.populateTableList(self.db_list.currentText())


    def populateTableList(self,dbName):
        self.table_list.clear()
        tables=self.db.getTableList(dbName)
        self.table_list.addItems(tables)
        self.table_list.adjustSize()



    def tableChanged(self,table_index):
        self.table.clear()
        self.populateTableData(self.table_list.currentItem().text())


    def populateTableData(self,table_name):
        self.table.clear()
        col_names=self.db.getTableColumns(table_name)
        table_data=self.db.getAll(table_name)
        self.setHeaders(col_names)
        self.table.setRowCount(table_data.count())

        for col_index,row in enumerate(table_data):
            for key in row:
                self.addCell(str(row[key]),col_names.index(key),col_index)


    def addCell(self,item_text,row,col):
        table_item = QtGui.QTableWidgetItem(item_text)
        self.table.setItem(col,row, table_item)


    def setHeaders(self,headers):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(tuple(headers))




if __name__ == "__main__":
    # ...
    rows = []
    # Here I have to fill it in an array, because you need to know the number of rows before adding... There might be a better solution though.
    app = QtGui.QApplication(sys.argv)
    test = MainWindow()
    test.show()
    app.exec_()
