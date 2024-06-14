#apka_score_oscillate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Trade

def score_oscillate(data):
    xapka = pd.DataFrame()
    for j in range(10,len(data)):
        try:        
            #===========================================================================================
            RsiSlop = (data.at[j,'fastk_d']- data.at[j-1,'fastk_d'])
            wRsiSlop = (data.at[j,'fastk_w']- data.at[j-1,'fastk_w'])
            
            if data.at[j,'fastk_w'] > data.at[j,'fastd_w'] and data.at[j,'fastd_w'] < 20 and data.at[j,'fastk_w'] <20:
                xsrsi = 1                
                for k in range(j-10,j): 
                    if  data.at[k, 'fastk_d'] < data.at[k, 'fastd_d'] and  data.at[k, 'fastd_d'] < 20:
                        xsrsi = 2
                        if wRsiSlop>0: 
                            xsrsi = 3
            elif data.at[j,'fastk_w'] < data.at[j,'fastd_w'] and data.at[j,'fastd_w'] > 80 and data.at[j,'fastk_w'] >80:
                xsrsi = -1
                for k in range(j-10,j): 
                    if data.at[k, 'fastk_d'] > data.at[k, 'fastd_d'] and  data.at[k, 'fastd_d'] > 90:
                        xsrsi = -2
                        if wRsiSlop<0: 
                            xsrsi = -3                        
            else:
                xsrsi = 0

            '''
            if data.at[j, 'fastk_d'] > data.at[j, 'fastd_d'] and data.at[j, 'fastd_d'] < 20 :
                xsrsi = 1
                for k in range(j-10,j): 
                    if  data.at[k, 'fastk_w'] < data.at[k, 'fastd_w'] and  data.at[k, 'fastd_w'] < 20:
                        xsrsi = 2
            elif data.at[j, 'fastk_d'] < data.at[j, 'fastd_d'] and data.at[j, 'fastd_d'] > 90:
                xsrsi = -1
                for k in range(j-10,j): 
                    if data.at[k, 'fastk_w'] > data.at[k, 'fastd_w'] and  data.at[k, 'fastd_w'] > 90:
                        xsrsi = -2
            else:
                xsrsi = 0
            '''
            
            #===========================================================================================
            wSlop_d = (data.at[j,'willrd'] + data.at[j-1,'willrd'] + data.at[j-2,'willrd'] )/3
            wSlop_w = data.at[j,'willrw'] - data.at[j-1,'willrw']
            if data.at[j, 'willrd'] < -90 and wSlop_d <-90: 
                xwillrd = 1
                if data.at[j, 'willrw'] <-90:
                    xwillrd = 2
                    if data.at[j, 'willrd'] > data.at[j, 'willrw']:
                        xwillrd = 3
            elif data.at[j, 'willrd'] > -10  and wSlop_d >-10:
                xwillrd = -1
                if  data.at[j, 'willrw'] >-10:
                    xwillrd = -2
                    if data.at[j, 'willrd'] < data.at[j, 'willrw']:
                        xwillrd = -3
            else:
                xwillrd = 0
            '''
            if data.at[j, 'willrd'] < -90 and wSlop_d <-90: 
                xwillrd = 1
                if data.at[j, 'willrw'] <-90:
                    xwillrd = 2
            elif data.at[j, 'willrd'] > -10  and wSlop_d >-10:
                xwillrd = -1
                if  data.at[j, 'willrw'] >-10:
                    xwillrd = -2
            else:
                xwillrd = 0            
            '''

            #===========================================================================================
            #"upp_d","mid_d","low_d","upp_w","mid_w","low_w","upp_m","mid_m","low_m"
            # (data.at[j, 'high'] - data.at[j, 'mid_d'])/(data.at[j, 'upp_d'] - data.at[j, 'mid_d']) > 0.9
            def Exup(k):
                return data.at[j-k, 'high'] - data.at[j-k, 'upp_d']            
            def ExDn(k):
                return data.at[j-k, 'low'] - data.at[j-k, 'low_d']

            BandWidth = (data.at[j, 'upp_d'] - data.at[j, 'low_d'])+1e-15
            level     = (data.at[j, 'close'] - data.at[j, 'low_d'])/BandWidth

            wBandWidth = (data.at[j, 'upp_w'] - data.at[j, 'low_w'])+1e-15
            wlevel     = (data.at[j, 'close'] - data.at[j, 'low_w'])/wBandWidth
            if level >0.8: 
                xBBand = -1
                if wlevel >0.8:
                    xBBand = -2                
                    if Exup(0)>0 or Exup(1)>0 or Exup(2)>0 :
                        xBBand = -3 
            elif level < 0.2:
                xBBand = 1
                if wlevel < 0.2:
                    xBBand = 2
                    if Exup(0) <0 or Exup(-1) <0 or Exup(2) <0:
                        xBBand = 3
            else:
                xBBand = 0
            '''
            if  data.at[j, 'low'] < data.at[j, 'low_d'] and data.at[j-1, 'low'] > data.at[j-1, 'low_d']: 
                xBBand = 1
                if data.at[j, 'low'] < data.at[j, 'low_w'] :
                    xBBand = 2   
            if  data.at[j, 'high'] > data.at[j, 'upp_d'] and data.at[j-1, 'close'] < data.at[j-1, 'upp_d']: 
                xBBand = -1
                if data.at[j, 'high'] > data.at[j, 'upp_w'] :
                     xBBand = -2
            else:
                xBBand = 0

            '''
            sum= xBBand+xsrsi+xwillrd    
            #===========================================================================================
            a=[ data.at[j,'date'],data.at[j,'close'], xsrsi, xwillrd,xBBand, sum, level.round(3), 0, 0, 0.0]
            xapka = pd.concat([xapka, pd.DataFrame([a])], ignore_index=True)                
        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)                   

    xapka.columns = ["date", "close", "xsrsi", "xwillrd", "xBBand", "OscSum", "BBlevel","buy", "sell", "profit"]
    return xapka
    '''
    fig = plt.figure(num =1, figsize=(18,9))    #創建圖表
    sub1 = fig.add_subplot(2, 1, 1) # 添加子圖表1
    sub2 = fig.add_subplot(2, 1, 2) # 添加子圖表2
    sub1.plot(xapka["date"],xapka["close"],label="close" ,color = 'blue')        
    sub2.plot(xapka["date"],xapka["sum"], label="sum" , linewidth = 1, linestyle = '-' ,color = 'red')
    sub2.plot(xapka["date"],xapka["xsrsi"],label="xsrsi" , linewidth = 1, linestyle = '-.',color = 'orange') 
    sub2.plot(xapka["date"],xapka["xwillrd"],label="xwillrd" , linewidth = 1, linestyle = '--',color = 'green')
    sub2.plot(xapka["date"],xapka["xBBand"],label="xBBand" , linewidth = 1, linestyle = '-.',color = 'blue')
    #決策進出場
    for i in range(1,len(xapka)):
        if xapka.at[i, "sum"] >=5 :
            sub1.text(xapka.at[i, "date"], xapka.at[i, "close"],str(xapka.at[i, "date"])[5:10],rotation=90,color='blue')
            sub2.text(xapka.at[i, "date"], xapka.at[i, "sum"],str(xapka.at[i, "date"])[5:10],rotation=90,color='blue')
        elif xapka.at[i, "sum"] <=-5:
            sub1.text(xapka.at[i, "date"],xapka.at[i, "close"],str(xapka.at[i, "date"])[5:10],rotation=90,color='red')
            sub2.text(xapka.at[i, "date"], xapka.at[i, "sum"],str(xapka.at[i, "date"])[5:10],rotation=90,color='red') 
    
    buy = 0.0
    BuySellway =''
    for i in range(1,len(xapka)):
        if xapka.at[i,"xsrsi"] + xapka.at[i,"xsrsi"] + xapka.at[i,"xsrsi"] >3 :
            sub2.text(xapka.at[i, "date"], 1,str(xapka.at[i, "date"])[5:10],color='green')
            xapka.at[i,"buy"] =1
            buy = xapka.at[i,"close"]
            BuySellway = BuySellway +'Buy_'+str(xapka.at[i, "date"])[5:10]+'=>' 
        elif xapka.at[i,"xmacd"] <0 and xapka.at[i-1,"xmacd"]>=0:
            sub2.text(xapka.at[i, "date"],-1,str(xapka.at[i, "date"])[5:10],color='black') 
            xapka.at[i,"Sell"] =1
            xapka.at[i,"profit"] = (xapka.at[i,"close"] - buy)/buy
            #print(BuySellway +'Sell_'+str(xapka.at[i, "date"])[5:10]+'_profit= '+str(xapka.at[i,"profit"].round(3)))
            BuySellway ='' 
    total =1000.0
    count = 0
    EndDate = len(xapka)
    for i in range(1,len(xapka)):
        if xapka.at[i,"profit"] != 0:
            count = count +1
            total = total + total*xapka.at[i,"profit"]
    print("From [" + str(xapka.at[1,"date"]) +"] to ["+ str(xapka.at[len(xapka)-1,"date"]) +"] total =1000.0 after count: []"+str(count)+"] times total profit = "+str(total) )
    
    
    
    #Trade.TotProfit(xapka)

    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    plt.legend() 
    plt.show()
    '''