import sqlite3
import api
import requests  # necessary isntall
import pandas as pd #necessary install
from matplotlib import pyplot, font_manager #necessary install


class DataBase():

    def __init__(self):
        self.dataDict = {}
        self.tableData = []
        self.createTable()
        self.getData()
        self.getDataToDB()
        self.createGraph()

    def createTable(self):
        self.connect = sqlite3.connect('./db.db')
        self.cursor = self.connect.cursor()
        try:
            self.cursor.execute('CREATE TABLE IPCA(date, value)')
        except sqlite3.OperationalError:
            print('Table already exists')

    def getData(self):
        try:
            response = (requests.get(api.api['getIPCA'], verify=False)).json()
        except:
            print('Get API error, try again')
            exit()

        for a in response:
            # self.cursor.execute('INSERT INTO IPCA VALUES(?,?)', (a['data'], a['valor']))
            # self.connect.commit()
            pass

    def getDataToDB(self):
        for row in self.cursor.execute('SELECT date, value FROM IPCA'):
            day, month, year = row[0].split('/')
            if self.dataDict.get(year):
                self.dataDict[year] = self.dataDict[year] + round(float(row[1]),2)
            else:
                self.dataDict[year] = round(float(row[1]),2)

    def createGraph(self):
        self.date =  list(self.dataDict.keys())
        self.value = list(self.dataDict.values())
        self.tableData = list(self.dataDict.items())

        

        pyplot.figure('IPCA analysis',figsize=(4,2))
        pyplot.subplot(1,2,1)
        pyplot.bar(self.date, self.value, color = 'blue', width = 0.6)
        pyplot.title('IPCA PER YEAR')
        pyplot.xlabel('YEARS')
        pyplot.ylabel('SUM IPCA')
        pyplot.xticks(range(0,42,5))

        pyplot.subplot(1,2,2)
        table = pyplot.table(cellText=self.tableData,loc='center')
        table.set_fontsize(2)
        table.scale(0.5,1)
        pyplot.axis('off')

        window = pyplot.get_current_fig_manager()
        window.window.showMaximized()
        pyplot.show()


        

