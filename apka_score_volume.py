#apka_score_volume
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
'''
評分艾爾德脈衝系統EMA參數 2 13*3 26*3
2 :vap2>0 and vap3>0  and (vap1<0 第2天)
1 :vap2>0 and vap3>0  and (vap1<0 第1天)
0 :
-1 : vap2<0 and vap3<0  and (vap1>0 第1天)
-2 : vap2<0 and vap3<0  and (vap1>0 第2天)                       
############################################    
評分emavol參數 5 10 20 'emavol1','emavol2','emavol3','close','vol2pri','volume'
2 : (emavol1 > emavol2 > emavol3) and (ema1 < ema2 < ema3) and (volume > emavol3*1.5) 
1 : (emavol1 > emavol2 > emavol3) and (ema1 < ema2 < ema3) 
0 :
-1 : (emavol1 > emavol2 > emavol3) and (ema1 < ema2 < ema3) 
-2 : (emavol1 < emavol2 < emavol3) and (ema1 > ema2 > ema3) and (volume > emavol3*1.1)

'''
def score_volume( data ):
    xapka = pd.DataFrame() 
    for j in range(10,len(data)):
        try:
            if data.at[j, 'vap1'] < 0 and  data.at[j, 'vap2'] > 0 and data.at[j, 'vap2'] > 0:

        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)                   
