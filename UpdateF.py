def updatePrices (event):
    global dfglobal
    ## O Dataframe que o a Update Prices irá receber: 
    #Data Produto  Preço Pricing Type nomeMktSrc idMktSrc Preços Procurados Currency PU Real  PU Dolar  
    #PU Euro Product Class Paridade USD/BRL Paridade EUR/BRL
    o = len(dataf.index)     
    dflinhas = dfglobal.values.tolist()
    for j in range (0,o):
        preco       = dflinhas[j][2] #Preço Botado pelo cliente
        produto     = dflinhas[j][1] #Produto
        date        = dflinhas[j][1] #Data
        idMktSource = dflinhas[j][5] #idMktSrc
        
        query = "UPDATE RESPU "
        query = query + "SET n0n_Vl_PU ='"+preco+"',n0n_Vl_TradePU='"+preco+"'"
        #query = query + "	 CASE "
        #query = query + "		WHEN PRD.n0n_Str_Product  = PRD.n0n_Str_ProductNick THEN PRD.n0n_Str_ProductNick "
        #query = query + "		WHEN PRD.f1n_Id_ProductClass IN (52,50,33,704) THEN PRD.n0n_Str_ProductNick "
        #query = query + "		ELSE PRD.n0n_Str_Product "
        #query = query + "	END AS Product, "
        #query = query + "	RESPU.n0n_Vl_PU AS Price, "
        #query = query + "	RESPU.n0n_Vl_TradePU AS TradePU, "
        #query = query + "	RESPUCOMP.n0n_Vl_PU AS PUCompany, "
        #query = query + "	RESPUCOMP.f1n_Id_TradingDesk AS idTradindesk, "
        #query = query + "	CURR.n0n_Str_Currency AS Currency, "
        #query = query + "	CLASS.n0n_Str_ProductClass AS ProductClass, "
        #query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,RESPU.f2n_Id_MktSource,CURR.p1n_Id_Currency,220) AS MKTSRCPARITY, "
        #query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,0,CURR.p1n_Id_Currency,220) AS ZEROPARITY, "
        #query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,RESPU.f2n_Id_MktSource,790,220) AS MKTSRCUSDBRLPARITY, "
        #query = query + "	[LOTIS_LOTE45].[dbo].[f_GetParity](RESPU.n0n_Dt_ValDate,RESPU.f2n_Id_MktSource,220,978) AS MKTSRCEURUSDPARITY "
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
        
        try:
            sqlBridgeClient.ExecuteQuery(query)
            print("Update realizado com sucesso linha:"+str(o))
        except: 
            print("Erro durante o Update, na linha:"+str(o))