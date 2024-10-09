import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta

# 先測試一檔試看看
stock = yf.Ticker('2317.TW')
#yf.download('2317.TW',period='max',interval='1d').to_csv('2317.csv')
engine = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/Stock?charset=GBK")
yf.download('2317.TW',period='1d',interval='1h').to_sql( 'RowHour_2317',engine,if_exists='append', index=True)
time.sleep(5) 
# 取得價量資料＋股利發放資料＋股票分割資料

#stock.history(period = 'max')