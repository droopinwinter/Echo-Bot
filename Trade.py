#Trade
import pandas as pd
import os,sys
from datetime import datetime
import conn_db as db

def TotProfit(xapka, Ticker, CurrDateTime, rzt):

    def Xtred(i):
        xtred = 0
        for j in range(1,5):
            xtred +=(xapka.at[i-j+1,"xmacd"] - xapka.at[i-j,"xmacd"])
        return xtred    
            
    def ToBuy(i, xtred):
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
        xplse   = xapka.at[i,"plse"]
        xplse_1 = xapka.at[i-1,"plse"]
        cnt9    = xapka.at[i-1,"count9"]

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
            elif xmacd >0 and xmacd_1 <=0   and xTrnSlop>0:
                xapka.at[i,"buySig"] =20
                return 20 #+趨勢交易
            elif  xmacd <0 and xmacd_1 >=0 and xTrnSlop<-0.1:
                xapka.at[i,"buySig"] =-20
                return -20            
        else:
            return 0
        
    def ToSell(i, xtred):
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
        xplse   = xapka.at[i,"plse"]
        xplse_1 = xapka.at[i-1,"plse"]
        cnt9    = xapka.at[i-1,"count9"]
        
        Prebuy = xapka.at[i-1,"buy"]
        if   Prebuy == 10 and (xmacd == 4 or (OscSum<=-1 and xmacd <0) )  :
            xapka.at[i,"SellSig"] =110  
            return Prebuy #+極端交易
        elif Prebuy == 11 and OscSum == 0 :
            xapka.at[i,"SellSig"] =111
            return Prebuy #+極端交易
        elif Prebuy == -11 and OscSum == 0 :
            xapka.at[i,"SellSig"] =-110
            return Prebuy  #-極端交易      
        elif Prebuy < 0 and Prebuy > -10 and ( yema > yema_1 or xmacd > xmacd_1):
            xapka.at[i,"SellSig"] =Prebuy-100
            return Prebuy #-GMMA交易
        elif Prebuy > 0   and Prebuy < 10 and(yema < yema_1 or xmacd < xmacd_1 ): #and Prebuy == yema_1
            xapka.at[i,"SellSig"] =Prebuy+100
            return Prebuy #+GMMA交易
        elif Prebuy ==20  and (OscSum <=-6 or (xmacd < xmacd_1 ) \
                               or (xema < xema_1 ) ) :     
            xapka.at[i,"SellSig"] =Prebuy+100
            return Prebuy #+趨勢交易
        elif Prebuy ==-20  and ( OscSum >=3 or (xmacd > xmacd_1 and  xmacd<=0 ) or (xema > xema_1 and  xema <=0))  :     
            xapka.at[i,"SellSig"] =Prebuy-100
            return Prebuy        
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
        totred = int (Xtred(i) or 0)
        toBuy = int (ToBuy(i, totred) or 0)
        toSell= int (ToSell(i, totred) or 0) 
        if toBuy >= 1 :
            xapka.at[i,"buy"] =toBuy
            buyPrice = xapka.at[i,"close"]
            Buydate  = xapka.at[i, "date"]
            BuySellway = BuySellway +'+Buy_'+str(xapka.at[i, "date"])[5:10]+' => ' 
        elif toBuy <= -1 :
            xapka.at[i,"buy"] =toBuy
            buyPrice = xapka.at[i,"close"]
            Buydate  = xapka.at[i, "date"]
            BuySellway = BuySellway +'-Buy_'+str(xapka.at[i, "date"])[5:10]+' => '             
        elif toSell >= 1 :
            #xapka.at[i,"Sell"] =1
            xapka.at[i,"buy"] =0
            xapka.at[i,"profit"] = (xapka.at[i,"close"] - buyPrice)/buyPrice
            #print(BuySellway +'Sell_'+str(xapka.at[i, "date"])[5:10]+'_profit= '+str( xapka.at[i,"profit"].round(3)))
            a = [Ticker, xapka.at[i-1,"buy"], Buydate, xapka.at[i, "date"], round(buyPrice, 3), round(xapka.at[i,"close"], 3), round(xapka.at[i,"profit"],3), CurrDateTime]
            TredRoc = pd.concat([TredRoc, pd.DataFrame([a])], ignore_index=True)
            BuySellway =''
        elif toSell <= -1 :
            #xapka.at[i,"Sell"] =-1
            xapka.at[i,"buy"] =0
            xapka.at[i,"profit"] = (buyPrice - xapka.at[i,"close"])/buyPrice
            #print(BuySellway +'Sell_'+str(xapka.at[i, "date"])[5:10]+'_profit= '+str( xapka.at[i,"profit"].round(3)))
            a = [Ticker, xapka.at[i-1,"buy"], Buydate, xapka.at[i, "date"], round(buyPrice, 3), round(xapka.at[i,"close"], 3), round(xapka.at[i,"profit"], 3), CurrDateTime]
            TredRoc = pd.concat([TredRoc, pd.DataFrame([a])], ignore_index=True)            
            BuySellway =''
        else:
            #xapka.at[i,"Sell"] = xapka.at[i-1,"Sell"]
            xapka.at[i,"buy"]  = xapka.at[i-1,"buy"]

    EndDate = len(xapka)
    init = total =100.0
    count = 0
    for i in range(1,EndDate):
        if xapka.at[i,"profit"] != 0:
            count = count +1
            total = total + total*xapka.at[i,"profit"]
    print( Ticker, "From [" + str(xapka.at[1,"date"]) +"] to ["+ str(xapka.at[len(xapka)-1,"date"]) +"] total =1000.0 after count: ["+str(count)+"] times total profit = "+str(round(total,3)) )
    

    mtime = os.path.getmtime('D:\\Stock_bk\\Trade.py') #修改时间
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
    if (CurrDateTime.day >= 1 and CurrDateTime.day <= 3) or (CurrDateTime.day >= 15 and CurrDateTime.day <= 17):
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
        xBBand = xapka.at[i,"xBBand"]
        prebuy  = xapka.at[i-1,"buy"]
        
        if prebuy ==0:
            if   xBBand ==2:
                return 1
            #elif xBBand ==-2:
            #    return -1               
        else:
            return 0
        
    def BbToSell(i):
        xBBand  = xapka.at[i,"xBBand"]
        Prebuy = xapka.at[i-1,"buy"]      
        if   xBBand  <0 and Prebuy == 1:
            return 1
        elif xBBand  >0 and Prebuy == -1:
            return -1
        else:
            return 0
#---------------------------------------------------------------------------
    def MacdToBuy(i):
        xema   = xapka.at[i,"xema"] 
        yema   = xapka.at[i,"yema"] 
        xmacd  = xapka.at[i,"xmacd"]
        Prebuy = xapka.at[i-1,"buy"] 
        if Prebuy ==0:
            if   xmacd > xmacd_1 and xmacd_1== -1 :
                return 1
            #elif xBBand ==-2:
            #    return -1               
        else:
            return 0
        
    def MacdToSell(i):
        xema   = xapka.at[i,"xema"] 
        yema   = xapka.at[i,"yema"] 
        xmacd  = xapka.at[i,"xmacd"]
        Prebuy = xapka.at[i-1,"buy"]   
        if   xmacd < xmacd_1 and xmacd_1== 2 and Prebuy == 1:
            return 1
        #elif xmacd < xmacd_1 and xmacd_1== 2:
        #    return -1
        else:
            return 0