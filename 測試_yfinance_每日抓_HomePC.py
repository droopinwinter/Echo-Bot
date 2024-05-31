import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.168.244.8:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.168.244.8:1433/Stock?charset=GBK")

    sql2 = "select * FROM [Stock].[dbo].[Ticker] WHERE STOCK = 'SPXL' "
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(sql2, engine)
    for i in pd_read_sql.Stock:
        print('Stock_'+i)
        #yf.download(i,period='2y',interval='1h').to_csv('RowHr_'+i.strip()+'.csv')#to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        #小時K
        sql3 = 'select top 1 max(Datetime) Date FROM [Stock].[dbo].[RowHour_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowHour_"+i.strip()+"] Where Datetime >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        #rzt = yf.download(i,start = SqlMaxDate.iat[0, 0].strftime("%Y-%m-%d"), end=CurrDate.strftime("%Y-%m-%d"),interval='1h')
        #print(rzt)
        yf.download(i,start = SqlMaxDate, end=CurrDate,interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        #日K
        sql3 = 'select top 1 max(Date) Date FROM [Stock].[dbo].[RowDay_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowDay_"+i.strip()+"] Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        yf.download(i,start = SqlMaxDate, end=CurrDate,interval='1d').to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)        
        #週K
        sql3 = 'select top 1 max(Date) Date FROM [Stock].[dbo].[RowWeek_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowWeek_"+i.strip()+"] Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        yf.download(i,start = SqlMaxDate, end=CurrDate,interval='1wk').to_sql( 'RowWeek_'+i.strip(),engine,if_exists='append', index=True)        

        '''
        #初始下載歷史資料
        yf.download(i,period='1d',interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5) 
        yf.download(i,period='1d',interval='1d').to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5)
        if datetime.now().isoweekday() == 5: 
            yf.download(i,period='1wk',interval='1wk').to_sql( 'RowWeek_'+i.strip(),engine,if_exists='append', index=True)#to_csv('RowWeek_'+i.strip()+'.csv')#

        '''
        time.sleep(5)   
    #print(pd_read_sql.kdatetime)
    '''
    stock = yf.Ticker('^IXIC')
    yf.download('^SPX',period='1d',interval='90m').to_sql('test_table',engine,if_exists='append', index=True)

    '''
 
  
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)


