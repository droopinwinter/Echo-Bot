import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta
import conn_db as db
import collect_sql_cmd as cmd
import warnings
import sys

def ClearAnalysHour( xTicker1):               
    Arr_date = pd.read_sql(cmd.SLastHour(yTicker), db.eng_Stock)
    if len(Arr_date) >=1 :
        SqlMaxDate = Arr_date.iat[0, 0].strftime("%Y-%m-%d")
    else:
        SqlMaxDate = datetime.timedelta(days = -500)       
    db.cur_Stock.execute( cmd.DelLastHour(yTicker, SqlMaxDate) )
    db.con_Stock.commit()
    db.cur_Stock.execute( cmd.DelDupHour(yTicker) )
    db.con_Stock.commit() 


def ClearAnalysDay( xTicker1):                       
    Arr_date = pd.read_sql(cmd.SLastDay(yTicker), db.eng_Stock)
    if len(Arr_date) >=1 :
        SqlMaxDate = Arr_date.iat[0, 0].strftime("%Y-%m-%d")
    else:
        SqlMaxDate = datetime.timedelta(days = -1000)      
    db.cur_Stock.execute( cmd.DelLastDay(yTicker, SqlMaxDate) )
    db.con_Stock.commit()
    db.cur_Stock.execute( cmd.DelDupDay(yTicker) )
    db.con_Stock.commit()     
    
    
try:
    warnings.simplefilter(action="ignore", category=FutureWarning)
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    Bef3YerDate = datetime.now()  - timedelta(days=1000)
    sql_cmd = cmd.s_Stock_Ticker
    if len(sys.argv) >=2:
        if sys.argv[1] == 'TW':
            sql_cmd = cmd.s_Stock_Ticker_TW
            CurrDate1 = datetime.now() + timedelta(days=1)
            CurrDate = CurrDate1.strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(sql_cmd, db.eng_Stock)
    for i in pd_read_sql.Stock:
        print('yfinance_每日抓_'+i)
        yTicker = i.strip()
        #yf.download(i,period='2y',interval='1h').to_csv('RowHr_'+i.strip()+'.csv')#to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        #小時K
        '''
        db.cur_Stock.execute( cmd.DelDupHour(yTicker) )
        db.con_Stock.commit()                
        SqlMaxDate = pd.read_sql(cmd.SLastHour(yTicker), db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
        db.cur_Stock.execute( cmd.DelLastHour(yTicker, SqlMaxDate) )
        db.con_Stock.commit()
        yf.download(yTicker,start = SqlMaxDate, end=CurrDate,interval='1h').to_sql( 'RowHour_'+yTicker,db.eng_Stock,if_exists='append', index=True)
        '''
        #日K
        db.cur_Stock.execute( cmd.DelDupDay(yTicker) )
        db.con_Stock.commit()
        try:
            SqlMaxDate = pd.read_sql(cmd.SLastDay(yTicker), db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
        except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
            SqlMaxDate = Bef3YerDate.strftime("%Y-%m-%d")                        
        db.cur_Stock.execute( cmd.DelLastDay(yTicker, SqlMaxDate) )
        db.con_Stock.commit()
        yf.download(yTicker,start = SqlMaxDate, end=CurrDate,interval='1d').to_sql( 'RowDay_'+yTicker,db.eng_Stock,if_exists='append', index=True)        

        

        '''
        #週K
        SqlMaxDate = pd.read_sql(cmd.SLastWeek(yTicker), db.eng_Stock).iat[0, 0].strftime("%Y-%m-%d")
        db.cur_Stock.execute( cmd.DelLastWeek(yTicker, SqlMaxDate) )
        db.con_Stock.commit()
        yf.download(yTicker,start = SqlMaxDate, end=CurrDate,interval='1wk').to_sql( 'RowWeek_'+yTicker,db.eng_Stock,if_exists='append', index=True)        


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


