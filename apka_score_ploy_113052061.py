import numpy as np
import matplotlib.pyplot as plt

color_list = [
    'black','sienna','red','orange','gold','green','blue','purple','grey','teal','black','sienna','red','orange','gold','green','blue','purple','grey','teal'
] 

def plot(xapka):
    xapka.columns = ["date", "close", "xema", "xmacd", "xsrsi", "xwillrd", "xBBand","total", "xploy"]
    fig = plt.figure(num =1, figsize=(18,9))    #創建圖表
    sub1 = fig.add_subplot(3, 1, 1) # 添加子圖表1
    sub2 = fig.add_subplot(3, 1, 2) # 添加子圖表2
    sub3 = fig.add_subplot(3, 1, 3) # 添加子圖表2
    sub1.plot(xapka["date"],xapka["close"],  label="close"   ,color = 'blue') 
    sub3.plot(xapka["date"],xapka["xema"],   label="xema"    , linewidth = 0.5, linestyle = '-' ,color = 'red') 
    sub3.plot(xapka["date"],xapka["xmacd"],  label="xmacd"   , linewidth = 0.5, linestyle = '--',color = 'green')  
    sub3.plot(xapka["date"],xapka["xsrsi"],  label="xsrsi"   , linewidth = 1,linestyle = '-',color = 'brown') 
    sub3.plot(xapka["date"],xapka["xwillrd"],label="xwillrd" , linewidth = 1,linestyle = '--',color = 'black')  
    sub2.plot(xapka["date"],xapka["xBBand"] ,label="xBBand"  , linewidth = 1,linestyle = '-.',color = 'indigo') 
    sub2.plot(xapka["date"],xapka["total"]  ,label="total"   , linewidth = 1,linestyle = ':' ,color = 'purple')
    for i in range(1,len(xapka)):
        if xapka.at[i,"total"] >=4 :
            sub1.text(xapka.at[i, "date"], xapka.at[i, "close"]+5, str(xapka.at[i, "date"])[5:10] ,color='red')
        elif xapka.at[i,"total"] <= -4 :
            sub1.text(xapka.at[i, "date"],xapka.at[i, "close"]-5,str(xapka.at[i, "date"])[5:10] ,color='blue')
        if xapka.at[i,"xsrsi"] >=2 :
            sub3.text(xapka.at[i, "date"], xapka.at[i,"xsrsi"],str(xapka.at[i, "date"])[5:10],color='red')
        elif xapka.at[i,"xsrsi"] <= -2 :
            sub3.text(xapka.at[i, "date"],xapka.at[i,"xsrsi"],str(xapka.at[i, "date"])[5:10],color='blue') 
        if xapka.at[i,"xmacd"] >0 and xapka.at[i-1,"xmacd"]<=0:
            sub1.text(xapka.at[i, "date"], xapka.at[i, "close"]+5,'+'+str(xapka.at[i, "date"])[5:10],color='green')
        elif xapka.at[i,"xmacd"] <0 and xapka.at[i-1,"xmacd"]>=0:
            sub1.text(xapka.at[i, "date"],xapka.at[i, "close"]-5,'-'+str(xapka.at[i, "date"])[5:10],color='black')      

    ## 設定x軸和y軸的範圍空間
    #plt.xlim((-1, 2.5))
    ## 設定x軸與y軸標籤名稱
    #plt.xticks(xapka["date"])
    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    plt.legend() 
    plt.show()
    
