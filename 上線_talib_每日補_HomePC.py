import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta
import talib
from talib import abstract
import conn_db as db
import talib_sql_cmd as cmd
import collect_sql_cmd

def ClearAnalysHour( xTicker1,):
    Arr_date = pd.read_sql(cmd.SLastHour( xTicker1), db.eng_analsy)
    if Arr_date.count >=1 :
        SqlMaxDate = Arr_date.iat[0, 0].strftime("%Y-%m-%d")
    else:
        SqlMaxDate = datetime.timedelta(days = -1000)
    db.cursor_analsy.execute(cmd.DelLastHour( xTicker1, SqlMaxDate) )
    db.conn_analsy.commit()    
    db.cursor_analsy.execute(cmd.DelDupHour( xTicker1) )
    db.conn_analsy.commit()
    return SqlMaxDate

def ClearAnalysDay( xTicker1,):
    SqlMaxDate = pd.read_sql(cmd.SLastDay( xTicker1), db.eng_analsy).iat[0, 0].strftime("%Y-%m-%d")
    db.cursor_analsy.execute(cmd.DelLastDay( xTicker1, SqlMaxDate) )
    db.conn_analsy.commit()    
    db.cursor_analsy.execute(cmd.DelDupDay( xTicker1) )
    db.conn_analsy.commit()
    return SqlMaxDate

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    pd_TechAnalysis = pd.read_sql(cmd.s_Stock_TechAnalysis, db.eng_Stock)
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(cmd.s_Stock_Ticker, db.eng_Stock)
    for i in pd_read_sql.Stock:
        print('Stock_'+i)
        yTicker = i.strip()
        try:
            #SRSI
            SqlMaxDate = ClearAnalysDay( yTicker)
            SqlMinDate = pd.read_sql(cmd.S1000StockDay(yTicker), db.eng_Stock).iat[999, 0].strftime("%Y-%m-%d")
            data       = pd.read_sql(cmd.SPeriodDay( yTicker,SqlMinDate), db.eng_Stock, parse_dates=True)
            data.columns = ["date","open", "high", "low", "close", "adj close", "colume"]
            for x in range(0,22):
                rztcoul = pd_TechAnalysis.at[x,"RztLabel"].strip().split(',')
                try:
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
                data1 = data[data["date"] >= SqlMaxDate+" 00:00:00.000"]  
                data1.reset_index(drop=True)
                data.columns = ["date","open","high","low","close","adjclose","colume",\
                        "fastk_d","fastd_d","fastk_w","fastd_w","fastk_m","fastd_m","willrd","willrw","willrm",\
                        "MACD_d","signal_d","histg_d","MACD_w","signal_w","histg_w","MACD_m","signal_m","histg_m",\
                        "upp_d","mid_d","low_d","upp_w","mid_w","low_w","upp_m","mid_m","low_m",\
                        "ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10"]  
                data.to_sql( 'AnalysDay_'+yTicker,db.eng_analsy,if_exists='append', index=False)
            except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
                print('回存資料庫錯誤_', yTicker , errMsg)    
        except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print('Day發生錯誤-'+yTicker , errMsg)            
        '''
        try:
            #小時K
            SqlMaxDate = ClearAnalysHour( yTicker)
            SqlMinDate = pd.read_sql(cmd.S1000StockHour(yTicker)         , db.eng_Stock).iat[999, 0].strftime("%Y-%m-%d")
            data       = pd.read_sql(cmd.SPeriodHour( yTicker,SqlMinDate), db.eng_Stock, parse_dates=True)
            data.columns = ["date","open", "high", "low", "close", "adj close", "colume"]
            for x in range(0,22):
                rztcoul = pd_TechAnalysis.at[x,"RztLabel"].strip().split(',')
                try:
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
                data1 = data[data["date"] >= SqlMaxDate+" 00:00:00.000"]  
                data1.reset_index(drop=True)
                data.columns = ["date","open","high","low","close","adjclose","colume",\
                        "fastk_d","fastd_d","fastk_w","fastd_w","fastk_m","fastd_m","willrd","willrw","willrm",\
                        "MACD_d","signal_d","histg_d","MACD_w","signal_w","histg_w","MACD_m","signal_m","histg_m",\
                        "upp_d","mid_d","low_d","upp_w","mid_w","low_w","upp_m","mid_m","low_m",\
                        "ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10"]  
                data.to_sql( 'AnalysHour_'+i.strip(),db.eng_analsy,if_exists='append', index=False)
            except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
                print('回存資料庫錯誤_', yTicker , errMsg)    
        except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print('發生錯誤-'+yTicker , errMsg)            
        '''

        
        #週K
        '''
        sql3 = 'select top 1 max(Date) Date FROM [Stock].[dbo].[RowWeek_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowWeek_"+i.strip()+"] Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        yf.download(i,start = SqlMaxDate, end=CurrDate,interval='1wk').to_sql( 'RowWeek_'+i.strip(),engine,if_exists='append', index=True)

        '''

        #yf.download(i,period='2y',interval='1h').to_csv('RowHr_'+i.strip()+'.csv')#to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        #小時K
        '''
        sql3 = 'select top 1 max(Datetime) Date FROM [Stock].[dbo].[RowHour_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowHour_"+i.strip()+"] Where Datetime >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        '''

        #rzt = yf.download(i,start = SqlMaxDate.iat[0, 0].strftime("%Y-%m-%d"), end=CurrDate.strftime("%Y-%m-%d"),interval='1h')
        #print(rzt)
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


