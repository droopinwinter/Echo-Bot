#Trade
import pandas as pd


def TotProfit(xapka, Ticker, CurrDateTime):

    def Xtred(i):
        xtred = 0
        for j in range(1,5):
            xtred +=(xapka.at[i-j+1,"xmacd"] - xapka.at[i-j,"xmacd"])
        return xtred    
            
    def ToBuy(i, xtred):
        xema  = xapka.at[i,"xema"] 
        yema  = xapka.at[i,"yema"] 
        xmacd = xapka.at[i,"xmacd"]
        OscSum= xapka.at[i,"OscSum"]
        xTrnSlop  = xapka.at[i,"TrnSlop"]
        prebuy  = xapka.at[i-1,"buy"]
        if prebuy ==0:
            if  ( OscSum==8 or (OscSum <  6 and xapka.at[i-1,"OscSum"] == 6 ) \
                 or ( OscSum < 4 and xapka.at[i-1,"OscSum"] == 4 ) )and (xmacd <-2 or xema<-2) :
                xapka.at[i,"buySig"] =10
                return 10 #+極端交易
            #elif ( OscSum < 4 and xapka.at[i-1,"OscSum"] == 4 ) and xmacd <=-1:
            #    return 11 #+極端交易
            #elif OscSum <= -6 and xmacd >=4 and xema >=4 and xTrnSlop<=0:
            #    return -11            
            elif  yema > xapka.at[i-1,"yema"]  and yema >0 :
                xapka.at[i,"buySig"] =yema
                return yema  #+GMMA交易                        
            #elif yema < xapka.at[i-1,"yema"] and yema <=-1 and xema <0 and xTrnSlop<=0:
            #    xapka.at[i,"buySig"] =yema
            #    return yema #-GMMA交易
            elif xmacd >0 and xapka.at[i-1,"xmacd"] <=0   and xTrnSlop>0:
                xapka.at[i,"buySig"] =20
                return 20 #+趨勢交易
            elif  xmacd <0 and xapka.at[i-1,"xmacd"] >=0 and xTrnSlop<-0.1:
                xapka.at[i,"buySig"] =-20
                return -20            
        else:
            return 0
        
    def ToSell(i, xtred):
        xema   = xapka.at[i,"xema"] 
        yema   = xapka.at[i,"yema"] 
        xmacd  = xapka.at[i,"xmacd"]
        OscSum = xapka.at[i,"OscSum"]
        xTrnSlop  = xapka.at[i,"TrnSlop"]
        xstate = xapka.at[i,"xstate"]
        Prebuy = xapka.at[i-1,"buy"]
        xlevel = xapka.at[i-1,"BBlevel"]
        if   Prebuy == 10 and (xmacd == 4 or (OscSum<=-1 and xmacd <0) )  :
            xapka.at[i,"SellSig"] =110  
            return Prebuy #+極端交易
        elif Prebuy == 11 and OscSum == 0 :
            xapka.at[i,"SellSig"] =111
            return Prebuy #+極端交易
        elif Prebuy == -11 and OscSum == 0 :
            xapka.at[i,"SellSig"] =-110
            return Prebuy  #-極端交易      
        elif Prebuy < 0 and Prebuy > -10 and ( yema > xapka.at[i-1,"yema"] or xmacd > xapka.at[i-1,"xmacd"]):
            xapka.at[i,"SellSig"] =Prebuy-100
            return Prebuy #-GMMA交易
        elif Prebuy > 0   and Prebuy < 10 and(yema < xapka.at[i-1,"yema"] or xmacd < xapka.at[i-1,"xmacd"] ): #and Prebuy == xapka.at[i-1,"yema"]
            xapka.at[i,"SellSig"] =Prebuy+100
            return Prebuy #+GMMA交易
        elif Prebuy ==20  and (OscSum <=-6 or (xmacd < xapka.at[i-1,"xmacd"] ) \
                               or (xema < xapka.at[i-1,"xema"] ) ) :     
            xapka.at[i,"SellSig"] =Prebuy+100
            return Prebuy #+趨勢交易
        elif Prebuy ==-20  and ( OscSum >=3 or (xmacd > xapka.at[i-1,"xmacd"] and  xmacd<=0 ) or (xema > xapka.at[i-1,"xema"] and  xema <=0))  :     
            xapka.at[i,"SellSig"] =Prebuy-100
            return Prebuy        
        else:
            return 0


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
            if   xmacd > xapka.at[i-1,"xmacd"] and xapka.at[i-1,"xmacd"]== -1 :
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
        if   xmacd < xapka.at[i-1,"xmacd"] and xapka.at[i-1,"xmacd"]== 2 and Prebuy == 1:
            return 1
        #elif xmacd < xapka.at[i-1,"xmacd"] and xapka.at[i-1,"xmacd"]== 2:
        #    return -1
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
    a = [Ticker+'_Total', 0, xapka.at[1,"date"], xapka.at[len(xapka)-1,"date"], init, count, round(total,3),CurrDateTime]
    TredRoc = pd.concat([TredRoc, pd.DataFrame([a])], ignore_index=True)
    TredRoc.columns = ["Ticker","LongShort","Buydate","Selldate","buyPrice","SellPrice","profit", "CreatDate"]
    return TredRoc
    #TredRoc.to_csv('TredRocord_'+Ticker+'.csv')     
    