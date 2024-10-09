import requests
import pymssql
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time

#=================================================
# 買賣徵兆
Sql1 = "SELECT distinct [date],[buySig] buy,[SellSig] Sell,[OscSum] Osc,[BBlevel] BB,[TrnSlop] slp ,substring([xremark],4,5) typ"+\
" FROM [apka].[dbo].[ApkaDay_Combin] "+\
" where date > GETDATE()-2 AND ( buySig <>0 or SellSig <> 0) order by date,typ "

#=================================================
# 接近布林帶下沿
Sql2 = "SELECT distinct [date],[BBlevel] BB,[OscSum] Osc,[TrnSlop] slp ,substring([xremark],4,5) typ "+\
       " FROM [apka].[dbo].[ApkaDay_Combin] "+\
       " where date > GETDATE()-2 AND ([BBlevel]<0.2 ) order by date,typ "

#=================================================
# 接近布林帶上沿
Sql3 = "SELECT distinct [date],[BBlevel] BB,[OscSum] Osc,[TrnSlop] slp ,substring([xremark],4,5) typ "+\
       " FROM [apka].[dbo].[ApkaDay_Combin]  "+\
       " where date > GETDATE()-2 AND ([BBlevel]>0.9 ) order by date,typ"
#=================================================
# 當日收盤後技術分析擺盪
Sql4 = "SELECT  distinct [date],[buy],[OscSum] Osc,[BBlevel] BB,[xremark] typ "+\
       " FROM [apka].[dbo].[ApkaDay_Combin] "+\
       " where date > GETDATE()-2 "+\
       " order by date,xremark"
#=================================================
# 當日收盤後技術分析趨勢
#Sql5 = "SELECT  distinct [date],[xema] ema,[xmacd] mcd,[TrnSlop] slp,[OscSum] Os,[BBlevel] BB,[xremark] typ "+\
#       " FROM [apka].[dbo].[ApkaDay_Combin] "+\
#       " where date > GETDATE()-2 "+\
#       " order by date,xremark"
Sql5 = "SELECT [date],[xema] ema,[xmacd] mcd,[TrnSlop] slp,[OscSum] Os,[BBlevel] BB,[mark] typ FROM ( "+\
      "  SELECT distinct [date],[xema],[xmacd],[TrnSlop],[buySig],[SellSig],[buy],[OscSum] "+\
      "  ,[BBlevel], substring([xremark],1,2) pre,substring([xremark],4,5) mark "+\
      "  FROM [apka].[dbo].[ApkaDay_Combin] where date > GETDATE()-2 "+\
      ") a order by pre "

def lineNotify(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = 'HsPrW2IKr4JpdhJB7x1RpG5iMZNEMH60f9V3BkkimOb'#'Cw2ifsTDcyllU50bnKKik6d9y3nez6O4PGjmX5uUXSP'  # 替換成自己的 LINE Notify 權杖
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': msg}
    requests.post(url, headers=headers, data=data)

def read_sql(SqlStr, engine):
    Ticker = pd.read_sql(SqlStr, engine)
    Ticker =Ticker.drop(columns=["date"])
    StrDate = Ticker.to_string()
    if len(Ticker) == 0 :
       return ''
    else:
       return StrDate

Bef1Date = datetime.now()  - timedelta(days=1)
StrDate = Bef1Date.strftime("%Y-%m-%d")
print('實驗日期-時間 : ' , StrDate)

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数  
    engine = create_engine("mssql+pymssql://sa:abc123@127.0.0.1:1433/apka?charset=GBK")
    #sql2 = 'select * FROM [Stock].[dbo].[Ticker_apk] '
    #Ticker = pd.read_sql(sql2, engine)
    #StrDate = Ticker.to_string()
        
    msg1 = read_sql(Sql1, engine)
    if msg1 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n買賣徵兆\n"+  msg1)
    time.sleep(1)
    
    msg2 =  read_sql(Sql2, engine)
    if msg2 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n接近布林帶下沿\n"+ msg2)
    time.sleep(1)
    
    msg3 = read_sql(Sql3, engine)
    if msg3 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n接近布林帶上沿\n"+ msg3)
    time.sleep(1)

   # msg4 = read_sql(Sql4, engine)
   # if msg4 !='':
   #    lineNotify( "\n日期 : "+ StrDate +"\n擺盪技術分析\n"+ msg4)
   # time.sleep(1)
   
    msg5 = read_sql(Sql5, engine)
    if msg5 !='':
       lineNotify( "\n日期 : "+ StrDate +"\n趨勢技術分析\n"+ msg5) 
    
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)

