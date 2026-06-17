from datetime import datetime
from datetime import timedelta
import time
import symbol2Chtext as cv
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
##########################################################################
##########################################################################   
def GetProfit(country):
    return ReadText("Profit", country)        
##########################################################################
def NotifySign(ybefDay,yStrDate,ycountry):
    msg =''
    msg1 = ReadText("Trade", ycountry)
    if msg1 !='':
        msg =msg + msg1
    msg3 =  ReadText("Warn", ycountry)
    if msg3 !='':
        msg =msg +"\n"+ msg3 
    return msg1 + msg3
##########################################################################
def GetEvaluate_TW(befDay,StrDate):
    return ReadText("Daily", "TW")
##########################################################################
def GetEvaluate_US(befDay,StrDate):
    return ReadText("Daily", "US")
##########################################################################
def DailyNotiyf(country):
    xToday = datetime.now()
    Bef1Date = xToday - timedelta(days=1)
    StrDate = Bef1Date.strftime("%Y-%m-%d")
    befDay = '2'
    if country == 'TW':
        befDay = '1'
    NotifySign(befDay, StrDate, country)

