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

def ClearAnalysHour( xTicker1):               
    SqlMaxDate = pd.read_sql(collect_sql_cmd.SLastHour(yTicker), conn_db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
    conn_db.cur_Stock.execute( collect_sql_cmd.DelLastHour(yTicker, SqlMaxDate) )
    conn_db.con_Stock.commit()
    conn_db.cur_Stock.execute( collect_sql_cmd.DelDupHour(yTicker) )
    conn_db.con_Stock.commit() 


def ClearAnalysDay( xTicker1):                       
    SqlMaxDate = pd.read_sql(collect_sql_cmd.SLastDay(yTicker), conn_db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
    conn_db.cur_Stock.execute( collect_sql_cmd.DelLastDay(yTicker, SqlMaxDate) )
    conn_db.con_Stock.commit()
    conn_db.cur_Stock.execute( collect_sql_cmd.DelDupDay(yTicker) )
    conn_db.con_Stock.commit()     

try:
    warnings.simplefilter(action="ignore", category=FutureWarning)
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(collect_sql_cmd.s_Stock_Ticker, conn_db.eng_Stock)
    for i in pd_read_sql.Stock:
        print('Stock_'+i)
        yTicker = i.strip()
        #yf.download(i,period='2y',interval='1h').to_csv('RowHr_'+i.strip()+'.csv')#to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        #小時K
        '''
        conn_db.cur_Stock.execute( collect_sql_cmd.DelDupHour(yTicker) )
        conn_db.con_Stock.commit()                
        SqlMaxDate = pd.read_sql(collect_sql_cmd.SLastHour(yTicker), conn_db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
        conn_db.cur_Stock.execute( collect_sql_cmd.DelLastHour(yTicker, SqlMaxDate) )
        conn_db.con_Stock.commit()
        yf.download(yTicker,start = SqlMaxDate, end=CurrDate,interval='1h').to_sql( 'RowHour_'+yTicker,conn_db.eng_Stock,if_exists='append', index=True)
        '''
        #日K
        conn_db.cur_Stock.execute( collect_sql_cmd.DelDupDay(yTicker) )
        conn_db.con_Stock.commit()                        
        SqlMaxDate = pd.read_sql(collect_sql_cmd.SLastDay(yTicker), conn_db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
        conn_db.cur_Stock.execute( collect_sql_cmd.DelLastDay(yTicker, SqlMaxDate) )
        conn_db.con_Stock.commit()
        yf.download(yTicker,start = SqlMaxDate, end=CurrDate,interval='1d').to_sql( 'RowDay_'+yTicker,conn_db.eng_Stock,if_exists='append', index=True)        

        

        '''
        #週K
        SqlMaxDate = pd.read_sql(collect_sql_cmd.SLastWeek(yTicker), conn_db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
        conn_db.cur_Stock.execute( collect_sql_cmd.DelLastWeek(yTicker, SqlMaxDate) )
        conn_db.con_Stock.commit()
        yf.download(yTicker,start = SqlMaxDate, end=CurrDate,interval='1wk').to_sql( 'RowWeek_'+yTicker,conn_db.eng_Stock,if_exists='append', index=True)        


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


