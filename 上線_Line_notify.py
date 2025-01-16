import requests
import pymssql
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
import notify_sql_cmd as cmd
import conn_db as db
import symbol2Chtext as cv
import sys 

manual = "\n技術分析-日K+週K-綜合訊號說明如下\n"+\
         "Sta  當下買賣狀態(-20~20 )大於0時為多倉,小於0時為空倉\n"+\
         "slop 3日漲跌斜率(-20~20)  大於1時3日均漲幅>1％ \n"+\
         "OSC  綜合震盪極限(-8~8)   小於-6時疑超跌,大於6時疑超漲\n"+\
         "MACD 日K+週K趨勢(-4~4)    大於2時確認牛市\n"+\
         "BB   日K布林區間(0.0~1.0) 小於0.1下，搭配OSC大於6疑反轉\n"
def lineNotify(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = 'HsPrW2IKr4JpdhJB7x1RpG5iMZNEMH60f9V3BkkimOb'#'Cw2ifsTDcyllU50bnKKik6d9y3nez6O4PGjmX5uUXSP'  # 替換成自己的 LINE Notify 權杖
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': msg}
    requests.post(url, headers=headers, data=data)
    time.sleep(1)

def read_sql1(SqlStr, engine):
#          做多 做多 做空 做空
#次數  利潤 次數 利潤 次數 利潤    品種
   sProfTitle = '                 做多 做多 做空 做空\n'+\
                '次數  利潤 次數 利潤 次數 利潤    品種\n'#'品種 交易次數 利潤\n'
   df = pd.read_sql(SqlStr, engine)
   if len(df) == 0 :
      return ''
   else:
      Sdate = df.at[10,"StartDate"]
      Edate = df.at[10,"EndDate"]
      df =df.drop(columns=["StartDate","EndDate"])
      df = cv.USdf2Chtext(df)
      for col in df.columns:
         df[col] = df[col].astype(str)
         df[col] = df[col].str.rjust(4)
      df["STK"] = df["STK"].str.ljust(min(len(df["profit"]), 10))
      #df["profit"] = df["profit"].str.pad( min(len(df["profit"]), 6), side='right')
      #df[""] = df[""].str.zfill(6)  
      StrData = df.to_string(index=False,header=False)
      return "起使日期_"+Sdate.strftime("%Y-%m-%d") +"\n結束日期"+Edate.strftime("%Y-%m-%d")+"\n"+sProfTitle+StrData

def read_sql(SqlStr, engine):
   Ticker = pd.read_sql(SqlStr, engine)
   Ticker =Ticker.drop(columns=["date"])
   #print(Ticker)
   Ticker = cv.USdf2Chtext(Ticker)
   for col in Ticker.columns:
      Ticker[col] = Ticker[col].astype(str)
      #Ticker[col] = Ticker[col].str.pad( min(len(Ticker[col]), 4), side='left')
      Ticker[col] = Ticker[col].str.rjust(4)
      if col == 'STK':
         Ticker[col] = Ticker[col].str.ljust(min(len(Ticker[col]), 5))
      if col == 'TYP':
         Ticker[col] = Ticker[col].str.pad( min(len(Ticker[col]), 1), side='left')
      '''
      if col == 'OSC':
         Ticker[col] = Ticker[col].str.rjust(2)      
      if col == 'MCD':
         Ticker[col] = Ticker[col].str.rjust(2)    
      if col == 'Sta':
         Ticker[col] = Ticker[col].str.zfill(6)                
      if col == 'SellSig':
         Ticker = cv.SellSigdf2Chtext(Ticker)         
      '''
   StrData = Ticker.to_string(index=False,header=False)
   #for col in Ticker.columns:
   #  Ticker[col] = Ticker[col].str.pad(min(len(Ticker[col]), 4), side='both') # 填充到指定长度，不足则右对齐    
   if len(Ticker) == 0 :
      return ''
   else:
      return StrData

def NotifyComm(ybefDay,yStrDate,ycountry):         
   msg1 = read_sql(cmd.Sig2BuySell(ybefDay,ycountry), db.eng_apka)
   if msg1 !='':
      lineNotify( "\n日期 : "+ yStrDate +"\n買賣徵兆\n"+sBuyTitle +  msg1)
   #msg2 =  read_sql(cmd.Sig2LowBull(ybefDay,ycountry), db.eng_apka)
   #if msg2 !='':
   #   lineNotify( "\n日期 : "+ yStrDate +"\n接近布林帶下沿\n"+ msg2)
   msg3 = read_sql(cmd.Sig2HighBull(ybefDay,ycountry), db.eng_apka)
   if msg3 !='':
      lineNotify( "\n日期 : "+ yStrDate +"\n逼近布林帶邊緣且有極端反轉訊號\n"+ sLimiTitle+msg3)

xToday = datetime.now()
Bef1Date = xToday - timedelta(days=1)
sToday = xToday.strftime("%Y-%m-%d")
StrDate = Bef1Date.strftime("%Y-%m-%d")
print('實驗日期-時間 : ' , sToday)
befDay = '2'
country = 'US'
if len(sys.argv) >=2:
   if sys.argv[1] == 'TW':
      country = 'TW'
      befDay = '1'
      
cmd.DelDupDay(country)
stitle = " 類  布林 擺盪 多空 持倉 \n"+ " 別  帶限 極限 趨勢 狀態  品種\n"
sBuyTitle = "                            多空\n"+"類別 進出場信號  趨勢   品種\n"
sLimiTitle = "類別 布林 擺盪 九轉\n"+"        帶限 極限       品種\n"

'''
"類別 布林 擺盪 多空 持倉 \n"+
"        帶限 極限 趨勢 狀態 品種\n"

"                     多空 品種\n"+
"類別 進場信號 出場信號 趨勢 品種\n"

" 類  布林 擺盪 多空 持倉 \n"+
" 別  帶限 極限 趨勢 狀態  品種\n"
'''
try:
   if country == 'TW':      
      NotifyComm(befDay, sToday, country)
      msg5 = read_sql(cmd.Sig2TrendAndOsc_part1(befDay,country), db.eng_apka)
      if msg5 !='':
         #lineNotify( "\n日期 : "+ StrDate + manual)
         lineNotify("\n日期 : "+ sToday+"\n股指_前22個\n"+stitle+ msg5)
      msg5 = read_sql(cmd.Sig2TrendAndOsc_part2(befDay,country), db.eng_apka)
      if msg5 !='':
         lineNotify("\n日期 : "+ sToday+"\n基金_共22個\n"+stitle+ msg5)  
      msg5 = read_sql(cmd.Sig2TrendAndOsc_part3(befDay,country), db.eng_apka)
      if msg5 !='':
         lineNotify("\n日期 : "+ sToday+"\n其他＿共22個\n"+stitle+ msg5)
      
      if xToday.day == 1 or xToday.day == 16 :
         msg5 = read_sql1(cmd.TradeProfit1M( 3,country), db.eng_trade)
         if msg5 !='':
            lineNotify("\n日期 : "+ sToday+"\n一年內交易績效排序\n"+ msg5)
   else:
      NotifyComm(befDay, sToday, country)
      msg5 = read_sql(cmd.Sig2TrendAndOsc_part1(befDay,country), db.eng_apka)
      if msg5 !='':
         #lineNotify( "\n日期 : "+ StrDate + manual)
         lineNotify("\n日期 : "+ sToday+"\n股指_前22\n"+stitle+ msg5)
      msg5 = read_sql(cmd.Sig2TrendAndOsc_part2(befDay,country), db.eng_apka)
      if msg5 !='':
         lineNotify("\n日期 : "+ sToday+"\n大科技&其他\n"+stitle+ msg5)  
      '''      
      msg5 = read_sql(cmd.Sig2TrendAndOsc_part3(befDay,country), db.eng_apka)
      if msg5 !='':
         lineNotify("_大科技＿共11個\n"+msg5)   
      '''
      if xToday.day == 1 or xToday.day == 16 :
         msg5 = read_sql1(cmd.TradeProfit1M( 3,country), db.eng_trade)
         if msg5 !='':
            lineNotify("\n日期 : "+ sToday+"\n一年內交易績效排序\n"+ msg5)      
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

