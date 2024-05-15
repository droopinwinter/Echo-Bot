#Trade

def TotProfit(xapka):

    def ToBuy(i):
        if   xapka.at[i,"xcmb"] >=  6:
            return 1
        elif xapka.at[i,"xcmb"] <= -6:
            return -1
        else:
            return 0
        
    def ToSell(i):
        if   xapka.at[i,"xcmb"] == 0 and xapka.at[i-1,"xcmb"] > 0:
            return 1
        elif xapka.at[i,"xcmb"] == 0 and xapka.at[i-1,"xcmb"] < 0:
            return -1
        else:
            return 0
        
    buyPrice = 0.0
    BuySellway =''
    EndDate = len(xapka)

    for i in range(1,len(xapka)):
        if ToBuy(i) ==1:
            xapka.at[i,"buy"] =1
            buyPrice = xapka.at[i,"close"]
            BuySellway = BuySellway +'+Buy_'+str(xapka.at[i, "date"])[5:10]+' => ' 
        elif ToBuy(i) ==-1:
            xapka.at[i,"buy"] =-1
            buyPrice = xapka.at[i,"close"]
            BuySellway = BuySellway +'-Buy_'+str(xapka.at[i, "date"])[5:10]+' => '             
        elif ToSell(i)==1:
            xapka.at[i,"Sell"] =1
            xapka.at[i,"profit"] = (xapka.at[i,"close"] - buyPrice)/buyPrice
            print(BuySellway +'Sell_'+str(xapka.at[i, "date"])[5:10]+'_profit= '+str( xapka.at[i,"profit"].round(3)))
            BuySellway =''
        elif ToSell(i)==-1:
            xapka.at[i,"Sell"] =-1
            xapka.at[i,"profit"] = (buyPrice - xapka.at[i,"close"])/buyPrice
            print(BuySellway +'Sell_'+str(xapka.at[i, "date"])[5:10]+'_profit= '+str( xapka.at[i,"profit"].round(3)))
            BuySellway =''

    total =1000.0
    count = 0
    for i in range(1,EndDate):
        if xapka.at[i,"profit"] != 0:
            count = count +1
            if xapka.at[i,"Sell"] ==1:
                total = total + total*xapka.at[i,"profit"]
            elif xapka.at[i,"Sell"] ==-1:
                total = total - total*xapka.at[i,"profit"]
    print("From [" + str(xapka.at[1,"date"]) +"] to ["+ str(xapka.at[len(xapka)-1,"date"]) +"] total =1000.0 after count: []"+str(count)+"] times total profit = "+str(round(total,3)) )