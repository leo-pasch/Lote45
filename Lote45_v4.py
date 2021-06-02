# -*- coding: utf-8 -*-

# Importando Bibliotecas e arquivos necessários.
from tkinter import Tk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pandas as pd
import sys,clr
import numpy as np

sys.path.append("C:\Program Files (x86)\Lote45\Lote45 Bridge Client")
clr.AddReference("zlib.net")
clr.AddReference("SocketClient")
clr.AddReference("SqlBridgeClient")
clr.AddReference("Lote45ClientTCP")
clr.AddReference("INIReader")
clr.AddReference("BridgeQuery")
clr.AddReference('System.Data')
from Lote45 import CSqlBridgeClientTCP
##

#! Definição de Funções
mkts = ''
answer = ''
mktstate = 'normal'
dfglobal = pd.DataFrame()
def clienteSelecionado(event):
    nomeCliente = comboClientes.get()
    
    global dfClientes
    clSelecionado = dfClientes[dfClientes['nomeCliente']==nomeCliente]
    id_cliente = clSelecionado['idCliente'].values[0]
    queryMktSrc = 'SELECT n0y_Id_ResMktSource AS MktSrc, n0n_Str_Qualifier AS MktSrcName FROM APM..Glb_TradingDesk (NOLOCK) INNER JOIN LOTIS_LOTE45..Scn_MktSource WITH (NOLOCK) ON p1n_Id_MktSource = n0y_Id_ResMktSource WHERE f3n_Id_Client = ' + id_cliente + ' AND f4n_Id_TradingDeskType <> 2 AND n0n_Bl_IsActive = 1 AND n0y_EndDate IS NULL OR n0y_Id_ResMktSource = 0 GROUP BY n0y_Id_ResMktSource , n0n_Str_Qualifier'
    tbMktSrc = sqlBridgeClient.ResolveQuery(queryMktSrc)
	
    global dfMktSrc
    global mkts
    global answer
    global mktstate
    global comboMkt
    
    dfMktSrc = dfMktSrc.iloc[0:0]
    
    arrayAux = np.array([np.empty(2, dtype='<U100')])
    i = 0
    for linha in tbMktSrc.Rows:
        idMktSrc = linha['MktSrc']
        nomeMktSrc = linha['MktSrcName']
        if idMktSrc != '':
            arrayAux = np.insert(arrayAux,i, [idMktSrc, nomeMktSrc], axis=0)
            i = i + 1   
    
    if (mkts) == '':
        #print('MktSource ainda não adicionado')
        answer = tk.messagebox.askquestion(title = "Seleção de Market Source",message = "Deseja selecionar um Market Source para onde não houver ? Se sim, escolha ele abaixo")
        if answer == 'no':
            mktstate = 'disabled'
            comboMkt = ttk.Combobox(wrapper, width=40,state = mktstate) 
            comboMkt.grid(column=1, row=1, sticky="E", padx=10)
            comboMkt.bind("<<ComboboxSelected>>", mktSelecionado)
        else:
            mktstate = 'normal'
            comboMkt = ttk.Combobox(wrapper, width=40,state = mktstate) 
            comboMkt.grid(column=1, row=1, sticky="E", padx=10)
            comboMkt.bind("<<ComboboxSelected>>", mktSelecionado)
            
        #print(answer)
    else:
        tk.messagebox.showinfo(title = "Informe", message="Está sendo usado como Market Source: "+str(mkts))
    
    dfAux = pd.DataFrame(arrayAux,columns=['idMktSrc','nomeMktSrc'])
    dfMktSrc = dfMktSrc.append(dfAux)
    auxMkt = dfMktSrc["nomeMktSrc"]
    auxMkt.drop(index = auxMkt.index[-1],axis=1,inplace=True)    
    auxMktArray = auxMkt.values.tolist()
    comboMkt["values"] = auxMktArray


def mktSelecionado(event):
    mkt = comboMkt.get()
    global mkts
    mkts = str(mkt)
    clienteSelecionado(event)



def procurar(event):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    files = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
    
    i = 0
    
    str_Arquivos = ""
    
    for file in files:
        arquivos.insert(i, file)
        if i == 0 :
            str_Arquivos = str(file)
        else:
            str_Arquivos = str_Arquivos + "," + str(file)
        i+=1
        
    arquivo.set(str_Arquivos)
    
def verificaPadrao(dtFrame, name):
    colunas = dtFrame.columns
    num = len(colunas)
    arquivoCerto = False
    
    if 'Data' not in colunas or 'MktSource' not in colunas or 'Produto' not in colunas or 'Preço' not in colunas or 'Pricing Type' not in colunas  : #! Adicionei 'MktSource'
        tk.messagebox.showwarning('Alerta', 'O arquivo '+ name +' não está dentro dos padrões. Favor ajustar!')
        print("O arquivo "+ name +" não está dentro dos padrões e por isso não foi processado!")
        arquivoCerto = False
    else:
        arquivoCerto = True 
    
    return arquivoCerto
        

def importar(event):
    
    idCliente = comboClientes.get()
    idMktSrc = comboMkt.get()
    arq = arquivo.get()
    files = []
    global answer
    global dfglobal
    global dfArquivos
    global mkts
    if idCliente == "" :
        tk.messagebox.showwarning('Alerta', 'Favor preencher o Cliente!')
        print("Favor preencher o Cliente!")
    elif idMktSrc == "" and answer != "no" :
        tk.messagebox.showwarning('Alerta', 'Favor preencher o Market Source!')
        print("Favor preencher o Market Source!")
    elif not arq:
        tk.messagebox.showwarning('Alerta', 'Favor selecionar o arquivo!')
        print("Favor selecionar o arquivo!") 
    else:    
        if ',' in arq:
            files = arq.split(',')
        else:
            files.insert(0,arq)
        print("Cliente e Market Source validados!")
        for file in files:
            aux = pd.read_excel(file)
            padraoArquivo = verificaPadrao(aux, file)
            if padraoArquivo:
                df = aux[['Data','MktSource','Produto','Preço','Pricing Type']]
                if (answer == 'yes'):
                    df[['MktSource']] = df[['MktSource']].fillna(value=mkts)
                df = df.dropna()
                tipoArquivo = verificaTipo(df)
                print(tipoArquivo)
                if tipoArquivo:
                    dfArquivos = dfArquivos.append(df)
                    dfglobal = dfArquivos
                    geratabela(event)
                    print(dfArquivos)
    
        
def geratabela(event):
    global dfglobal
    global wrapperResult
    #df2 = pd.DataFrame(np.array([[1, 2, 3,4], [4, 5, 6,7], [7, 8, 9,10], [10,11,12,13]]),columns=['a', 'b', 'c','d'])
    df2 = dfglobal
    df2_col = df2.values.tolist()
    trv = ttk.Treeview(wrapperResult, columns =(1,2,3,4,5), show="headings",height="6")
    trv.pack()
    trv.heading(1, text="Data")
    trv.column(1,anchor ="center")
    trv.heading(2, text="MktSource")
    trv.column(2,anchor ="center")
    trv.heading(3, text="Produto")
    trv.column(3,anchor ="center")
    trv.heading(4, text="Preço")
    trv.column(4,anchor ="center")
    trv.heading(5, text="Pricing Type")
    trv.column(5,anchor ="center")

    for dados in df2_col:
        trv.insert('',tk.END,values=dados)



def verificaTipo(dataf): ##Message Box##
    c = len(dataf.index)
    arquivoCerto = True
    for k in range (0,5): #Colunas Data,MktSource,Produto,Preço,Pricing Type
        for j in range (0,c): #Linhas
            hhh = str(type(dataf.iat[j,k]))
            if(k == 0):  #data (datetime.datetime)
                if (str(type(dataf.iat[j,k])) != "<class 'datetime.datetime'>") and (str(type(dataf.iat[j,k])) != "<class 'pandas._libs.tslibs.timestamps.Timestamp'>"):
                    tk.messagebox.showwarning('Alertsa', "Existe um dado errado na coluna de Datas,Linha:"+str(j))
                    arquivoCerto = False
                    print("Existe um dado errado na coluna de Datas,Linha:"+str(j))
            if(k == 2):  #produto (str)
                if(str(type(dataf.iat[j,k])) != "<class 'str'>"): 
                    tk.messagebox.showwarning('Alerta', "Existe um dado errado na coluna de Produtos,Linha:"+str(j))
                    arquivoCerto = False
                    print("Existe um dado errado na coluna de Produtos,Linha:"+str(j))
            if(k == 3):  #preço (float64)
                if   (str(type(dataf.iat[j,k])) != "<class 'numpy.float64'>") and (str(type(dataf.iat[j,k])) != "<class 'int'>"): 
                    tk.messagebox.showwarning('Alerta', "Existe um dado errado na coluna de Preço,Linha:"+str(j))
                    arquivoCerto = False
                    print("Existe um dado errado na coluna de Preço,Linha:"+str(j))
            if(k == 4):  #pricing type (str)
                if(str(type(dataf.iat[j,k])) != "<class 'str'>"): 
                    tk.messagebox.showwarning('Alerta', "Existe um dado errado na coluna de Pricing Type,Linha:"+str(j))
                    arquivoCerto = False
                    print("Existe um dado errado na coluna de Pricing Type,Linha:"+str(j))
    return arquivoCerto

def getClientes():
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
            i = i + 1
    
    
    dfAux = pd.DataFrame(arrayAux,columns=['idCliente','nomeCliente'])
    dfAux.drop(index = dfAux.index[-1],axis=1,inplace=True) 
    dfClientes = dfClientes.append(dfAux)
    return dfClientes['nomeCliente']
        
    

##

#!Acesso aos Dados
sqlBridgeClient = CSqlBridgeClientTCP()
sqlBridgeClient.CustomBridgeServer = "13.84.148.159"

#! Parte gráfica

janela = Tk()
janela.title("Sistema Check Prices")
janela.geometry("550x600")

arquivos = []
dfArquivos = pd.DataFrame(columns = ['Data','MktSource','Produto','Preço','Pricing Type'])
dfClientes = pd.DataFrame(columns=['idCliente','nomeCliente'])
dfMktSrc = pd.DataFrame(columns=['idMktSrc','nomeMktSrc'])


clientes = getClientes()
clientesArray = clientes.values.tolist()
arquivo = StringVar()

wrapper = LabelFrame(janela, text="Informações")
wrapper.pack(pady=5, padx=5,fill="both", expand="no")

Label_Cliente = Label(wrapper, width=20,text="Selecione o Cliente:", pady = 10, padx = 10)
Label_Cliente.grid(row = 0, sticky="W")
comboClientes = ttk.Combobox(wrapper, width=40, values=clientesArray) 
comboClientes.grid(column=1, row=0, sticky="E", padx=10)
comboClientes.bind("<<ComboboxSelected>>", clienteSelecionado)
# comboExample.current(0)

Label_Mkt = Label(wrapper,width=20, text="Selecione o Market Source:", pady = 10, padx = 10)
Label_Mkt.grid(row = 1, sticky="W")
#print(mktstate)
comboMkt = ''
comboMkt = ttk.Combobox(wrapper, width=40,state = mktstate) 
comboMkt.grid(column=1, row=1, sticky="E", padx=10)
comboMkt.bind("<<ComboboxSelected>>", mktSelecionado)
#print(comboMkt)

labelArq = Label(wrapper, width=20, text="Selecione o arquivo:", pady = 10, padx = 10)
labelArq.grid(row = 2, column = 0, sticky="W")
entryArq = Entry(wrapper, width=43, textvariable=arquivo)
entryArq.grid(row = 2, column = 1, padx=10, sticky="E")

searchButton = Button(wrapper, text="Procurar", fg="black")
searchButton.grid(row=1, column = 2, sticky="E")
searchButton.bind("<Button-1>", procurar)

importButton = Button(wrapper, text="Importar", fg="black")
importButton.grid(row=2, column = 2, sticky="E")
importButton.bind("<Button-1>", importar)

wrapperResult = LabelFrame(janela, text="Resultado")
wrapperResult.pack(pady=10,padx=10,fill="both", expand="yes")

wrapperprocess = LabelFrame(janela, text = "Em Processamento")
wrapperprocess.pack(fill="both", expand = "yes" , padx=10,pady=10)


##!
#df2 = pd.DataFrame(np.array([[1, 2, 3,4], [4, 5, 6,7], [7, 8, 9,10], [10,11,12,13]]),columns=['a', 'b', 'c','d'])
#df2_col = df2.values.tolist()
#print(df2_col)
##print(df2)
#
#
#wrappertabela = LabelFrame(janela, text = "Tabela")
#wrappertabela.pack(fill="both", expand = "yes" , padx=10,pady=10)
#
#trv = ttk.Treeview(wrappertabela, columns =(1,2,3,4,5), show="headings",height="6")
#trv.pack()
#trv.heading(1, text="Data")
#trv.column(1,anchor ="center")
#trv.heading(2, text="MktSource")
#trv.column(2,anchor ="center")
#trv.heading(3, text="Produto")
#trv.column(3,anchor ="center")
#trv.heading(4, text="Preço")
#trv.column(4,anchor ="center")
#trv.heading(5, text="Pricing Type")
#trv.column(5,anchor ="center")
#
#for dados in df2_col:
#    trv.insert('',tk.END,values=dados)

##!



janela.mainloop()
