import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import apka_score_ploy
import apka_count_EMA
import apka_score_trend
import apka_score_oscillate

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")
    engine1 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/analsy?charset=GBK")
    #sql = 'select * FROM [Stock].[dbo].[ApkaRating_day] '
    #pd_TechAnalysis = pd.read_sql(sql, engine)

    sql2 = 'select top 1 * FROM [Stock].[dbo].[Ticker] '
    Ticker = pd.read_sql(sql2, engine)
    CurrDate = datetime.now().strftime("%Y-%m-%d")   
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

for i in Ticker.Stock:
    sql3 = "select  distinct [date],[open],[high],[low],[close],[colume],[fastk_d],[fastd_d],[fastk_w],[fastd_w],[fastk_m],[fastd_m],[willrd],[willrw],[willrm],\
            [MACD_d],[signal_d],[histg_d],[MACD_w],[signal_w],[histg_w],[MACD_m],[signal_m],[histg_m],[upp_d],[mid_d],[low_d],[upp_w],[mid_w],[low_w],[upp_m],[mid_m],[low_m],\
            [ema1],[ema2],[ema3],[ema4],[ema5],[ema6],[ema7],[ema8],[ema9],[ema10]\
            FROM [Stock].[dbo].[AnalysDay_"+i.strip()+"] WHere date > '2023-08-03 00:00:00.000'"
    data = pd.read_sql(sql3, engine1, parse_dates=True)
    data.columns = ["date","open","high","low","close","colume",\
                    "fastk_d","fastd_d","fastk_w","fastd_w","fastk_m","fastd_m",\
                    "willrd","willrw","willrm",\
                    "MACD_d","signal_d","histg_d","MACD_w","signal_w","histg_w","MACD_m","signal_m","histg_m",\
                    "upp_d","mid_d","low_d","upp_w","mid_w","low_w","upp_m","mid_m","low_m",\
                    "ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10"]
    data.fillna(0) 
    #data.set_index("date" , inplace=True)
    print('Ticker='+i)
    #apka_count_EMA.score_EMA(data) 
    apkaTre = apka_score_trend.score_trend(data)
    apkaTre =apkaTre.drop(columns=["buy", "sell", "profit"])
    apkaOsc = apka_score_oscillate.score_oscillate(data)
    apkEma = apka_count_EMA.score_EMA(data)
    
    #apkaOsc =apkaOsc.drop(columns=["close","sum","buy", "sell", "profit"])
    #apkaOsc.set_index('date')
    apkaCom = pd.merge( apkaTre, apkaOsc)
    apkaCom = pd.merge( apkaCom, apkEma)
    #["date", "close", "xema", "xmacd", "xsrsi", "xwillrd", "xBBand","sum", "xploy"]
    apkaCom["OscSum"] = apkaCom["xsrsi"]+apkaCom["xwillrd"]+apkaCom["xBBand"]
    #xapka.columns = ["date", "close", "xema", "xmacd", "xsrsi", "xwillrd", "xBBand","sum", "xploy"]
    #print(apkaCom.head())
    
    cmb = pd.DataFrame()
    for i in range(1,len(apkaCom)):
        xema = apkaCom.at[i,"xema"] 
        yema = apkaCom.at[i,"yema"] 
        xmacd= apkaCom.at[i,"xmacd"]
        xremark= ''
        if  yema > apkaCom.at[i-1,"yema"]:
            for  j in range(2,3):
                if apkaCom.at[i-1,"yema"] == apkaCom.at[i-j,"yema"]: 
                    xremark = '確認漲勢_K線回採GMMA_週期倍率' +  str(apkaCom.at[i,"EamCnt"] )
                    xcmb = apkaCom.at[i,"OscSum"] + apkaCom.at[i,"EamCnt"]
        elif yema < apkaCom.at[i-1,"yema"]:
            for  j in range(2,3):
                if apkaCom.at[i-1,"yema"] == apkaCom.at[i-j,"yema"]:             
                    xremark = '確認跌勢_K線反彈GMMA_週期倍率' +  str(apkaCom.at[i,"EamCnt"] )
                    xcmb = apkaCom.at[i,"OscSum"] - apkaCom.at[i,"EamCnt"]
        elif xema >0 and xmacd>0:
            #牛市修正<找買點 或牛市到頂轉空
            xcmb = apkaCom.at[i,"OscSum"]+ xmacd + xema+ yema
        elif xema >0 and xmacd<0:
            #牛市修正<找買點 或牛市到頂轉空
            if xmacd > apkaCom.at[i-1,"xmacd"]:
                xcmb = apkaCom.at[i,"OscSum"] + xema + yema
            else:
                xcmb = apkaCom.at[i,"OscSum"]
        elif xema == -2 and xmacd== -2:
            #熊市找極端反轉
            xcmb = apkaCom.at[i,"OscSum"] 
        elif xema <0 and xmacd<0:
            #熊市找賣空進場點
            xcmb = apkaCom.at[i,"OscSum"]
        else:
            #震盪沒有方向<觀望
            xcmb =apkaCom.at[i,"OscSum"]
        a = [ apkaCom.at[i,'date'], xcmb, xremark]
        cmb = pd.concat([cmb, pd.DataFrame([a])], ignore_index=True)
    cmb.columns = ["date", "xcmb","xremark"]
    #print(cmb.head())
    apkaCom = pd.merge( apkaCom, cmb)    
    


    #apkaCom.to_csv("apkaCom.csv")
    apka_score_ploy.plot(apkaCom)
    