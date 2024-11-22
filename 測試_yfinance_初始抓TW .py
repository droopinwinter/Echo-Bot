import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

stk_list = [
 '0050.TW'
]

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="127.0.0.1:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/Stock?charset=GBK")

    sql2 = 'select * FROM [Stock].[dbo].[Ticker_TW] '
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(sql2, engine)
    #print(pd_read_sql.kdatetime)
    for i in pd_read_sql.Stock:
        print('Stock_'+i)
        #初始下載歷史資料
        #yf.download(i,period='1d',interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        #time.sleep(5) 
        #yf.download(i.strip()+'.TW',period='max',interval='1d').to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        yf.download(i.strip()+'.TW',period='1y',interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        #yf.download(i.strip()+'.TW',period='max',interval='1wk').to_sql( 'RowWeek_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5)  


    '''
    for i in stk_list:
        print('Stock_'+i)
        stock = yf.Ticker('0050.TW')
        yf.download('0050.TW',period='max',interval='1d').to_sql('RowHour_0050',engine,if_exists='append', index=True)
        
        #初始下載歷史資料
        #yf.download(i,period='1d',interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        #time.sleep(5) 
        yf.download('',period='1y',interval='1d').to_csv('Hprice_IXIC.csv') #to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5)

        
        time.sleep(5)   



    '''
 
  
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)


