import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

stk_list = [
 '^SPX','^IXIC'
]

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")

    sql2 = 'select * FROM [Stock].[dbo].[Ticker] '
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(sql2, engine)
    for i in stk_list:
        print('Stock_'+i)

        
        #初始下載歷史資料
        yf.download(i,period='1d',interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5) 
        yf.download(i,period='1d',interval='1d').to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5)

        
        time.sleep(5)   
    #print(pd_read_sql.kdatetime)
    '''
    stock = yf.Ticker('^IXIC')
    yf.download('^SPX',period='1d',interval='90m').to_sql('test_table',engine,if_exists='append', index=True)

    '''
 
  
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)


