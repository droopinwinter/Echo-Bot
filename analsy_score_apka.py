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
import analsy_score_xcom
import Trade

def sqlCommand( xcode, kind):
        #between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000'
    # > '2021-05-03 00:00:00.000'

    BaseSql = "select  distinct [date],[open],[high],[low],[close],[colume],[fastk_d],[fastd_d],[fastk_w],[fastd_w],[fastk_m],[fastd_m],[willrd],[willrw],[willrm],\
            [MACD_d],[signal_d],[histg_d],[MACD_w],[signal_w],[histg_w],[MACD_m],[signal_m],[histg_m],[upp_d],[mid_d],[low_d],[upp_w],[mid_w],[low_w],[upp_m],[mid_m],[low_m],\
            [ema1],[ema2],[ema3],[ema4],[ema5],[ema6],[ema7],[ema8],[ema9],[ema10]\
            FROM [analsy].[dbo]."
    if   kind ==1:
        sql = BaseSql +"[AnalysDay_"+xcode+"] " #between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' "
    elif kind ==2:
        sql = BaseSql +"[AnalysHour_3_"+xcode+"] WHere date > '2024-02-03 00:00:00.000'" 
    else:
        sql = "select  distinct [date],[open],[high],[low],[close],[colume],[fastk_d],[fastd_d],[fastk_w],[fastd_w],[fastk_m],[fastd_m],[willrd],[willrw],[willrm],\
                [MACD_d],[signal_d],[histg_d],[MACD_w],[signal_w],[histg_w],[MACD_m],[signal_m],[histg_m],[upp_d],[mid_d],[low_d],[upp_w],[mid_w],[low_w],[upp_m],[mid_m],[low_m],\
                [ema1],[ema2],[ema3],[ema4],[ema5],[ema6],[ema7],[ema8],[ema9],[ema10]\
                FROM [analsy].[dbo].[AnalysDay_"+xcode+"] WHere date between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' "        
    return sql

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")
    engine1 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/analsy?charset=GBK")
    engine2 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/apka?charset=GBK")
    engine3 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/trade?charset=GBK")
    #sql = 'select * FROM [Stock].[dbo].[ApkaRating_day] '
    #pd_TechAnalysis = pd.read_sql(sql, engine)

    sql2 = 'select top 1 * FROM [Stock].[dbo].[Ticker] '
    Ticker = pd.read_sql(sql2, engine)
    CurrDate = datetime.now().strftime("%Y-%m-%d")   
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

TotTredRoc = pd.DataFrame()
for xcode in Ticker.Stock:
    sql3 = sqlCommand( xcode.strip() ,1)

    data = pd.read_sql(sql3, engine1, parse_dates=True)
    data.columns = ["date","open","high","low","close","colume",\
                    "fastk_d","fastd_d","fastk_w","fastd_w","fastk_m","fastd_m",\
                    "willrd","willrw","willrm",\
                    "MACD_d","signal_d","histg_d","MACD_w","signal_w","histg_w","MACD_m","signal_m","histg_m",\
                    "upp_d","mid_d","low_d","upp_w","mid_w","low_w","upp_m","mid_m","low_m",\
                    "ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10"]
    data.fillna(0) 
    #data.set_index("date" , inplace=True)
    #print('Ticker='+xcode)
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
    #print(apkaCom.tail(5))
    
    #print(cmb.head())
    cmb = analsy_score_xcom.score_xcom(apkaCom)
    apkaCom = pd.merge( apkaCom, cmb)    
    
    apkaCom.to_sql('Apka_'+xcode.strip(),engine2,if_exists='append', index=False)
    '''
    try:
        engine2 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/apka?charset=GBK")
        apkaCom.reset_index(drop=True)      
        apkaCom.to_sql( 'apka_'+xcode.strip(),engine2,if_exists='append', index=False)
    except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('回存apka資料庫錯誤_', i.strip() , errMsg)   

    '''
    #SingTredRoc = Trade.TotProfit(apkaCom, xcode.strip())
    #apkaCom.to_csv("apkaCom.csv")
    #apka_score_ploy.plot(apkaCom, xcode.strip())
    #TotTredRoc = pd.concat([TotTredRoc, SingTredRoc], ignore_index=True)
#TotTredRoc.columns = ["Ticker","LongShort","Buydate","Selldate","buyPrice","SellPrice","profit"]
#t = datetime.now()
#StrTime = t.strftime("_%Y-%m-%d_%H_%M_%S")
#TotTredRoc.to_csv(   '..\\tradeRecord\\TotTredRoc'+StrTime+'.csv')   
#TotTredRoc.to_sql('TradeRecord_'+xcode.strip(),engine3,if_exists='append', index=False)