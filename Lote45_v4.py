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
from tkinter import messagebox

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
##
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
            
    else:
        tk.messagebox.showinfo(title = "Informe", message="Está sendo usado como Market Source: "+str(mkts))
    
    dfAux = pd.DataFrame(arrayAux,columns=['idMktSrc','nomeMktSrc'])
    dfMktSrc = dfMktSrc.append(dfAux)
    auxMkt = dfMktSrc["nomeMktSrc"]
    auxMkt.drop(index = auxMkt.index[-1],axis=1,inplace=True)    
    auxMktArray = auxMkt.values.tolist()
    comboMkt["values"] = auxMktArray

##
def mktSelecionado(event):
    mkt = comboMkt.get()
    global mkts
    mkts = str(mkt)
    clienteSelecionado(event)

##
#def upPrices (dataf)


def getPrices(produto, date, idMktSource):
    query = "SELECT "
    query = query + "	 CASE "
    query = query + "		WHEN PRD.n0n_Str_Product  = PRD.n0n_Str_ProductNick THEN PRD.n0n_Str_ProductNick "
    query = query + "		WHEN PRD.f1n_Id_ProductClass IN (52,50,33,704) THEN PRD.n0n_Str_ProductNick "
    query = query + "		ELSE PRD.n0n_Str_Product "
    query = query + "	END AS Product, "
    query = query + "	RESPU.n0n_Vl_PU AS Price, "
    query = query + "	RESPU.n0n_Vl_TradePU AS TradePU, "
    query = query + "	RESPUCOMP.n0n_Vl_PU AS PUCompany, "
    query = query + "	RESPUCOMP.f1n_Id_TradingDesk AS idTradindesk, "
    query = query + "	CURR.n0n_Str_Currency AS Currency, "
    query = query + "	CLASS.n0n_Str_ProductClass AS ProductClass, "
    query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,RESPU.f2n_Id_MktSource,CURR.p1n_Id_Currency,220) AS MKTSRCPARITY, "
    query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,0,CURR.p1n_Id_Currency,220) AS ZEROPARITY, "
    query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,RESPU.f2n_Id_MktSource,790,220) AS MKTSRCUSDBRLPARITY, "
    query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,RESPU.f2n_Id_MktSource,220,978) AS MKTSRCEURUSDPARITY "
    query = query + "FROM [LOTIS_RESMASTER].[dbo].[Res_PUProduct] RESPU (NOLOCK) "
    query = query + "INNER JOIN [LOTIS_RESMASTER].[dbo].[Res_PUCompanyProduct] RESPUCOMP (NOLOCK) "
    query = query + "	ON RESPU.n0n_Str_Product = RESPUCOMP.n0n_Str_Product "
    query = query + "	AND RESPU.n0n_Dt_ValDate = RESPUCOMP.n0n_Dt_ValDate "
    query = query + "	AND  RESPU.f2n_Id_MktSource = RESPUCOMP.f3n_Id_MktSource " 
    query = query + "INNER JOIN [APM].[dbo].[Prd_Products] PRD (NOLOCK) "
    query = query + "	ON RESPU.n0n_Str_Product = PRD.n0n_Str_Product "
    query = query + "	AND (PRD.n0n_Str_Product = '"+produto+"' OR  PRD.n0n_Str_ProductNick ='"+produto+"' ) " 
    query = query + "INNER JOIN [APM].[dbo].[Prd_ProductClass] CLASS (NOLOCK) "
    query = query + "	ON CLASS.p1n_Id_ProductClass = PRD.f1n_Id_ProductClass " 
    query = query + "INNER JOIN [GLOBAL].[dbo].[Glb_Currency] AS CURR (NOLOCK) "
    query = query + "	ON PRD.f3n_Id_ProductCurrency = CURR.p1n_Id_Currency "
    query = query + "WHERE RESPU.n0n_Dt_ValDate = '"+date+"' AND RESPU.f2n_Id_MktSource = "+str(idMktSource)

    Precos = []
    dtPrices = sqlBridgeClient.ResolveQuery(query)
    i = 0
    
    for linha in dtPrices.Rows:
        preco = linha['Price']
        curr = linha['Currency']          #Tipo de Moeda
        usd = linha['MKTSRCUSDBRLPARITY'] #MKTSRCUSDBRLPARITY -- Preço da paridade USD / BRL
        eur = linha['MKTSRCEURUSDPARITY'] #Dolar/Euro
        pclass = linha['ProductClass']    #Product Class
        zero = linha['ZEROPARITY']    #Paridade Zero
        mktpar = linha['MKTSRCPARITY']    #Paridade Zero
        
        Precos.append((preco,curr,usd,eur,pclass,zero,mktpar))
        
    return Precos

##
def  addPrice(event):
    global dfglobal
    o = len(dfglobal.index)
    for z in range(0,o):
        print(dfglobal)
        dfglobal.iat[z,1].lstrip()
        dfglobal.iat[z,3].lstrip()
        
        data  = str(dfglobal.iat[z,0])
        idmkt = str(int(dfglobal.iat[z,5]))
        prod  = str(dfglobal.iat[z,1])
        try:
            prec = getPrices(prod,data,idmkt)
            
            dfglobal.iat[z,6] = prec[0][0] #Preço Procurado
            dfglobal.iat[z,7] = prec[0][1] #Moeda
            dfglobal.iat[z,11] = prec[0][4] #Product Class
            dfglobal.iat[z,12] = prec[0][2] #Paridade USD/BRL
            dfglobal.iat[z,13] = prec[0][2]*prec[0][3] #Paridade EUR/BRL
            if prec[0][1] == 'BRL': #Se o Preço for em Real
                dfglobal.iat[z,8] = float(prec[0][0]) #Preço em Real
                
                dfglobal.iat[z,9] = float((prec[0][0])) / float((prec[0][2])) #Preço em Dolar
                
                dfglobal.iat[z,10] = float((prec[0][0])) / (float((prec[0][2])) * float((prec[0][3]))) #Preço em Euro
                
            if prec[0][1] == 'USD': # Se o preço for em Dolar
                dfglobal.iat[z,9] = float(prec[0][0]) #Preço em Dolar
                
                dfglobal.iat[z,8] = float((prec[0][0])) * float((prec[0][2])) #Preço em Real
                
                dfglobal.iat[z,10] = float((prec[0][0])) / float((prec[0][3])) #Preço em Euro
                
                
                
                
                
            if prec[0][1] == 'EUR': # Se o preço for em Dolar
                dfglobal.iat[z,10] = float(prec[0][0]) #Preço em Euro
                
                dfglobal.iat[z,9] = float((prec[0][0])) * float((prec[0][3])) #Preço em Dolar
                
                dfglobal.iat[z,8] = float((prec[0][0])) * (float((prec[0][3]))*float((prec[0][2]))) #Preço em Dolar
                
                
        except:
            dfglobal.iat[z,6] = ""
            dfglobal.iat[z,7] = ""
            dfglobal.iat[z,8] = ""
            dfglobal.iat[z,9] = ""
            dfglobal.iat[z,10] = ""
            dfglobal.iat[z,11] = ""
            
    dfglobal['Data'] = dfglobal['Data'].dt.strftime('%Y-%m-%d')
    geratabela(event)





##
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
##   
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
        
##
def importar(event):
    
    idCliente = comboClientes.get()
    idMktSrc = comboMkt.get()
    arq = arquivo.get()
    files = []
    global answer
    global dfglobal
    global dfArquivos
    global mkts
    global dfMktSrc
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
                aux = aux.rename(columns={'MktSource': 'nomeMktSrc'})
                df = aux[['Data','nomeMktSrc','Produto','Preço','Pricing Type']]
                
                if (answer == 'yes'):
                    df[['nomeMktSrc']] = df[['nomeMktSrc']].fillna(value=mkts)
                df = df.dropna()

                tipoArquivo = verificaTipo(df)
                if tipoArquivo:
                    dfArquivos = dfArquivos.append(df)     #Tabela sem preço

                    dfglobal = pd.merge(dfArquivos,dfMktSrc,on = 'nomeMktSrc',how = 'left') #Tabela que vai ter preço
                    dfglobal["Preços Procurados"] = ""
                    dfglobal["Currency"] = ""
                    dfglobal["PU Real"] = ""
                    dfglobal["PU Dolar"] = ""
                    dfglobal["PU Euro"] = ""
                    dfglobal["Product Class"] = ""
                    dfglobal["Paridade USD/BRL"] = ""
                    dfglobal["Paridade EUR/BRL"] = ""
                    del dfglobal["MktSource"]
                    addPrice(event)


##        
def geratabela(event):
    global dfglobal
    global wrapperResult
    global l
    print("======= DF Global ======")
    print(dfglobal)
    df2 = dfglobal
    df2_col = df2.values.tolist()
    print(df2_col[0][0])
    print(df2_col[0][1])
    trv = ttk.Treeview(wrapperResult, columns =(1,2,3,4,5,6,7,8,9,10,11,12,13,14), show="headings",height="6")
    trv.pack()
    trv.heading(1, text="Data")
    trv.column(1,anchor ="center")
    trv.heading(2, text="Produto")
    trv.column(2,anchor ="center",minwidth = 60)
    trv.heading(3, text="Preço")
    trv.column(3,anchor ="center",minwidth = 50)
    trv.heading(4, text="Pricing Type")
    trv.column(4,anchor ="center",minwidth = 100)
    trv.heading(5, text="nomeMktSrc")
    trv.column(5,anchor ="center",minwidth = 150)
    trv.heading(6, text="idMktSrc")
    trv.column(6,anchor ="center",minwidth = 60)
    trv.heading(7, text="Preços Procurados")
    trv.column(7,anchor ="center",minwidth = 100,width = 100)
    
    trv.heading(8, text="Moeda")
    trv.column(8,anchor ="center",minwidth = 100,width = 100)
    trv.heading(9, text="PU Real")
    trv.column(9,anchor ="center",minwidth = 100,width = 100)
    trv.heading(10, text="PU Dolar")
    trv.column(10,anchor ="center",minwidth = 100,width = 100)
    trv.heading(11, text="PU Euro")
    trv.column(11,anchor ="center",minwidth = 100,width = 100)
    trv.heading(12, text="Product Class")
    trv.column(12,anchor ="center",minwidth = 100,width = 100)
    
    
    trv.heading(13, text="Paridade USD/BRL")
    trv.column(13,anchor ="center",minwidth = 100,width = 100)
    trv.heading(14, text="Paridade EUR/BRL")
    trv.column(14,anchor ="center",minwidth = 100,width = 100)
    
    trv.tag_configure('bgg', background='#aafa84') #verde
    trv.tag_configure('bgr', background='#fa8e7d') #vermelho

    for dados in df2_col:
        if (dados[2]==dados[8]) or (dados[2]==dados[9]) or (dados[2]==dados[10]):
            trv.insert('',tk.END,values=dados,tags=('bgg'))
        else:
            trv.insert('',tk.END,values=dados,tags=('bgr'))

##
l = locals()
##

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
##
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
w = janela.winfo_screenwidth()
h = janela.winfo_screenheight()
janela.geometry("%dx%d" % (w,h)) #Antes era 800x600
#janela.attributes('-fullscreen',True)

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

comboMkt = ''
comboMkt = ttk.Combobox(wrapper, width=40,state = mktstate) 
comboMkt.grid(column=1, row=1, sticky="E", padx=10)
comboMkt.bind("<<ComboboxSelected>>", mktSelecionado)


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

##!


janela.mainloop()
