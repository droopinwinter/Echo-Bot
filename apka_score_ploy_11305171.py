import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

ColoLst =['black','sienna','red','orange','gold','green','blue','purple','grey','teal','black','sienna','red','orange','gold','green','blue','purple','grey','teal'] 

def plot(xapka, xcode):
    #xapka.columns = ["date", "close", "xema", "xmacd", "xsrsi", "xwillrd", "xBBand","sum", "xploy"]
    #print(xapka.head())
    #date       close  xema  xmacd  TrnSum  xsrsi  xwillrd  xBBand  OscSum  buy  sell  profit  EamCnt  EmaState  yema  xcmb
    fig = plt.figure(num =1, figsize=(18,9))    #創建圖表
    sub1 = fig.add_subplot(2, 1, 1) # 添加子圖表1
    sub2 = fig.add_subplot(2, 1, 2) # 添加子圖表2
    #sub3 = fig.add_subplot(3, 1, 3) # 添加子圖表2
    sub1.plot(xapka["date"],xapka["close"],  label="close"   ,color = 'blue') 
    sub1.grid()
    plt.legend(loc =2)
    plt.title('Ticker='+xcode+StrTime) 
    sub2.plot(xapka["date"],xapka["xema"],   label="xema"    , linewidth = 0.5, linestyle = '-' ,color = 'red') 
    sub2.plot(xapka["date"],xapka["xmacd"],  label="xmacd"   , linewidth = 0.5, linestyle = '--',color = 'teal')
    sub2.plot(xapka["date"],xapka["yema"],  label="yema"   , linewidth = 0.5, linestyle = '--',color = 'sienna')
    sub2.plot(xapka["date"],xapka["xcmb"],  label="xcmb"   , linewidth = 2, linestyle = '--',color = 'orange')  
    #sub2.plot(xapka["date"],xapka["xsrsi"],  label="xsrsi"   , linewidth = 1,linestyle = '-',color = 'brown') 
    #sub2.plot(xapka["date"],xapka["xwillrd"],label="xwillrd" , linewidth = 1,linestyle = '--',color = 'black')  
    sub2.plot(xapka["date"],xapka["OscSum"] ,label="OscSum"  , linewidth = 1,linestyle = '-.',color = 'indigo') 
    
    
    for i in range(1,len(xapka)):
        Yaxis   = xapka.at[i, "close"]
        Xaxis   = xapka.at[i, "date"]
        Xbuy    = xapka.at[i, "buy"]
        Pbuy    = xapka.at[i-1, "buy"]
        Xclose  = str(xapka.at[i, "close"].round(2))
        Xprofit = str( xapka.at[i,"profit"].round(3))
        if xapka.at[i,"buy"] >=1 and xapka.at[i-1,"buy"] ==0:
            Yaxis =  Yaxis*0.99
            sub1.text(Xaxis, Yaxis,str(Xbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose,rotation=90,color='red')
            sub2.text(Xaxis, 7    ,str(Xbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose,color='red')
        elif xapka.at[i,"buy"] ==0 and xapka.at[i-1,"buy"] >=1:
            Yaxis =  Yaxis*1.01            
            sub1.text(Xaxis,Yaxis,str(Pbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose+'_'+Xprofit,rotation=90,color='blue')
            sub2.text(Xaxis,-6  ,str(Pbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose+'_'+Xprofit,color='blue')
        elif xapka.at[i,"buy"] <=-1 and xapka.at[i-1,"buy"] ==0:
            Yaxis =  Yaxis*1.01            
            sub1.text(Xaxis,Yaxis,str(Xbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose,rotation=90,color='black')
            sub2.text(Xaxis,5    ,str(Xbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose,color='black')
        elif xapka.at[i,"buy"] ==0 and xapka.at[i-1,"buy"] <=-1:
            Yaxis =  Yaxis*0.99            
            sub1.text(Xaxis,Yaxis,str(Pbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose+'_'+Xprofit,rotation=90,color='sienna')
            sub2.text(Xaxis,-5   ,str(Pbuy)+'_'+str(Xaxis)[5:10]+'\n'+Xclose+'_'+Xprofit,color='sienna')
        '''
        if xapka.at[i,"xmacd"] >0 and xapka.at[i-1,"xmacd"]<=0:
            Yaxis =  Yaxis*1.02
            sub1.text(Xaxis, Yaxis,'+C'+str(Xaxis)[5:10],rotation=90,color='orange')
        elif xapka.at[i,"xmacd"] <0 and xapka.at[i-1,"xmacd"]>=0:
            Yaxis =  Yaxis*0.95
            sub1.text(Xaxis,Yaxis,'-C'+str(Xaxis)[5:10],rotation=90,color='purple')      
        
        if xapka.at[i,"yema"] >xapka.at[i-1,"yema"]:
            TrenBuy = xapka.at[i, "date"] 
            sub1.text(TrenBuy, xapka.at[i, "close"],'+'+str(xapka.at[i, "EamCnt"])+'_'+str(TrenBuy)[5:10],rotation=90,color=ColoLst[0])
        elif xapka.at[i,"yema"] <xapka.at[i-1,"yema"]:
            TrenSell = xapka.at[i, "date"]
            sub1.text(TrenSell,xapka.at[i, "close"],'-'+str(xapka.at[i, "EamCnt"])+'_'+str(TrenSell)[5:10],rotation=90,color=ColoLst[1]) 

        '''

    ## 設定x軸和y軸的範圍空間
    #plt.xlim((-1, 2.5))
    ## 設定x軸與y軸標籤名稱
    #plt.xticks(xapka["date"])
    
    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    plt.grid() 
    plt.legend()
    t = datetime.now()
    StrTime = t.strftime("_%Y-%m-%d_%H_%M_%S")
    plt.title('Ticker='+xcode+StrTime) 
    plt.savefig('..\\PlotImg\\'+xcode+ StrTime+'.png')
    #plt.show()
    
