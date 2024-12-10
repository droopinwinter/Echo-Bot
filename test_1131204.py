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
import sys

def ClearAnalysHour( xTicker1,):
    SqlMaxDate = pd.read_sql(cmd.SLastHour( xTicker1), db.eng_analsy).iat[0, 0].strftime("%Y-%m-%d")
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

stk_list1 = ['00642U.TW','00645.TW','00661.TW','00685L.TW','00738U.TW','00708L.TW','00640L.TW','00635U.TW','00693U.TW','00763U.TW','00683L.TW','00663L.TW','00709.TW','00660.TW','00682U.TW']

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    pd_TechAnalysis = pd.read_sql(cmd.s_Stock_TechAnalysis, db.eng_Stock)
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    sql_cmd = cmd.s_Stock_Ticker_TW  #s_Stock_Ticker
    if len(sys.argv) >=2:
        if sys.argv[1] == 'TW':
            sql_cmd = cmd.s_Stock_Ticker_TW

    pd_read_sql = pd.read_sql(sql_cmd, db.eng_Stock)
    for i in pd_read_sql.Stock:
    #for i in stk_list1:
        print('talib_每日抓_'+i)
        yTicker = i.strip()
        db.cursor_analsy.execute(cmd.DelLastDay( yTicker,'2024-11-29') )
        db.conn_analsy.commit()


        time.sleep(5)   
    #print(pd_read_sql.kdatetime)
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)






