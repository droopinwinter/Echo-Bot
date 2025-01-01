import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="127.0.0.1:1433", user='sa', password='abc123', database='analsy',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/analsy?charset=GBK")

    sql2 = 'select * FROM [Stock].[dbo].[Ticker_TW1] '
    Ticker = pd.read_sql(sql2, engine)
except Exception as errMsg: # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)



    

    '''
    print('Stock_'+i +'_AnalysDay')
    try:
        sql4 =  " Delete [Stock].[dbo]."+ i.strip()+'_AnalysDay '
        cursor.execute(sql4)
        conn.commit()
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('資料庫刪重複＿_發生錯誤-'+i.strip() , errMsg)     

    print('Stock_'+i +'_AnalysHour')
    try:

        sql4 =  " Delete [Stock].[dbo]."+ i.strip()+'_AnalysHour '
        cursor.execute(sql4)
        conn.commit()
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('資料庫刪重複＿_發生錯誤-'+i.strip() , errMsg)
    '''             
'''
for i in Ticker.Stock:
    print('Stock_'+i)
    try:
        sql4 = \
            "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER ("+\
            "	    PARTITION BY [date] ORDER BY (SELECT NULL)"+\
            "	) FROM [Stock].[dbo]."+ i.strip()+'_AnalysDay '+\
            ") AS T WHERE DupRank > 1"
 
        cursor.execute(sql4)
        conn.commit()
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('資料庫刪重複＿_發生錯誤-'+i.strip() , errMsg)     
'''
for i in Ticker.Stock:
    print('Stock_'+i)
    try:
        '''
        sql4 = \
            "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER ("+\
            "	    PARTITION BY [date] ORDER BY (SELECT NULL)"+\
            "	) FROM [analsy].[dbo].AnalysHour_"+ i.strip()+\
            ") AS T WHERE DupRank > 1"
        '''
        sql4 = \
            "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER ("+\
            "	    PARTITION BY [date] ORDER BY (SELECT NULL)"+\
            "	) FROM [analsy].[dbo].[AnalysDay_"+ i.strip() +"]"+\
            ") AS T WHERE DupRank > 1"

        sql5 = \
            "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER ("+\
            "	    PARTITION BY [date] ORDER BY (SELECT NULL)"+\
            "	) FROM [apka].[dbo].[ApkaDay_"+ i.strip() +"]"+\
            ") AS T WHERE DupRank > 1"
        
        sql6 =  " Delete [analsy].[dbo].[AnalysDay_"+ i.strip()+"] WHERE date >= '2023-12-22 00:00:00.000' "
        sql7 =  " Delete [apka].[dbo].[ApkaDay_"+ i.strip()+"] WHERE date >= '2023-12-22 00:00:00.000' "
        cursor.execute(sql7)
        cursor.execute(sql7)
        conn.commit()
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('資料庫刪重複＿_發生錯誤-'+i.strip() , errMsg)    
