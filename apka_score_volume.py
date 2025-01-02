#apka_score_volume
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
'''
評分艾爾德脈衝系統EMA參數 2 13*3 26*3
 2 :vap2>0 and vap3>0 and vap1<0
 1 :vap2>0 and vap3>0 and vap1>0
 0 :
-1 :vap2<0 and vap3<0 and vap1<0
-2 :vap2<0 and vap3<0 and vap1>0
############################################    
評分emavol參數 5 10 20 'emavol1','emavol2','emavol3','close','vol2pri','volume'
2 : (emavol1 > emavol2 > emavol3) and (ema1 < ema2 < ema3) and (volume > emavol3*1.5) 
1 : (emavol1 > emavol2 > emavol3) and (ema1 < ema2 < ema3) 
0 :
-1 : (emavol1 > emavol2 > emavol3) and (ema1 < ema2 < ema3) 
-2 : (emavol1 < emavol2 < emavol3) and (ema1 > ema2 > ema3) and (volume > emavol3*1.1)

'''
def score_volume( data ):
    vol = pd.DataFrame() 
    for j in range(1,len(data)):
        try:
            if data.at[j, 'emavol1'] > data.at[j, 'emavol2'] and data.at[j, 'emavol1'] > data.at[j, 'emavol3']:
                volexp = 1
            elif data.at[j, 'emavol1'] > data.at[j, 'emavol3']*2 and vol.iat[j-1,1] ==1:
                volexp = 2
            elif data.at[j, 'emavol1'] > data.at[j, 'emavol2'] and data.at[j, 'emavol2'] > data.at[j, 'emavol3']:
                volexp =-1
            elif data.at[j, 'emavol1'] > data.at[j, 'emavol3']*0.5 and vol.iat[j-1,1] ==-1:
                volexp =-2
            else:
                volexp = 0
            a=[ data.at[j,'date'],volexp]
            vol = pd.concat([vol, pd.DataFrame([a])], ignore_index=True)  
        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)
    vol.columns = ["date", "volexp"] 
    return vol

def score_pulse( data ):
    efi = pd.DataFrame() 
    for j in range(3,len(data)):
        vap1 = data.at[j, 'vap1']
        vap1_2 = data.at[j-2, 'vap1']
        vap2 = data.at[j, 'vap2']
        vap3 = data.at[j, 'vap3']
        try:
            if   (vap1 < 0 and vap2 > 0 and vap3 > 0 and vap1_2>0 )\
                or ( vap1 > 0 and vap2 < 0 and vap3 < 0 and vap1_2>0 ):
                pls = 2
            elif vap1 > 0 and vap2 > 0 and vap3 > 0:
                pls = 1
            elif (vap1 > 0 and vap2 < 0 and vap3 < 0 and vap1_2<0)\
                or ( vap1 < 0 and vap2 > 0 and vap3 > 0 and vap1_2<0 ):
                pls = -2
            elif vap1 < 0 and vap2 < 0 and vap3 < 0:
                pls = -1                
            else:
                pls = 0
            a=[ data.at[j,'date'],pls]
            efi = pd.concat([efi, pd.DataFrame([a])], ignore_index=True)   
        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)              
    efi.columns = ["date", "plse"] 
    return efi

def score_nime( data ):
    c9 = pd.DataFrame()
    lcnt =0
    scnt =0
    for j in range(5,len(data)):
        close = data.at[j, 'close']
        close_4 = data.at[j-4, 'close']
        try:
            if lcnt==9 or (close <= close_4 and lcnt>0 and lcnt<8 ):
                lcnt=0
            if (close > close_4)  and lcnt==0:
                lcnt =1
            if (close > close_4) and (data.at[j-1, 'close'] > data.at[j-5, 'close']) and lcnt>0 and lcnt<9:
                lcnt +=1
            if lcnt ==8 or lcnt ==9:
                cnt9 = lcnt
            else:
                cnt9 = 0

            if scnt==-9 or (close >= close_4 and scnt<0 and scnt>-8 ):
                scnt=0
            if (close < close_4)  and scnt==0:
                scnt =-1
            if (close < close_4) and (data.at[j-1, 'close'] < data.at[j-5, 'close']) and scnt<0 and lcnt>-9:
                scnt -=1
            if scnt ==-8 or scnt ==-9:
                cnt9 = scnt
            else:
                cnt9 = 0
            a=[ data.at[j,'date'],cnt9]
            c9 = pd.concat([c9, pd.DataFrame([a])], ignore_index=True)   
        except Exception as errMsg: 
            print('每K線計算錯誤-', str(data.at[j,'date']) , errMsg)
    c9.columns = ["date", "count9"] 
    return c9
