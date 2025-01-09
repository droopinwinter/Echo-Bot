#Trade
import pandas as pd
import os,sys
from datetime import datetime
import conn_db as db

xema    = 0.0
xema_1  = 0.0
yema    = 0.0
yema_1  = 0.0
xmacd   = 0.0
xmacd_1 = 0.0
OscSum  = 0.0
OscSum_1= 0.0
xTrnSlop= 0.0
prebuy  = 0.0
xBBand  = 0.0
buyPrice=0.0
plse    =0.0
plse_1  =0.0
Buydate ='2001-01-01 00:00:00.000'

def TotProfit(xapka, Ticker, CurrDateTime, rzt):
    def curValue(i):
        xema    = xapka.at[i,"xema"]
        xema_1  = xapka.at[i-1,"xema"]
        yema    = xapka.at[i,"yema"] 
        yema_1  = xapka.at[i-1,"yema"] 
        xmacd   = xapka.at[i,"xmacd"]
        xmacd_1 = xapka.at[i-1,"xmacd"]
        OscSum  = xapka.at[i,"OscSum"]
        OscSum_1= xapka.at[i-1,"OscSum"]
        xTrnSlop= xapka.at[i,"TrnSlop"]
        prebuy  = xapka.at[i-1,"buy"]
        xBBand  = xapka.at[i,"xBBand"]
        #xplse   = xapka.at[i,"plse"]
        #xplse_1 = xapka.at[i-1,"plse"]
        buyPrice = xapka.at[i,"close"]
        Buydate  = xapka.at[i, "date"]

    def Xtred(i):
        xtred = 0
        for j in range(1,5):
            xtred +=(xapka.at[i-j+1,"xmacd"] - xapka.at[i-j,"xmacd"])
        return xtred    
            
    def ToBuy(i, xtred):
        if prebuy ==0:
            if  ( OscSum==8 or (OscSum <  6 and OscSum_1 == 6 ) \
                 or ( OscSum < 4 and OscSum_1 == 4 ) )and (xmacd <-2 or xema<-2) :
                xapka.at[i,"buySig"] =10
                return 10 #+極端交易
            #elif ( OscSum < 4 and OscSum_1 == 4 ) and xmacd <=-1:
            #    return 11 #+極端交易
            #elif OscSum <= -6 and xmacd >=4 and xema >=4 and xTrnSlop<=0:
            #    return -11            
            elif  yema > yema_1  and yema >0 :#and xTrnSlop>0
                xapka.at[i,"buySig"] =yema
                return yema  #+GMMA交易                        
            #elif yema < yema_1 and yema <=-1 and xema <0 and xTrnSlop<=0:
            #    xapka.at[i,"buySig"] =yema
            #    return yema #-GMMA交易
            elif xmacd >0 and xmacd_1 <=0  and xTrnSlop>0:
                xapka.at[i,"buySig"] =20
                return 20 #+趨勢交易
            elif  xmacd <0 and xmacd_1 >=0 and xTrnSlop<-0.1:
                xapka.at[i,"buySig"] =-20
                return -20            
        else:
            return 0
        
    def ToSell(i, xtred):
        if   prebuy == 10 and (xmacd == 4 or (OscSum<=-1 and xmacd <0) )  :
            xapka.at[i,"SellSig"] =110  
            return prebuy #+極端交易
        elif prebuy == 11 and OscSum == 0 :
            xapka.at[i,"SellSig"] =111
            return prebuy #+極端交易
        elif prebuy == -11 and OscSum == 0 :
            xapka.at[i,"SellSig"] =-110
            return prebuy  #-極端交易      
        elif prebuy < 0 and prebuy > -10 and ( yema > yema_1 or xmacd > xmacd_1):
            xapka.at[i,"SellSig"] =prebuy-100
            return prebuy #-GMMA交易
        elif prebuy > 0   and prebuy < 10 and(yema < yema_1 or xmacd < xmacd_1 ): #and prebuy == yema_1
            xapka.at[i,"SellSig"] =prebuy+100
            return prebuy #+GMMA交易
        elif prebuy ==20  and (OscSum <=-6 or (xmacd < xmacd_1 ) \
                               or (xema < xema_1 ) ) :     
            xapka.at[i,"SellSig"] =prebuy+100
            return prebuy #+趨勢交易
        elif prebuy ==-20  and ( OscSum >=3 or (xmacd > xmacd_1 and  xmacd<=0 ) or (xema > xema_1 and  xema <=0))  :     
            xapka.at[i,"SellSig"] =prebuy-100
            return prebuy        
        else:
            return 0
#---------------------------------------------------------------------------
    buyPrice = 0.0
    BuySellway =''
    Buydate =''
    LongShort =''

    xapka.fillna(0)
    #print(xapka.head())
    TredRoc = pd.DataFrame()
    TredProfit = pd.DataFrame()
    for i in range(5,len(xapka)):
        curValue(i)
        totred = int (Xtred(i) or 0)
        toBuy = int (ToBuy(i, totred) or 0)
        toSell= int (ToSell(i, totred) or 0) 
        if toBuy >= 1 :
            xapka.at[i,"buy"] =toBuy
            BuySellway = BuySellway +'+Buy_'+str(xema_1)[5:10]+' => ' 
        elif toBuy <= -1 :
            xapka.at[i,"buy"] =toBuy
            BuySellway = BuySellway +'-Buy_'+str(xema_1)[5:10]+' => '             
        elif toSell >= 1 :
            #xapka.at[i,"Sell"] =1
            xapka.at[i,"buy"] =0
            xapka.at[i,"profit"] = (buyPrice - buyPrice)/buyPrice
            #print(BuySellway +'Sell_'+str(xema_1)[5:10]+'_profit= '+str( xapka.at[i,"profit"].round(3)))
            a = [Ticker, prebuy, Buydate, xema_1, round(buyPrice, 3), round(buyPrice, 3), round(xapka.at[i,"profit"],3), CurrDateTime]
            TredRoc = pd.concat([TredRoc, pd.DataFrame([a])], ignore_index=True)
            BuySellway =''
        elif toSell <= -1 :
            #xapka.at[i,"Sell"] =-1
            xapka.at[i,"buy"] =0
            xapka.at[i,"profit"] = (buyPrice - buyPrice)/buyPrice
            #print(BuySellway +'Sell_'+str(xema_1)[5:10]+'_profit= '+str( xapka.at[i,"profit"].round(3)))
            a = [Ticker, prebuy, Buydate, xema_1, round(buyPrice, 3), round(buyPrice, 3), round(xapka.at[i,"profit"], 3), CurrDateTime]
            TredRoc = pd.concat([TredRoc, pd.DataFrame([a])], ignore_index=True)            
            BuySellway =''
        else:
            #xapka.at[i,"Sell"] = xapka.at[i-1,"Sell"]
            xapka.at[i,"buy"]  = prebuy

    EndDate = len(xapka)
    init = total =100.0
    count = 0
    for i in range(1,EndDate):
        if xapka.at[i,"profit"] != 0:
            count = count +1
            total = total + total*xapka.at[i,"profit"]
    print( Ticker, "From [" + str(xapka.at[1,"date"]) +"] to ["+ str(xapka.at[len(xapka)-1,"date"]) +"] total =1000.0 after count: ["+str(count)+"] times total profit = "+str(round(total,3)) )
    

    mtime = os.path.getmtime('D:\Stock_bk\Trade.py') #修改时间
    mtime_string = datetime.fromtimestamp(int(mtime))
    b = [Ticker, mtime_string, xapka.at[1,"date"], xapka.at[len(xapka)-1,"date"], init, count, round(total,3),CurrDateTime]
    TredProfit = pd.concat([TredProfit, pd.DataFrame([b])], ignore_index=True)
    if len(TredProfit) >0:
        TredProfit.columns = ["Ticker","VersionDate","StartDate","EndDate","InitPrice","TradeCount","profit", "CreatDate"]
    #TredRoc = pd.concat([TredRoc, pd.DataFrame([a])], ignore_index=True)
    if len(TredRoc) > 0:
        TredRoc.columns = ["Ticker","LongShort","Buydate","Selldate","buyPrice","SellPrice","profit", "CreatDate"]
    ##############################################################################################
    CurrDateTime = datetime.now()
    if CurrDateTime.day == 1 or CurrDateTime.day == 15:
        try:
            if len(TredProfit) >0:
                TredProfit.to_sql( 'TrateProf1',db.eng_trade,if_exists='append', index=False)
            if len(TredRoc) > 0:
                TredRoc.to_sql( 'TrateRec_'+Ticker,db.eng_trade,if_exists='append', index=False)        
            #print(SingTredRoc)
        except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print('回存Trade資料庫錯誤_', Ticker , errMsg) 

    if rzt == 1:
        return xapka
    else:
        return TredRoc
    #TredRoc.to_csv('TredRocord_'+Ticker+'.csv')     
    
#---------------------------------------------------------------------------
    def BbToBuy(i):
        if prebuy ==0:
            if   xBBand ==2:
                return 1
            #elif xBBand ==-2:
            #    return -1               
        else:
            return 0
        
    def BbToSell(i):
        if   xBBand  <0 and prebuy == 1:
            return 1
        elif xBBand  >0 and prebuy == -1:
            return -1
        else:
            return 0
#---------------------------------------------------------------------------
    def MacdToBuy(i):
        if prebuy ==0:
            if   xmacd > xmacd_1 and xmacd_1== -1 :
                return 1
            #elif xBBand ==-2:
            #    return -1               
        else:
            return 0
        
    def MacdToSell(i):
        
        if   xmacd < xmacd_1 and xmacd_1== 2 and prebuy == 1:
            return 1
        #elif xmacd < xmacd_1 and xmacd_1== 2:
        #    return -1
        else:
            return 0
