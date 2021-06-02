# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias
from tkinter import Tk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pandas as pd


def clienteSelecionado(event):
    auxcl = comboClientes.get()
    cl = int(auxcl)
    auxdf = pd.read_excel('C:\\Users\\FernandaBraga\\OneDrive - Bridge & Co\\TestePythonCombobox.xlsx')
    auxdf = auxdf[auxdf["Cliente"]==cl]
    auxMkt = auxdf["MktSrc"]
    auxMkt = auxMkt.drop_duplicates()
    auxMktArray = auxMkt.values.tolist()
    comboMkt["values"] = auxMktArray

def mktSelecionado(event):
    mkt = comboMkt.get()


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
    
    if 'Data' not in colunas or 'Produto' not in colunas or 'Preço' not in colunas or 'Pricing Type' not in colunas  :
        messagebox.showwarning('ALerta', 'O arquivo '+ name +' não está dentro dos padrões. Favor ajustar!')
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
    
    if idCliente == "" :
        messagebox.showwarning('ALerta', 'Favor preencher o Cliente!')
        print("Favor preencher o Cliente!")
    elif idMktSrc == "":
        messagebox.showwarning('ALerta', 'Favor preencher o Market Source!')
        print("Favor preencher o Market Source!")
    elif not arq:
        messagebox.showwarning('ALerta', 'Favor selecionar o arquivo!')
        print("Favor selecionar o arquivo!") 
    else:    
        if ',' in arq:
            files = arq.split(',')
        else:
            files.insert(0,arq)
        print("CLiente e Market Source validados!")
        for file in files:
            aux = pd.read_excel(file)
            padraoArquivo = verificaPadrao(aux, file)
            if padraoArquivo:
                df = aux[['Data','Produto','Preço','Pricing Type']]
                df = df.dropna()
                print(df.head())


janela = Tk()
janela.title("Sistema Check Prices")
janela.geometry("550x600")

arquivos = []

dt_teste = pd.read_excel('C:\\Users\\FernandaBraga\\OneDrive - Bridge & Co\\TestePythonCombobox.xlsx')
clientes = dt_teste["Cliente"]
clientes = clientes.drop_duplicates()
clientesArray = clientes.values.tolist()

mkt_src = dt_teste["MktSrc"]
mkt_src = mkt_src.drop_duplicates()
mkt_srcArray = mkt_src.values.tolist()

arquivo = StringVar()

wrapper = LabelFrame(janela, text="Informações")
wrapper.pack(pady=10, padx=10,fill="both", expand="yes")

Label_Cliente = Label(wrapper, width=20,text="Selecione o Cliente:", pady = 10, padx = 10)
Label_Cliente.grid(row = 0, sticky="W")
comboClientes = ttk.Combobox(wrapper, width=40, values=clientesArray) 
comboClientes.grid(column=1, row=0, sticky="E", padx=10)
comboClientes.bind("<<ComboboxSelected>>", clienteSelecionado)
# comboExample.current(0)

Label_Mkt = Label(wrapper,width=20, text="Selecione o Market Source:", pady = 10, padx = 10)
Label_Mkt.grid(row = 1, sticky="W")
comboMkt = ttk.Combobox(wrapper, width=40) 
comboMkt.grid(column=1, row=1, sticky="E", padx=10)
comboMkt.bind("<<ComboboxSelected>>", mktSelecionado)

labelArq = Label(wrapper, width=20, text="Selecione o arquivo:", pady = 10, padx = 10)
labelArq.grid(row = 2, column = 0, sticky="W")
entryArq = Entry(wrapper, width=43, textvariable=arquivo)
entryArq.grid(row = 2, column = 1, padx=10, sticky="E")

searchButton = Button(wrapper, text="Procurar", fg="black")
searchButton.grid(row=2, column = 2, sticky="E")
searchButton.bind("<Button-1>", procurar)

importButton = Button(wrapper, text="Importar", fg="black")
importButton.grid(column = 2, pady = 10)
importButton.bind("<Button-1>", importar)

wrapperResult = LabelFrame(janela, text="Resultado")
wrapperResult.pack(pady=10,padx=10,fill="both", expand="yes")




janela.mainloop()



    