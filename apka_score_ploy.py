import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

ColoLst =['black','sienna','red','orange','gold','green','blue','purple','grey','teal','black','sienna','red','orange','gold','green','blue','purple','grey','teal'] 

def plot(xapka, xcode):
    #xapka.columns = ["date", "close", "xema", "xmacd", "xsrsi", "xwillrd", "xBBand","sum", "xploy"]
    #print(xapka.head())
    #date       close  xema  xmacd  TrnSum  xsrsi  xwillrd  xBBand  OscSum  buy  sell  profit  EamCnt  EmaState  yema  xcmb
    fig = plt.figure(num =1, figsize=(18,9))    #創建圖表
    plt.subplot(2, 1, 1) # 添加子圖表1
    t = datetime.now()
    StrTime = t.strftime("_%Y-%m-%d_%H_%M_%S")
    plt.title('Ticker='+xcode+StrTime)
    plt.plot(xapka["date"],xapka["close"],  label=xcode , linewidth = 1, linestyle = '-'  ,color = 'blue')
    plt.plot(xapka["date"],xapka["close"] + 10*xapka["xmacd"],  label="xmacd"   , linewidth = 0.5, linestyle = '--',color = 'teal')  
    plt.plot(xapka["date"],xapka["close"] + 15*xapka["xema"],  label="xema"   , linewidth = 0.5, linestyle = '--',color = 'red')  
    plt.grid()
    plt.legend(loc =2)
    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    for i in range(1,len(xapka)):
        Yaxis   = xapka.at[i, "close"]
        Xaxis   = xapka.at[i, "date"]
        Xbuy    = xapka.at[i, "buy"]
        Pbuy    = xapka.at[i-1, "buy"]
        sPrice  = xapka.at[0, "close"]
        Xclose  = str(xapka.at[i, "close"].round(2))
        Xprofit =  xapka.at[i,"profit"].round(3)
        if xapka.at[i,"buy"] >=1 and xapka.at[i-1,"buy"] ==0:
            Yaxis =  Yaxis*0.99
            plt.text(Xaxis, sPrice,str(Xbuy)+'_'+str(Xaxis)[5:10]+'_'+Xclose,rotation=90,color='red')
            plt.plot([Xaxis,Xaxis], [sPrice, Yaxis],color='red')
        elif xapka.at[i,"buy"] ==0 and xapka.at[i-1,"buy"] >=1:
            Yaxis =  Yaxis*1.01
            if Xprofit>0:
                hmove = 20
            else:
                hmove = 0
            plt.text(Xaxis,sPrice+hmove,str(Pbuy)+'_'+str(Xaxis)[5:10]+'_'+Xclose+'_'+str(Xprofit),rotation=90,color='blue')
            plt.plot([Xaxis,Xaxis], [sPrice, Yaxis],color='blue')
        elif xapka.at[i,"buy"] <=-1 and xapka.at[i-1,"buy"] ==0:
            Yaxis =  Yaxis*1.01            
            plt.text(Xaxis,sPrice,str(Xbuy)+'_'+str(Xaxis)[5:10]+'_'+Xclose,rotation=90,color='black')
            plt.plot([Xaxis,Xaxis], [sPrice, Yaxis],color='black')
        elif xapka.at[i,"buy"] ==0 and xapka.at[i-1,"buy"] <=-1:
            Yaxis =  Yaxis*0.99
            if Xprofit>0:
                hmove = 20
            else:
                hmove = 0            
            plt.text(Xaxis,sPrice+hmove,str(Pbuy)+'_'+str(Xaxis)[5:10]+'_'+Xclose+'_'+str(Xprofit),rotation=90,color='sienna')
            plt.plot([Xaxis,Xaxis], [sPrice, Yaxis],color='sienna')



    plt.subplot(2, 1, 2) # 添加子圖表2
    #plt.plot(xapka["date"],xapka["xcmb"],   label="xcmb"    , linewidth = 1, linestyle = '-' ,color = 'red') 
    #plt.plot(xapka["date"],xapka["xmacd"],  label="xmacd"   , linewidth = 1, linestyle = '--',color = 'teal') 
    plt.plot(xapka["date"],xapka["yema"],  label="yema"   , linewidth = 1, linestyle = '--',color = 'sienna')
    #plt.plot(xapka["date"],xapka["xcmb"],  label="xcmb"   , linewidth = 2, linestyle = '--',color = 'orange')  
    #sub2.plot(xapka["date"],xapka["xsrsi"],  label="xsrsi"   , linewidth = 1,linestyle = '-',color = 'brown') 
    #sub2.plot(xapka["date"],xapka["xwillrd"],label="xwillrd" , linewidth = 1,linestyle = '--',color = 'black')  
    plt.plot(xapka["date"],xapka["OscSum"] ,label="OscSum"  , linewidth = 1,linestyle = '-.',color = 'indigo') 
    
    for i in range(1,len(xapka)):
        Xaxis   = xapka.at[i, "date"]
        Xbuy    = xapka.at[i, "buy"]
        Pbuy    = xapka.at[i-1, "buy"]
        Xclose  = str(xapka.at[i, "close"].round(2))
        iXprofit = xapka.at[i,"profit"].round(3)
        sXprofit = str( iXprofit )
        if iXprofit>0:
            hmove = 8
        else:
            hmove = 0
        if xapka.at[i,"buy"] >=1 and xapka.at[i-1,"buy"] ==0:
            plt.text(Xaxis, -5    ,str(Xbuy)+'_'+str(Xaxis)[5:10],rotation=90,color='red')
            plt.plot([Xaxis,Xaxis], [-6, -4],color='red')
        elif xapka.at[i,"buy"] ==0 and xapka.at[i-1,"buy"] >=1:
            plt.text(Xaxis,-6+hmove  ,str(Pbuy)+'_'+str(Xaxis)[5:10]+'_'+sXprofit,rotation=90,color='blue')
            plt.plot([Xaxis,Xaxis], [-6, -4],color='blue')
        elif xapka.at[i,"buy"] <=-1 and xapka.at[i-1,"buy"] ==0:
            plt.text(Xaxis,-5    ,str(Xbuy)+'_'+str(Xaxis)[5:10],rotation=90,color='black')
            plt.plot([Xaxis,Xaxis], [-6, -4],color='black')
        elif xapka.at[i,"buy"] ==0 and xapka.at[i-1,"buy"] <=-1:
            plt.text(Xaxis,-5+hmove ,str(Pbuy)+'_'+str(Xaxis)[5:10]+'_'+sXprofit,rotation=90,color='sienna')
            plt.plot([Xaxis,Xaxis], [-6, -4],color='sienna')
    


    ## 設定x軸和y軸的範圍空間
    #plt.xlim((-1, 2.5))
    ## 設定x軸與y軸標籤名稱
    #plt.xticks(xapka["date"])
    
    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    plt.grid() 
    plt.legend()
    plt.savefig('..\\PlotImg\\'+xcode+ StrTime+'.png')
    plt.show()
    
