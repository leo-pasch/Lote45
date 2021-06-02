# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias
import pandas as pd
import sys,clr
# import datatable as dt
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
sqlBridgeClient = CSqlBridgeClientTCP()
sqlBridgeClient.CustomBridgeServer = "13.84.148.159"
res_dt = sqlBridgeClient.ResolveQuery("SELECT * FROM Glb_Currency")

data = np.array([np.empty(8, dtype='<U100')])

i = 0

for linha in res_dt.Rows:
    idCurrency = linha["p1n_Id_Currency"]
    strCurrency = linha["n0n_Str_Currency"]
    strDescription = linha["n0y_Str_Description"]
    idHoliday = linha["f1n_Id_Holiday"]
    strCurrencyType = linha["n0n_Str_CurrencyType"]
    b1Deliverable = linha["n0n_Bl_Deliverable"]
    idInputUser = linha["f2n_Id_InputUser"]
    dtLastUpdate = linha["n0n_Dt_LastUpdate"]
    
    data = np.insert(data, i, [idCurrency,strCurrency,strDescription,idHoliday,strCurrencyType,b1Deliverable,idInputUser,dtLastUpdate], axis=0)
    i = i + 1
    

df = pd.DataFrame(data,columns=["idCurrency","strCurrency","strDescription","idHoliday","strCurrencyType","b1Deliverable","idInputUser","dtLastUpdate"])
