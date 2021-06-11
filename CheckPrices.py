# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\FernandaBraga\Bridge & Co\Bridge Technology - Squad Athena - Squad Athena\Lote 45 - Otimização da Operação\Scripts\Aplicacao\CheckPricesote45.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# Importando Bibliotecas e arquivos necessários.
#from Lote45_v4 import getClientes
import pandas as pd
import sys,clr
import numpy as np
from tkinter import Tk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilenames

from pandas.core import frame

sys.path.append("C:\Program Files (x86)\Lote45\Lote45 Bridge Client")
clr.AddReference("zlib.net")
clr.AddReference("SocketClient")
clr.AddReference("SqlBridgeClient")
clr.AddReference("Lote45ClientTCP")
clr.AddReference("INIReader")
clr.AddReference("BridgeQuery")
clr.AddReference('System.Data')
from checkableCombobox import CheckableComboBox
from Lote45 import CSqlBridgeClientTCP
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

sqlBridgeClient = CSqlBridgeClientTCP()
sqlBridgeClient.CustomBridgeServer = "13.84.148.159"

##
arquivos = []

dfArquivos = pd.DataFrame(columns = ['Data','MktSource','Produto','Preço','Pricing Type'])
dfClientes = pd.DataFrame(columns=['idCliente','nomeCliente'])
dfMktSrc = pd.DataFrame(columns=['idMktSrc','nomeMktSrc'])







def getClientes(self):
    global dfClientes
    queryClientes = 'SELECT p1n_Id_Client AS ID, n0n_Str_ClientName AS Name FROM GLOBAL..Glb_Clients (NOLOCK) WHERE n0y_Dt_End IS NULL ORDER BY n0n_Str_ClientName'
    tbClientes = sqlBridgeClient.ResolveQuery(queryClientes)
    arrayAux = np.array([np.empty(2, dtype='<U100')])
    i = 0
    for linha in tbClientes.Rows:
        idCliente = linha['ID']
        nomeCliente = linha['Name']
        
        if (idCliente) != '':
            arrayAux = np.insert(arrayAux,i, [idCliente, nomeCliente], axis=0)
            self.clienteBox.addItem(nomeCliente)
            i = i + 1
    
    
    dfAux = pd.DataFrame(arrayAux,columns=['idCliente','nomeCliente'])
    dfAux.drop(index = dfAux.index[-1],axis=1,inplace=True) 
    dfClientes = dfClientes.append(dfAux)
    return True

def getMktSrc(self,nomeCliente):
    self.mkrSrcBox.clear()
    global dfClientes
    clSelecionado = dfClientes[dfClientes['nomeCliente']==nomeCliente]
    id_cliente = clSelecionado['idCliente'].values[0]
    queryMktSrc = 'SELECT n0y_Id_ResMktSource AS MktSrc, n0n_Str_Qualifier AS MktSrcName FROM APM..Glb_TradingDesk (NOLOCK) INNER JOIN LOTIS_LOTE45..Scn_MktSource WITH (NOLOCK) ON p1n_Id_MktSource = n0y_Id_ResMktSource WHERE f3n_Id_Client = ' + id_cliente + ' AND f4n_Id_TradingDeskType <> 2 AND n0n_Bl_IsActive = 1 AND n0y_EndDate IS NULL OR n0y_Id_ResMktSource = 0 GROUP BY n0y_Id_ResMktSource , n0n_Str_Qualifier'
    tbMktSrc = sqlBridgeClient.ResolveQuery(queryMktSrc)
	
    global dfMktSrc
    
    dfMktSrc = dfMktSrc.iloc[0:0]
    
    arrayAux = np.array([np.empty(2, dtype='<U100')])
    i = 0
    for linha in tbMktSrc.Rows:
        idMktSrc = linha['MktSrc']
        nomeMktSrc = linha['MktSrcName']
        if idMktSrc != '':
            arrayAux = np.insert(arrayAux,i, [idMktSrc, nomeMktSrc], axis=0)
            valor = str(idMktSrc) + " - " + nomeMktSrc
            self.mkrSrcBox.addItem(valor, idMktSrc)
            i = i + 1   

    dfAux = pd.DataFrame(arrayAux,columns=['idMktSrc','nomeMktSrc'])
    #print(dfAux)
    dfMktSrc = dfMktSrc.append(dfAux)
    #print(dfMktSrc)
    auxMkt = dfMktSrc["nomeMktSrc"]
    auxMkt.drop(index = auxMkt.index[-1],axis=1,inplace=True)
    return True









class Ui_SistemaChekPrices(object):
    def setupUi(self, SistemaChekPrices):
        SistemaChekPrices.setObjectName("SistemaChekPrices")
        SistemaChekPrices.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        SistemaChekPrices.setFont(font)
        SistemaChekPrices.setStyleSheet("background-color:rgb(214, 214, 214)")
        self.centralwidget = QtWidgets.QWidget(SistemaChekPrices)
        self.centralwidget.setObjectName("centralwidget")
        self.frameInformacoes = QtWidgets.QGroupBox(self.centralwidget)
        self.frameInformacoes.setGeometry(QtCore.QRect(10, 10, 771, 141))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.frameInformacoes.setFont(font)
        self.frameInformacoes.setStyleSheet("")
        self.frameInformacoes.setObjectName("frameInformacoes")
        self.label = QtWidgets.QLabel(self.frameInformacoes)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frameInformacoes)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frameInformacoes)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.clienteBox = QtWidgets.QComboBox(self.frameInformacoes) #!
        self.clienteBox.setGeometry(QtCore.QRect(120, 20, 301, 21))
        self.clienteBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.clienteBox.setObjectName("clienteBox")
        self.clienteBox.setCurrentIndex(5)
        self.mkrSrcBox = CheckableComboBox(self.frameInformacoes)     #!
        self.mkrSrcBox.setGeometry(QtCore.QRect(120, 50, 301, 21))
        self.mkrSrcBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.mkrSrcBox.setFrame(True)
        self.mkrSrcBox.setObjectName("mkrSrcBox")
        self.arqBox = QtWidgets.QLineEdit(self.frameInformacoes) #!
        self.arqBox.setGeometry(QtCore.QRect(120, 80, 461, 20))
        self.arqBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.arqBox.setObjectName("arqBox")
        self.pushButton = QtWidgets.QPushButton(self.frameInformacoes)
        self.pushButton.setGeometry(QtCore.QRect(590, 80, 75, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frameInformacoes)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 110, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 160, 771, 241))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.resultTable = QtWidgets.QTableWidget(self.groupBox)
        self.resultTable.setGeometry(QtCore.QRect(10, 20, 751, 211))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.resultTable.setFont(font)
        self.resultTable.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.resultTable.setProperty("showDropIndicator", True)
        self.resultTable.setDragEnabled(True)
        self.resultTable.setAlternatingRowColors(True)
        self.resultTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.resultTable.setGridStyle(QtCore.Qt.SolidLine)
        self.resultTable.setCornerButtonEnabled(False)
        self.resultTable.setRowCount(1)
        self.resultTable.setColumnCount(13)
        self.resultTable.setObjectName("resultTable")
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(12, item)
        self.resultTable.horizontalHeader().setCascadingSectionResizes(False)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 410, 771, 181))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.processTable = QtWidgets.QTableWidget(self.groupBox_2)
        self.processTable.setGeometry(QtCore.QRect(10, 20, 751, 141))
        self.processTable.setObjectName("processTable")
        self.processTable.setColumnCount(0)
        self.processTable.setRowCount(0)
        SistemaChekPrices.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SistemaChekPrices)
        self.statusbar.setObjectName("statusbar")
        SistemaChekPrices.setStatusBar(self.statusbar)

        auxCli = getClientes(self)

        self.clienteBox.currentIndexChanged.connect(self.clientesSelected)
        self.pushButton.clicked.connect(self.procurarClicked)
        self.pushButton_2.clicked.connect(self.importarClicked)

        self.retranslateUi(SistemaChekPrices)
        QtCore.QMetaObject.connectSlotsByName(SistemaChekPrices)  
        
    def clientesSelected(self):
        auxCliente = self.clienteBox.currentText()
        auxMkt = getMktSrc(self,auxCliente)
        
    def anula(self):
        print('s')


    def procurarClicked(self):
        print('Apertou Procurar')
        self.procurar()
    def procurar(self):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        files = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
        #arquivo = StringVar()
        i = 0
        self.str_Arquivos = ""
        #print(files)
        for file in files:
            #arquivos.insert(i, file)
            if i == 0 :
                self.str_Arquivos = str(file)
            else:
                self.str_Arquivos = self.str_Arquivos + "," + str(file)
            i+=1
            print(self.str_Arquivos)
            self.arqBox.setText(self.str_Arquivos)
            
    def importarClicked(self):
        print('Apertou Importar')
        self.importar()
    def importar(self):
        print('Importando...')
        print(self.str_Arquivos)
        print(self.mkrSrcBox.currentText())
        print(self.clienteBox.currentText())
        
        arq = self.str_Arquivos
        files = []
        if ',' in arq:
            files = arq.split(',')
        else:
            files.insert(0,arq)
        for file in files:
            aux = pd.read_excel(file)
            #padraoArquivo = verificaPadrao(aux, file)
            padraoArquivo = True
            answer = 'yes'
            if padraoArquivo:
                    aux = aux.rename(columns={'MktSource': 'nomeMktSrc'})
                    df = aux[['Data','nomeMktSrc','Produto','Preço','Pricing Type']]
                    #if (answer == 'yes'):
                    #    df[['nomeMktSrc']] = df[['nomeMktSrc']].fillna(value=mkts)
                    df = df.dropna()
                    print(df)
                    #tipoArquivo = verificaTipo(df)
                    #if tipoArquivo:
                    #    dfArquivos = dfArquivos.append(df)     #Tabela sem preço
                    #    dfglobal = pd.merge(dfArquivos,dfMktSrc,on = 'nomeMktSrc',how = 'left') #Tabela que vai ter preço
                    #    dfglobal["Preços Procurados"] = ""
                    #    dfglobal["Currency"] = ""
                    #    dfglobal["PU Real"] = ""
                    #    dfglobal["PU Dolar"] = ""
                    #    dfglobal["PU Euro"] = ""
                    #    dfglobal["Product Class"] = ""
                    #    dfglobal["Paridade USD/BRL"] = ""
                    #    dfglobal["Paridade EUR/BRL"] = ""
                    #    del dfglobal["MktSource"]


    def retranslateUi(self, SistemaChekPrices):
        _translate = QtCore.QCoreApplication.translate
        SistemaChekPrices.setWindowTitle(_translate("SistemaChekPrices", "Sistema Check Prices"))
        self.frameInformacoes.setTitle(_translate("SistemaChekPrices", "Informações"))
        self.label.setText(_translate("SistemaChekPrices", "Cliente:"))
        self.label_2.setText(_translate("SistemaChekPrices", "Market Source:"))
        self.label_3.setText(_translate("SistemaChekPrices", "Arquivo:"))
        self.pushButton.setText(_translate("SistemaChekPrices", "Procurar"))
        self.pushButton_2.setText(_translate("SistemaChekPrices", "Importar"))
        self.groupBox.setTitle(_translate("SistemaChekPrices", "Resultado"))
        self.resultTable.setSortingEnabled(True)
        item = self.resultTable.horizontalHeaderItem(0)
        item.setText(_translate("SistemaChekPrices", "Date"))
        item = self.resultTable.horizontalHeaderItem(1)
        item.setText(_translate("SistemaChekPrices", "Product"))
        item = self.resultTable.horizontalHeaderItem(2)
        item.setText(_translate("SistemaChekPrices", "Desired Price"))
        item = self.resultTable.horizontalHeaderItem(3)
        item.setText(_translate("SistemaChekPrices", "Pricing Type"))
        item = self.resultTable.horizontalHeaderItem(4)
        item.setText(_translate("SistemaChekPrices", "Market Source"))
        item = self.resultTable.horizontalHeaderItem(5)
        item.setText(_translate("SistemaChekPrices", "Product Class"))
        item = self.resultTable.horizontalHeaderItem(6)
        item.setText(_translate("SistemaChekPrices", "Current Price"))
        item = self.resultTable.horizontalHeaderItem(7)
        item.setText(_translate("SistemaChekPrices", "Currency"))
        item = self.resultTable.horizontalHeaderItem(8)
        item.setText(_translate("SistemaChekPrices", "New Column"))
        item = self.resultTable.horizontalHeaderItem(9)
        item.setText(_translate("SistemaChekPrices", "PU USD"))
        item = self.resultTable.horizontalHeaderItem(10)
        item.setText(_translate("SistemaChekPrices", "PU EUR"))
        item = self.resultTable.horizontalHeaderItem(11)
        item.setText(_translate("SistemaChekPrices", "USD/BRL Parity"))
        item = self.resultTable.horizontalHeaderItem(12)
        item.setText(_translate("SistemaChekPrices", "EUR/BRL Parity"))
        self.groupBox_2.setTitle(_translate("SistemaChekPrices", "Processamento"))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SistemaChekPrices = QtWidgets.QMainWindow()
    ui = Ui_SistemaChekPrices()
    ui.setupUi(SistemaChekPrices)
    SistemaChekPrices.show()
    sys.exit(app.exec_())
