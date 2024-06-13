#apka_score_EMA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def EmaStateMaChing( ema1, ema2, high, low, PreSt):
    if ema1> ema2:
        if PreSt>=2 and low < ema2:
            PreSt = 0
        if PreSt%2 ==0 and low > ema1 :
            PreSt = PreSt+1
        if PreSt%2 ==1 and low > ema2 and low < ema1:
            PreSt = PreSt+1
    elif ema1 < ema2: 
        if PreSt>=2 and high > ema2:
            PreSt = 0
        if PreSt%2 ==0 and high < ema1 :
            PreSt = PreSt+1
        if PreSt%2 ==1 and high > ema1 and high < ema2:
            PreSt = PreSt+1
    return PreSt

def PutOrCall( NowWaveSt, PreWaveSt):
    if NowWaveSt == 1 and PreWaveSt ==0:
        return 1
    elif (NowWaveSt == 0 and PreWaveSt >=2) :            
        return -1
    else:
        return 0

def plot_EMA( CntEma ):
    color_list =['black','sienna','red','orange','gold','green','blue','purple','grey','teal','black','sienna','red','orange','gold','green','blue','purple','grey','teal'] 
    plt.figure(num =1, figsize=(18,9))    #創建圖表
    plt.plot(CntEma["date"],CntEma["close"],  label="close"   ,color = 'blue')
    for i in range(10,len(CntEma)):
        xdate = CntEma.at[i, "date"]
        yclose = CntEma.at[i, "close"]
        for j in range(16,22):
            rzt = PutOrCall(CntEma.iat[i,j], CntEma.iat[i-1,j])
            if rzt >0:
                plt.text(xdate, yclose-5, str(j-13)+'_' +str(xdate)[5:10],rotation=90,color=color_list[j-16])
            if rzt <0:
                plt.text(xdate, yclose+5, str(j-13)+'_' +str(xdate)[5:10],rotation=90,color=color_list[j-16])      
        '''
                rzt = PutOrCall(CntEma.at[i,"Cntema23"], CntEma.at[i-1,"Cntema23"])
        if rzt >0:
            plt.text(xdate, yclose-5, '2_' +str(xdate)[5:10],rotation=90,color='red')
        if rzt <0:
            plt.text(xdate, yclose+5, '2_' +str(xdate)[5:10],rotation=90,color='blue')         
        '''
    for j in range(4,13):
        plt.plot(CntEma["date"],CntEma.iloc[:,j],  label='ema'+str(j-3)   ,color = color_list[j-4])
    #plt.xlabel("價位")\plt.ylabel("日期")
    plt.subplots_adjust(left=0.05,bottom=0.07,right=0.97,top=0.97,wspace=0.12,hspace=0.12)
    plt.legend() 
    plt.savefig('..\\PlotImg\\'+'apka_count_EMA.png')  
    plt.show()
    

def score_EMA( data ):
    #print('apka_score_EMA')
    CntEma = pd.DataFrame()
    Cntema12 =Cntema23 =Cntema34 =Cntema45 =Cntema56 =Cntema67 =Cntema78 =Cntema89 =Cntema9A =0    
    for j in range(1,len(data)):
        try:
            Cntema12 = EmaStateMaChing( data.at[j, 'ema1'], data.at[j, 'ema2'],data.at[j, 'high'],data.at[j, 'low'],  Cntema12)                    
            Cntema23 = EmaStateMaChing( data.at[j, 'ema2'], data.at[j, 'ema3'],data.at[j, 'high'],data.at[j, 'low'],  Cntema23)
            Cntema34 = EmaStateMaChing( data.at[j, 'ema3'], data.at[j, 'ema4'],data.at[j, 'high'],data.at[j, 'low'],  Cntema34)        
            Cntema45 = EmaStateMaChing( data.at[j, 'ema4'], data.at[j, 'ema5'],data.at[j, 'high'],data.at[j, 'low'],  Cntema45)
            Cntema56 = EmaStateMaChing( data.at[j, 'ema5'], data.at[j, 'ema6'],data.at[j, 'high'],data.at[j, 'low'],  Cntema56)                    
            Cntema67 = EmaStateMaChing( data.at[j, 'ema6'], data.at[j, 'ema7'],data.at[j, 'high'],data.at[j, 'low'],  Cntema67)
            Cntema78 = EmaStateMaChing( data.at[j, 'ema7'], data.at[j, 'ema8'],data.at[j, 'high'],data.at[j, 'low'],  Cntema78)        
            Cntema89 = EmaStateMaChing( data.at[j, 'ema8'], data.at[j, 'ema9'],data.at[j, 'high'],data.at[j, 'low'],  Cntema89)
            Cntema9A = EmaStateMaChing( data.at[j, 'ema9'], data.at[j, 'ema10'],data.at[j, 'high'],data.at[j, 'low'],  Cntema9A)
            a=[ data.at[j,'date'],data.at[j,'close'],data.at[j,'high'],data.at[j,'low'],\
                data.at[j,"ema1"],data.at[j,"ema2"],data.at[j,"ema3"],data.at[j,"ema4"],\
                data.at[j,"ema5"],data.at[j,"ema6"],data.at[j,"ema7"],data.at[j,"ema8"],data.at[j,"ema9"],data.at[j,"ema10"],\
                Cntema12, Cntema23, Cntema34, Cntema45, Cntema56, Cntema67, Cntema78, Cntema89, Cntema9A]
            CntEma = pd.concat([CntEma, pd.DataFrame([a])], ignore_index=True)
        except Exception as errMsg: 
            print('每K線計算錯誤-', str(data.at[j,'date']) , errMsg)


    CntEma.columns = ["date", "close","high","low",\
                    "ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10",\
                    "Cntema12","Cntema23", "Cntema34", "Cntema45", "Cntema56","Cntema67", "Cntema78", "Cntema89", "Cntema9A"]
    
    #plot_EMA( CntEma )
    
    CntEma =CntEma.drop(columns=[ "close","high","low","ema1","ema2","ema3","ema4","ema5","ema6","ema7","ema8","ema9","ema10"])
    CntEma.to_csv("test_apka_count_EMA.csv")
    TredEma = pd.DataFrame()
    yema     = 0
    for i in range(10,len(CntEma)):
        try:
            EmaState =0
            EamCnt   =0
            #yema     =0 
            for j in range(3,10):
                if CntEma.iat[i,j] > EmaState :
                    EamCnt =j
                    EmaState = CntEma.iat[i,j]
            rzt = PutOrCall(EmaState, CntEma.iat[i-1,EamCnt])
            if rzt >0:
                yema += 1
            elif rzt <0:
                yema -= 1
            else:
                yema = yema
            a = [ CntEma.at[i,'date'], EamCnt, EmaState, yema ]
            TredEma = pd.concat([TredEma, pd.DataFrame([a])], ignore_index=True)            
        except Exception as errMsg: 
            print('每K線EMA錯誤-', str(data.at[j,'date']) , errMsg)
    TredEma.columns = ["date", "EamCnt","EmaState","yema"]                    
    TredEma.to_csv("test1_apka_count_EMA.csv")    
    return TredEma




