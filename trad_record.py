#trad_record
import pymssql
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
import shutil
import os

SumSql1 = "SELECT '+極端-盈' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]" \
+"WHERE LongShort between 10 and  11 and profit >0" \
+"  and CreatDate >= GETDATE()-0.001" 


SumSql2 = "  SELECT top 50 * FROM [trade].[dbo].[TradeRecord_SPY]" \
    +"  WHERE Ticker like '%Total' and CreatDate >= @CrTime" \

file_source = "C:/Users/droop/OneDrive/Stock/Trade.py"
file_destination = "C:/Users/droop/OneDrive/trade/" #C:/Users/tom.gau/OneDrive/trade
file_source = "C:/Users/tom.gau/OneDrive/Stock"
file_destination = "C:/Users/tom.gau/OneDrive/trade"



engine3 = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/trade?charset=GBK")
sql = 'SELECT * FROM [trade].[dbo].[Strategy]'

def DoSummsry(TotTredRoc, CurrDateTime):
    file_source = './Trade.py'
    file_destination = '../trade/Trade_'+CurrDateTime.strftime("%Y-%m-%d")+'.py'
    strDatetime = CurrDateTime.strftime("%Y-%m-%d %H:%M:%S")
    shutil.copyfile(file_source, file_destination)
    TotTredRoc.to_sql('TradeRecord1',engine3,if_exists='append', index=False)
    

    ProfitVsLoss = pd.DataFrame()

    Strategy = pd.read_sql(sql, engine3, parse_dates=True)
    for x in range(0,14):
        #TredRoc.columns = ["Ticker","LongShort","Buydate","Selldate","buyPrice","SellPrice","profit", "CreatDate"]
        #a   = TotTredRoc.query("LongShort>10 & LongShort<12 & profit>0 & CreatDate> '"+ strDatetime+"'"  )
        a   = TotTredRoc.query( Strategy.at[x, "Dfcondition"]+"'"+ strDatetime+"'"  )
        #print(a.groupby('profit').size())
        #print(a.groupby('profit').size())
        cnt = a.shape[0]
        sum = round(a["profit"].sum(), 3)
        arr = [ strDatetime, TotTredRoc.at[1,"Ticker"], Strategy.at[x, "TPE"], cnt, sum]
        ProfitVsLoss = pd.concat([ProfitVsLoss, pd.DataFrame([arr])], ignore_index=True)
    ProfitVsLoss.columns = ["strDatetime", "Ticker", "LongShort","count","profit"]
    ProfitVsLoss.to_sql('ProfitLossRate',engine3,if_exists='append', index=False)
    print(ProfitVsLoss)
    #a = TotTredRoc.query("LongShort>10 & LongShort<12 & profit>0 & CreatDate> '"+ strDatetime+"'"  )     
        
    
        
    '''
    Profit = pd.read_sql(SumSql1, engine3)
    print(Profit)

    '''
        
        #Profit1 = pd.read_sql(SumSql1, engine3)
        #print(Profit1)    
    