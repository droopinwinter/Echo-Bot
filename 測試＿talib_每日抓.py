import numpy as np
import pandas as pd
import talib
import time
from talib import abstract
import pymssql
from sqlalchemy import create_engine
from datetime import datetime
# 準備一份你想要計算並且併入 df 的技術指標清單


try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")

    sql = 'select * FROM [Stock].[dbo].[TechAnalysis] '
    pd_TechAnalysis = pd.read_sql(sql, engine)

    sql2 = 'select top 1 * FROM [Stock].[dbo].[Ticker] '
    Ticker = pd.read_sql(sql2, engine)
    CurrDate = datetime.now().strftime("%Y-%m-%d")   
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

for i in Ticker.Stock:
    print(i)
    sql3 = 'select * FROM [Stock].[dbo].[RowDay_'+i.strip()+'] '
    #data = pd.read_sql(sql3, engine, index_col="Date", parse_dates=True)
    data = pd.read_sql(sql3, engine, parse_dates=True)
    data.columns = ["date","open", "high", "low", "close", "adj close", "colume"]
    #data = data.astype('float')
    #print(data)
    for x in range(0,22):
        print( i , pd_TechAnalysis.at[x,"function"]+','+ pd_TechAnalysis.at[x,"parameter"].strip() +','+ pd_TechAnalysis.at[x,"RztLabel"].strip())
        rztcoul = pd_TechAnalysis.at[x,"RztLabel"].strip().split(',')
        #print(rztcoul) 
        try:
            #output = eval('abstract.STOCHRSI(data,timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=3 )')
            output = eval('abstract.'+pd_TechAnalysis.at[x,"function"].strip()+'(data, '+pd_TechAnalysis.at[x,"parameter"].strip()+' )')
            output.columns = rztcoul
            # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
            output.name = pd_TechAnalysis.at[x,"name"].lower() if type(output) == pd.core.series.Series else None
            # 透過 merge 把輸出結果併入 df DataFrame
            data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
            data = data.set_index('key_0')
        except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print('abstract發生錯誤-', pd_TechAnalysis.at[x,"name"] , errMsg)    

    try:
        #print(data)        
        #data.to_sql( i.strip()+'_AnalysDay',engine,if_exists='append', index=True)
        #data.to_sql( i.strip()+'_AnalysDay',engine,if_exists='append', index=False)
        
        data.reset_index(drop=True)
        #data.set_index('date')
        data.to_sql( i.strip()+'_AnalysDay',engine,if_exists='append', index=False)
        #data.drop("key_0", axis = 1)
        #del data['key_0']
        #data.to_csv("tech_idx.csv")
        #print(data)
    except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('回存資料庫錯誤_', i.strip() , errMsg)    
