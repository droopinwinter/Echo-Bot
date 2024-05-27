#apka_score_tred
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Trade

def score_trend(data):
    xapka = pd.DataFrame()
    for j in range(10,len(data)):
        try:      
            #利用EMA和MACD判斷長週期上升趨勢做多或空
            if data.at[j, 'ema1'] > data.at[j, 'ema2'] and data.at[j, 'ema2'] >= data.at[j-1, 'ema2']:
                xema =1 
                if data.at[j, 'ema2'] > data.at[j, 'ema3']:
                    xema =2
                    if data.at[j, 'ema3'] > data.at[j, 'ema4']:
                        xema =3
                        if data.at[j, 'ema4'] > data.at[j, 'ema5']:
                            xema =4
            elif data.at[j, 'ema1'] < data.at[j, 'ema2'] and data.at[j, 'ema2'] <= data.at[j-1, 'ema2']:
                xema =-1 
                if data.at[j, 'ema2'] < data.at[j, 'ema3']:
                    xema =-2
                    if data.at[j, 'ema3'] < data.at[j, 'ema4']:
                        xema =-3
                        if data.at[j, 'ema4'] < data.at[j, 'ema5']:
                            xema =-4
            else:
                xema = 0 #無法識別走勢<持倉或觀望不操作
            #短線判斷進出場信號
                
            #xema = apka_score_index.score_ema(data.iloc[j-10:j,:])
            if  data.at[j, 'MACD_d'] > data.at[j, 'signal_d'] and data.at[j, 'signal_d'] >= data.at[j-1, 'signal_d']:
                xmacd =1
                if data.at[j, 'MACD_d'] > 0:
                    xmacd =2
                    if data.at[j-1, 'MACD_w'] > data.at[j-1, 'signal_w']:
                        xmacd =3 
                        if data.at[j, 'MACD_w'] > 0:
                            xmacd =4                       
            elif data.at[j, 'MACD_d'] < data.at[j, 'signal_d'] and data.at[j, 'signal_d'] <= data.at[j-1, 'signal_d']:
                xmacd =-1
                if data.at[j, 'MACD_d'] < 0:
                    xmacd =-2
                    if data.at[j-1, 'MACD_w'] < data.at[j-1, 'signal_w']:
                        xmacd =-3
                        if data.at[j, 'MACD_w'] < 0:
                            xmacd =-4  
            else:
                xmacd =0


            xstate =(data.at[j,"ema3"] - data.at[j-1,"ema3"]) + (data.at[j,"ema3"] - data.at[j-2,"ema3"])

            a=[ data.at[j,'date'],data.at[j,'close'], xema, xmacd, xstate, 0, 0, 0.0]
            xapka = pd.concat([xapka, pd.DataFrame([a])], ignore_index=True)                
        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)                   

    xapka.columns = ["date", "close", "xema", "xmacd", "TrnSlop", "buy", "sell", "profit"] 
    return xapka
    '''
    fig = plt.figure(num =1, figsize=(18,9))    #創建圖表
    sub1 = fig.add_subplot(2, 1, 1) # 添加子圖表1
    sub2 = fig.add_subplot(2, 1, 2) # 添加子圖表2
    sub1.plot(xapka["date"],xapka["close"],label="close" ,color = 'blue')        
    sub2.plot(xapka["date"],xapka["xema"],label="xema" , linewidth = 0.5, linestyle = '-' ,color = 'red') 
    sub2.plot(xapka["date"],xapka["xmacd"],label="xmacd" , linewidth = 0.5, linestyle = '--',color = 'green')
    #決策進出場
    buy = 0.0
    BuySellway =''
    for i in range(1,len(xapka)):
        if xapka.at[i,"xmacd"] >0 and xapka.at[i-1,"xmacd"]<=0:
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
    
    Trade.TotProfit(xapka)

    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    plt.legend() 
    plt.show()
    
    '''
