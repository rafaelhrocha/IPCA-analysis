import sqlite3
import api
import numpy as np
import requests  # necessary isntall
import pandas as pd #necessary install
from matplotlib import pyplot #necessary install


class DataBase():

    def __init__(self):
        self.dataDict = {}
        self.tableData = []
        self.createTable()
        self.getData()
        self.getDataToDB()
        self.insertInExcel()
        self.createGraph()


    def createTable(self):
        print('Create table in DB')
        self.connect = sqlite3.connect('./db.db')
        self.cursor = self.connect.cursor()
        try:
            self.cursor.execute('CREATE TABLE IPCA(date, value)')
        except sqlite3.OperationalError:
            print('Table already exists')

    def getData(self):
        print('Call API')
        try:
            response = (requests.get(api.api['getIPCA'], verify=False)).json()
        except:
            print('Get API error, try again')
            exit()

        for a in response:
            self.cursor.execute('INSERT INTO IPCA VALUES(?,?)', (a['data'], a['valor']))
            self.connect.commit()
            pass

    def getDataToDB(self):
        print('Get data in DB')
        for row in self.cursor.execute('SELECT date, value FROM IPCA'):
            day, month, year = row[0].split('/')
            if self.dataDict.get(year):
                self.dataDict[year] = self.dataDict[year] + float(row[1])
                temp = '{:.2f}'.format(self.dataDict[year])
                self.dataDict[year] = float(temp)
            else:
                self.dataDict[year] = float(row[1])

        self.date =  list(self.dataDict.keys())
        self.value = list(self.dataDict.values())
        self.tableData = list(self.dataDict.items())

    
    def insertInExcel(self):
        self.df = pd.DataFrame(self.tableData, columns=list(['YEAR','VALUE']))
        print('Insert data in excel')
        with pd.ExcelWriter('IPCA.xlsx') as writer:
            self.df.to_excel(writer, sheet_name='IPCA analysis',index=False, header=False)

    
    def createGraph(self):
        print('Create graph and table')

        fig, ax = pyplot.subplots(dpi=150, num="IPCA analysis - Table")
        ccolors = np.full(len(self.value), 'lightcyan')
        table = ax.table(
            cellText=self.df.values,
            colLabels=self.df.columns,
            loc='center',
            rowLoc='center',
            cellLoc='center',
            colColours=ccolors,
        )
        ax.axis('off')
        table.scale(0.63, 0.63)
        table.set_fontsize(6)
        
        pyplot.figure('IPCA analysis - Graph')
        pyplot.bar(self.date, self.value, color = 'blue', width = 0.6)
        pyplot.title('IPCA PER YEAR')
        pyplot.xlabel('YEARS')
        pyplot.ylabel('SUM IPCA')
        pyplot.xticks(range(0,42,5))

        pyplot.show()

 

