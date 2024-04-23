import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")

    sql = 'select * FROM [Stock].[dbo].[ApkaRating_day] '
    pd_TechAnalysis = pd.read_sql(sql, engine)

    sql2 = 'select * FROM [Stock].[dbo].[Ticker] '
    Ticker = pd.read_sql(sql2, engine)
    CurrDate = datetime.now().strftime("%Y-%m-%d")   
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

for i in Ticker.Stock:
    #print(i)
    sql3 = 'select * FROM [Stock].[dbo].['+i.strip()+'_AnalysHour] '
    data = pd.read_sql(sql3, engine, parse_dates=True)

    #判斷SRSI
    for j in data.data

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
