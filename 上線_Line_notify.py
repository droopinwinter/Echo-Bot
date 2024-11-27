import requests
import pymssql
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import notify_sql_cmd as cmd
import conn_db as db

def lineNotify(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = 'HsPrW2IKr4JpdhJB7x1RpG5iMZNEMH60f9V3BkkimOb'#'Cw2ifsTDcyllU50bnKKik6d9y3nez6O4PGjmX5uUXSP'  # 替換成自己的 LINE Notify 權杖
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': msg}
    requests.post(url, headers=headers, data=data)

def read_sql(SqlStr, engine):
    Ticker = pd.read_sql(SqlStr, engine)
    Ticker =Ticker.drop(columns=["date"])
    for col in Ticker.columns:
         Ticker[col] = Ticker[col].astype(str)
         Ticker[col] = Ticker[col].str.pad( min(len(Ticker[col]), 4), side='left')

    StrDate = Ticker.to_string()
    #for col in Ticker.columns:
    #  Ticker[col] = Ticker[col].str.pad(min(len(Ticker[col]), 4), side='both') # 填充到指定长度，不足则右对齐    
    if len(Ticker) == 0 :
       return ''
    else:
       return StrDate

Bef1Date = datetime.now()  - timedelta(days=1)
StrDate = Bef1Date.strftime("%Y-%m-%d")
print('實驗日期-時間 : ' , StrDate)
befDay = '2'
try:
    msg1 = read_sql(cmd.Sig2BuySell(befDay), db.eng_apka)
    if msg1 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n買賣徵兆\n"+  msg1)
    time.sleep(1)
    
    msg2 =  read_sql(cmd.Sig2LowBull(befDay), db.eng_apka)
    if msg2 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n接近布林帶下沿\n"+ msg2)
    time.sleep(1)
    
    msg3 = read_sql(cmd.Sig2HighBull(befDay), db.eng_apka)
    if msg3 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n接近布林帶上沿\n"+ msg3)
    time.sleep(1)

    msg5 = read_sql(cmd.Sig2TrendAndOsc_part1(befDay), db.eng_apka)
    if msg5 !='':
       lineNotify( "\n日期 : "+ StrDate +\
                   "\n趨勢技術分析-訊號縮寫如下\n"+\
                   "bi= buy 買賣狀態(-20 ~ 20)\n "+\
                   "md= MACD狀態(-4 ~ +4)\n"+\
                   "sp= slop漲跌斜率(-20 ~ +20)\n"+\
                   "os= OSC 震盪指標(-8 ~ +8)\n"+\
                   "BB=BBand布林區間(0.0~ 1.0)\n")
       lineNotify("\n股指_前11個\n"+msg5)   

    msg5 = read_sql(cmd.Sig2TrendAndOsc_part2(befDay), db.eng_apka)
    if msg5 !='':
       lineNotify("\n板塊_共11個\n"+msg5)  

    msg5 = read_sql(cmd.Sig2TrendAndOsc_part3(befDay), db.eng_apka)
    if msg5 !='':
       lineNotify("\n大科技＿共11個\n"+msg5)            
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

