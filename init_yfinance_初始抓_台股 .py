import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta
import conn_db
import collect_sql_cmd
import warnings

stk_list = ['00681R.TW']
try:
    warnings.simplefilter(action="ignore", category=FutureWarning)
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(collect_sql_cmd.s_Stock_Ticker_TW, conn_db.eng_Stock)
    for i in stk_list:    
    #for i in pd_read_sql.Stock:
        yTicker = i.strip()
        print('Stock_'+yTicker)
        #小時K
        #日K
        yf.download(yTicker,period='5y',interval='1d').to_sql( 'RowDay_'+yTicker,conn_db.eng_Stock,if_exists='append', index=True)
        #stock = yf.Ticker(yTicker)
        #stock.history(period = 'max').to_sql( 'RowDay_'+yTicker,conn_db.eng_Stock,if_exists='append', index=True)                            
        '''
        #週K
        '''
        time.sleep(5)   
    #print(pd_read_sql.kdatetime)
    '''
    stock = yf.Ticker('^IXIC')
    yf.download('^SPX',period='1d',interval='90m').to_sql('test_table',engine,if_exists='append', index=True)
    '''  
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)
