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
import trad_record
import analsy_sql_cmd as cmd
import conn_db as db
import sys


stk_list1 = ['00642U.TW','00645.TW','00661.TW','00685L.TW','00738U.TW','00708L.TW','00640L.TW','00635U.TW','00693U.TW','00763U.TW','00683L.TW','00663L.TW','00709.TW','00660.TW','00682U.TW']
#stk_list1 = ['SVIX']

def ClearApkaDay( xTicker1):
    #SqlMaxDate = '2023-12-22'
    Arr_date = pd.read_sql(cmd.SLastDay( xTicker1), db.eng_apka)
    if len(Arr_date) >=1:
        SqlMaxDate = Arr_date.iat[0, 0].strftime("%Y-%m-%d")
    else:
        SqlMaxDate = datetime.timedelta(days = -1000)    
    #SqlMaxDate = pd.read_sql(cmd.SLastDay( xTicker1), db.eng_apka).iat[0, 0].strftime("%Y-%m-%d")
    db.cursor_apka.execute(cmd.DelLastDay( xTicker1, SqlMaxDate) )
    db.conn_apka.commit()    
    db.cursor_apka.execute(cmd.DelDupDay( xTicker1) )
    db.conn_apka.commit()
    return SqlMaxDate

try:  
    CurrDateTime = datetime.now()
    StrDate = CurrDateTime.strftime("%Y-%m-%d")
    StrTime = datetime.now().strftime("_%Y-%m-%d_%H_%M_%S")
    Bef1YerDate = CurrDateTime  - timedelta(days=365)
    Bef3Date = CurrDateTime  - timedelta(days=3)
    Str3Date = Bef3Date.strftime("%Y-%m-%d")
    print('實驗日期-時間 : ' , CurrDateTime)
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

TotTredRoc = pd.DataFrame()
cnt =0
sql_cmd = cmd.s_Stock_Ticker
Country = 'US'
if len(sys.argv) >=2:
    if sys.argv[1] == 'TW':
        sql_cmd = cmd.s_Stock_Ticker_TW
        Country = 'TW'
cmd.DelDupDay_Combin(Country)        
Ticker = pd.read_sql(sql_cmd, db.eng_Stock)
for i in Ticker.Stock:
#for i in stk_list1:
    xcode = i.strip()    
    print('apka_每日分析_'+xcode.strip())
    try:
        SqlMaxDate = ClearApkaDay(xcode)
    except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
        SqlMaxDate = Bef1YerDate.strftime("%Y-%m-%d")
    
    #
    #==========================================
    sql3 = cmd.sqlCommand( xcode.strip() ,4, Bef1YerDate)
    #==========================================
    data = pd.read_sql(sql3, db.eng_analsy, parse_dates=True)
    data.columns = ["date","open","high","low","close","colume",\
                    "fastk_d","fastd_d","fastk_w","fastd_w","fastk_m","fastd_m",\
                    "willrd","willrw","willrm",\
                    "MACD_d","signal_d","histg_d","MACD_w","signal_w","histg_w","MACD_m","signal_m","histg_m",\
                    "upp_d","mid_d","low_d","upp_w","mid_w","low_w","upp_m","mid_m","low_m",\
                    "ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10"]

    data.replace("Zero", 0)
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
    
    SingTredRoc = Trade.TotProfit(apkaCom, xcode, CurrDateTime,1)
    SingTredRoc = SingTredRoc[SingTredRoc["date"]>= "'"+SqlMaxDate+" 00:00:00.000'"]
    try:
        SingTredRoc.reset_index(drop=True)      
        SingTredRoc.to_sql( 'ApkaDay_'+xcode,db.eng_apka,if_exists='append', index=False)
        cnt = cnt+1
        SingTredRoc = SingTredRoc[SingTredRoc["date"]>= "'"+Str3Date+" 00:00:00.000'"]
        SingTredRoc.loc[SingTredRoc.close>0, "xremark"] = str(cnt).zfill(2)+'_'+ xcode
        df = SingTredRoc[['date','xremark']]
        df = df.rename(columns={'xremark': 'typ'})
        SingTredRoc = pd.merge( SingTredRoc, df)
        SingTredRoc.loc[SingTredRoc.close>0, "typ"] = Ticker.iat[cnt-1,0]  
        SingTredRoc.to_sql( 'ApkaDay_Combin_'+Country,db.eng_apka,if_exists='append', index=False)
        #print(SingTredRoc)
    except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('回存apka資料庫錯誤_', xcode , errMsg)   

    

    #apkaCom.to_csv("apkaCom.csv")
    
    #TotTredRoc = pd.concat([TotTredRoc, SingTredRoc], ignore_index=True)
    #TotTredRoc.columns = ["Ticker","LongShort","Buydate","Selldate","buyPrice","SellPrice","profit"]
    #t = datetime.now()
    #StrTime = t.strftime("_%Y-%m-%d_%H_%M_%S")
    #trad_record.DoSummsry(TotTredRoc, CurrDateTime)
    #TotTredRoc.to_sql('TradeRecord1',engine3,if_exists='append', index=False)
    #apka_score_ploy.plot(apkaCom, xcode.strip(),CurrDateTime)
    #trad_record.DoSummsry()