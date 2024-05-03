import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import apka_score_ploy

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
    #data.set_index("date" , inplace=True)
    print('Ticker='+i)
    xapka = pd.DataFrame()
    for j in range(10,len(data)):
    #for j in range(600,800):
        try:
            #print(data.at[j, 'ema1'])#print("Date" ,str(data.at[j,'date']))          
            #利用EMA和MACD判斷長週期上升趨勢做多或空
            if   data.at[j, 'ema1'] > data.at[j, 'ema2']  :
                xema =1 
                if data.at[j-1, 'ema1'] < data.at[j-1, 'ema2'] or data.at[j, 'ema2'] > data.at[j, 'ema3']:
                    xema =2 
            elif data.at[j, 'ema1'] < data.at[j, 'ema2'] :
                xema =-1 
                if data.at[j-1, 'ema1'] > data.at[j-1, 'ema2'] or data.at[j, 'ema2'] < data.at[j, 'ema3']:
                    xema =-2 
            else:
                xema = 0 #無法識別走勢<持倉或觀望不操作


                    
            #短線判斷進出場信號
            if data.at[j, 'MACD_d'] > data.at[j, 'signal_d']:
                xmacd =1
                if (data.at[j-1, 'MACD_d'] < data.at[j-1, 'signal_d'] and data.at[j, 'signal_d'] >0) or ( (data.at[j, 'histg_d'] -  data.at[j-2, 'histg_d']) >0):
                    xmacd =2                        
            elif data.at[j, 'MACD_d'] < data.at[j, 'signal_d'] :
                xmacd =-1
                if (data.at[j-1, 'MACD_d'] > data.at[j-1, 'signal_d'] and data.at[j, 'signal_d'] <0) or ( (data.at[j, 'histg_d'] -  data.at[j-2, 'histg_d']) <0):
                    xmacd =-2
            else:
                xmacd =0

            if data.at[j, 'fastk_d'] > data.at[j, 'fastd_d'] and data.at[j-1, 'fastk_d'] < data.at[j-1, 'fastd_d'] and data.at[j, 'fastd_d'] < 20 :
                xsrsi = 1
                for k in range(j-10,j): 
                    if  data.at[k, 'fastk_w'] > data.at[k, 'fastd_w'] and data.at[k-1, 'fastk_w'] < data.at[k-1, 'fastd_w'] and  data.at[k, 'fastd_w'] < 20 :
                        xsrsi = 2
            elif data.at[j, 'fastk_d'] < data.at[j, 'fastd_d'] and data.at[j-1, 'fastk_d'] > data.at[j-1, 'fastd_d'] and data.at[j, 'fastd_d'] > 80 :
                xsrsi = -1
                for k in range(j-10,j): 
                    if data.at[k, 'fastk_w'] < data.at[k, 'fastd_w'] and data.at[k-1, 'fastk_w'] > data.at[k-1, 'fastd_w'] and  data.at[k, 'fastd_w'] > 20 :
                        xsrsi = -2
            else:
                xsrsi = 0  

            if data.at[j, 'willrd'] < -95 : 
                xwillrd = 1
                if data.at[j, 'willrd'] > data.at[j-1, 'willrd'] and data.at[j, 'close'] < data.at[j-1, 'close']:
                    xwillrd = 2
            elif data.at[j, 'willrd'] > -5 :
                xwillrd = -1
                if  data.at[j, 'willrd'] < data.at[j-1, 'willrd'] and data.at[j, 'close'] > data.at[j-1, 'close']:
                    xwillrd = -2
            else:
                xwillrd = 0

            if  data.at[j-1, 'low'] < data.at[j-1, 'low_d'] and data.at[j, 'close'] > data.at[j, 'low_d']: 
                xBBand = 1
                if data.at[j, 'low'] > data.at[j, 'low_d']:
                    xBBand = 2   
            if  data.at[j-1, 'high'] > data.at[j-1, 'upp_d'] and data.at[j-1, 'close'] < data.at[j-1, 'upp_d']: 
                xBBand = -1
                if data.at[j, 'low'] > data.at[j, 'low_d']:
                     xBBand = -2
            else:
                xBBand = 0
            '''
            if (xema>0 and xmacd>0) and ( xwillrd ==2 or  xsrsi ==2): #上升趨勢找修正低點做多
                xsum = -(xema+ xmacd+ xsrsi + xwillrd+ xBBand)
                xploy = '上漲至極端走勢改作空'               
            elif (xema<0 and xmacd<0) and ( xwillrd ==-2 or  xsrsi ==-2): #下降趨勢找高點做空
                xsum = -(xsrsi+ xwillrd+ xBBand +xema+ xmacd)
                xploy = '下跌至極端走勢改作多'

            '''

            if (xema>0 and xmacd>0) and ( xwillrd ==2 or  xsrsi ==2): #上升趨勢找修正低點做多
                xsum = xema+ xmacd- xsrsi - xwillrd+ xBBand
                xploy = '上漲回調至價值區間'               
            elif (xema<0 and xmacd<0) and ( xwillrd ==-2 or  xsrsi ==-2): #下降趨勢找高點做空
                xsum = xsrsi+ xwillrd+ xBBand -xema- xmacd
                xploy = '下跌反彈過價值區間'                
            elif (xema>0 and xmacd<0) :
                xsum = xsrsi+ xwillrd+ xBBand +xema- xmacd
                xploy = '上漲中回到震盪區間'
            elif (xema<0 and xmacd>0) :
                xsum = xsrsi+ xwillrd+ xBBand +xema - xmacd            
                xploy = '下跌中回到震盪區間'
            else:
                xsum = xema+ xmacd+ xsrsi+ xwillrd+ xBBand
                xploy = '不確定'
               
            
            '''
            if data.at[j, 'high'] > data.at[j, 'upp_d'] and data.at[j, 'close'] < data.at[j-1, 'upp_d'] :
                xBBand = -1
                for k in range(j-5,j): 
                        #data.at[j,"fastk_d"]
                    if data.at[k, 'fastk_d'] > data.at[k, 'fastd_d'] and data.at[k, 'fastd_d'] > 80 :
                        xBBand = -2                
            elif data.at[j, 'low'] < data.at[j, 'low_d'] and data.at[j, 'close'] > data.at[j-1, 'low_d'] : 
                xBBand = 1
                for k in range(j-5,j): 
                    if data.at[k, 'fastk_d'] < data.at[k, 'fastd_d'] and data.at[k, 'fastd_d'] < 20 :
                        xBBand = 2                 
            else:
                xBBand = 0         
            '''
            a=[ data.at[j,'date'],data.at[j,'close'], xema, xmacd, xsrsi, xwillrd, xBBand, xsum, xploy]
            #xapka = xapka.append(a,ignore_index=True)
            #print(xema, xmacd, xsrsi, xwillrd, xBBand)
            xapka = pd.concat([xapka, pd.DataFrame([a])], ignore_index=True)
        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)    


    apka_score_ploy.plot(xapka)

#print(xapka)
#xapka.to_csv("ApkaSPY.CSV")
'''
"date","Ticker","strategy","STOCHRSI","MACD","WILLR","BBANDS","EMA","pattern","total","LongOrShort","current","support","pressure","profit","loss","PLratio","remark"
'''

        

'''
    try:
        #print(data)        
        #data.to_sql( i.strip()+'_AnalysDay',engine,if_exists='append', index=True)
        #data.to_sql( i.strip()+'_AnalysDay',engine,if_exists='append', index=False)
        
        data.reset_index(drop=True)
        #data.set_index('date')
        data.to_sql( i.strip()+'_AnalysHour',engine,if_exists='append', index=False)
        #data.drop("key_0", axis = 1)
        #del data['key_0']
        #data.to_csv("tech_idx.csv")
        #print(data)
    except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('回存資料庫錯誤_', i.strip() , errMsg)    

'''
