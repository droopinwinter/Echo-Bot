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
import requests, json 

manual = "\n技術分析-日K+週K-綜合訊號說明如下\n"+\
         "Sta  當下買賣狀態(-20~20 )大於0時為多倉,小於0時為空倉\n"+\
         "slop 3日漲跌斜率(-20~20)  大於1時3日均漲幅>1％ \n"+\
         "OSC  綜合震盪極限(-8~8)   小於-6時疑超跌,大於6時疑超漲\n"+\
         "MACD 日K+週K趨勢(-4~4)    大於2時確認牛市\n"+\
         "BB   日K布林區間(0.0~1.0) 小於0.1下，搭配OSC大於6疑反轉\n"

##########################################################################
def ReadText(UseWay, Country):
    #path ="D:\\AI-Line-Bot\\static\\"+ UseWay+"_"+Country+ ".txt"
    path = UseWay+"_"+Country+ ".txt"
    f = open(path, 'r')
    return f.read()
##########################################################################
def lineNotify(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = 'HsPrW2IKr4JpdhJB7x1RpG5iMZNEMH60f9V3BkkimOb'#'Cw2ifsTDcyllU50bnKKik6d9y3nez6O4PGjmX5uUXSP'  # 替換成自己的 LINE Notify 權杖
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': msg}
    requests.post(url, headers=headers, data=data)
    time.sleep(1)
##########################################################################    
def lineBotNotify(msg):
    headers = {'Authorization':'Bearer be0tzYkk3VyLZ+zHNZDy98vfexagRGkGuFIODguqmHzaMLhP81SDXBOxeL2amDG3gdIdMZ3J3SbNhf+BDaLxfAokk3lnUtBGpFbnGI0qVh+rBzCT7wvKj/KNKtAH8OPRVT04Hvo/Sq0sRw4nhWiv+QdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}
    body = {
        'to':'U7cae8226e0d97a3574ee92492aaf898a',
        'messages':[{
                'type': 'text',
                'text': msg
            }]
        }
    # 向指定網址發送 request
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(body).encode('utf-8'))

##########################################################################
def Sql2Str(SqlStr, engine):
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

   StrData = Ticker.to_string(index=False,header=False)
   #for col in Ticker.columns:
   #  Ticker[col] = Ticker[col].str.pad(min(len(Ticker[col]), 4), side='both') # 填充到指定长度，不足则右对齐    
   if len(Ticker) == 0 :
      return ''
   else:
      return StrData
##########################################################################   
def GetProfit(country):
#          做多 做多 做空 做空
#次數  利潤 次數 利潤 次數 利潤    品種
    '''
    sProfTitle = '總和  總和 做多 做多 做空 做空\n'+\
                 '次數  利潤 次數 利潤 次數 利潤    品種\n'#'品種 交易次數 利潤\n'
    df = pd.read_sql(cmd.TradeProfit1M( 16,country), db.eng_trade)
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
        return "起使日期_"+Sdate.strftime("%Y-%m-%d") +"\n結束日期_"+Edate.strftime("%Y-%m-%d")+"\n"+sProfTitle+StrData   
    '''
    return ReadText("Profit", country)        

##########################################################################
def NotifySign(ybefDay,yStrDate,ycountry):
    sBuyTitle = "                           多空\n"+"類別 進出場信號  趨勢   品種\n"
    sLimiTitle = "類別 布林 擺盪 神奇\n"+"        帶限 極限 九轉    品種\n"
    #msg1 = Sql2Str(cmd.Sig2BuySell(ybefDay,ycountry), db.eng_apka)
    msg1 = ReadText("Trade", ycountry)
    if msg1 !='':
        msg1 = "\n日期 : "+ yStrDate +"\n買賣徵兆\n"+ sBuyTitle+ msg1

    #msg3 = Sql2Str(cmd.Sig2HighBull(ybefDay,ycountry), db.eng_apka)
    msg3 =  ReadText("Warn", ycountry)
    if msg3 !='':
        msg3 = "\n可能有極端反轉訊號\n"+sLimiTitle+ msg3 
    return msg1 + msg3
##########################################################################
def GetEvaluate_TW(befDay,StrDate):
    stitle = "\n 布林 擺盪 多空 持倉 \n"+ " 帶限 極限 趨勢 狀態  品種\n"
    '''
    msg5 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'TW','etf'), db.eng_apka)
    if msg5 !='': #"\n台股板塊評估"+
        msg5 = "\n日期 : "+ StrDate +"\n_板塊"+stitle+msg5
    msg6 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'TW','index'), db.eng_apka)
    if msg6 !='':
        msg6 = "\n_股指_"+stitle+msg6        
    msg7 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'TW','stock'), db.eng_apka)
    if msg7 !='':
        msg7 = "\n_股票_"+stitle+msg7  
    msg8 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'TW','main'), db.eng_apka)
    if msg8 !='':
        msg8 = "\n_期貨_"+stitle+msg8    
    return msg5 + msg6 + msg7+msg8        
    '''
    return ReadText("Daily", "TW")

##########################################################################
def GetEvaluate_US(befDay,StrDate):
    '''
    stitle = "\n 布林 擺盪 多空 持倉 \n"+ " 帶限 極限 趨勢 狀態  品種\n"
    msg5 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'US','etf'), db.eng_apka)
    if msg5 !='': #"\n美股板塊評估"+
        msg5 = "\n日期 : "+ StrDate +"\n_板塊_"+stitle+msg5
    msg6 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'US','index'), db.eng_apka)
    if msg6 !='':
        msg6 = "\n_指數_\n"+stitle+msg6
    msg7 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'US','stock'), db.eng_apka)
    if msg7 !='':
        msg7 = "\n_股票_\n"+stitle+msg7
    msg8 = Sql2Str(cmd.Sig2TrendAndOsc_part1(befDay,'US','main'), db.eng_apka)
    if msg8 !='':
        msg8 = "\n_期貨_\n"+stitle+msg8
    return msg5 + msg6+msg7 + msg8
    '''
    return ReadText("Daily", "US")


##########################################################################
def DailyNotiyf(country):
    xToday = datetime.now()
    Bef1Date = xToday - timedelta(days=1)
    sToday = xToday.strftime("%Y-%m-%d")
    StrDate = Bef1Date.strftime("%Y-%m-%d")
    print('實驗日期-時間 : ' , sToday)
    befDay = '2'
    if country == 'TW':
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
        NotifySign(befDay, StrDate, country)
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('連線SQL發生錯誤-' , errMsg)

