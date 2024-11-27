import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np

import apka_score_ploy
import apka_count_EMA
import apka_score_trend
import apka_score_oscillate
import analsy_score_xcom
import Trade
import trad_record
import analsy_sql_cmd as cmd
import conn_db as db
import sys

print(sys.getdefaultencoding())     # 打印出目前系統字符編碼

s = 'I’Oa'
print(s)
#s_to_unicode = s.encode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
s_to_unicode = s.encode('GBK').decode('GBK')
print(s_to_unicode)


try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=cp936")
    engine1 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/analsy?charset=GBK")
    engine2 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/apka?charset=GBK")
    engine3 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/trade?charset=GBK")
    #sql = 'select * FROM [Stock].[dbo].[ApkaRating_day] '
    #pd_TechAnalysis = pd.read_sql(sql, engine)

    sql2 = 'select * FROM [Stock].[dbo].[Ticker_TW1] '
    Ticker = pd.read_sql(sql2, engine)
    CurrDateTime = datetime.now()
    StrDate = CurrDateTime.strftime("%Y-%m-%d")
    StrTime = datetime.now().strftime("_%Y-%m-%d_%H_%M_%S")
    Bef1YerDate = CurrDateTime  - timedelta(days=365)

    print('實驗日期-時間 : ' , CurrDateTime)
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)
#print(Ticker)
#print(Ticker.at[2 ,"mark"])

print(Ticker.at[2 ,"Ticker"].encode('latin-1').decode('cp936'))
print(Ticker.at[2 ,"mark"])
print(Ticker.at[2 ,"mark"].encode('latin-1').decode('cp936'))
print(Ticker.at[2 ,"mark"].encode('latin-1').decode('GBK'))
print(Ticker.at[2 ,"mark"].encode('cp936').decode('utf8'))
print(Ticker.at[2 ,"mark"].encode('GBK').decode('utf8'))
print(Ticker.at[2 ,"mark"].encode('utf8').decode('utf8'))
print(Ticker.at[2 ,"mark"].encode('cp936').decode('GBK'))