#analsy_volume.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

def analsy_volume( data ):
    dfVp = data
    dfEV = data
    try:
        ##############################################################     
        dfEV.columns = ['date','volacu','vap1','vap2','close','vap3','volume']
        for j in range(1,len(dfEV)):
            try:
                dfEV.at[j,'volacu'] = dfEV.at[j,"volume"]*(dfEV.at[j,"close"] - dfEV.at[j-1,"close"])
            except Exception as errMsg: 
                print('每K線計算發生錯誤-', str(dfEV.at[j,'date']) , errMsg)                   

        dfEV['vap1'] = talib.EMA(dfEV['volacu'], timeperiod=2)
        dfEV['vap2'] = talib.EMA(dfEV['volacu'], timeperiod=13)
        dfEV['vap3'] = talib.EMA(dfEV['volacu'], timeperiod=26)
        dfEV =dfEV.drop(columns=["volacu","close", "volume"])
        ##############################################################
        dfVp.columns   = ['date','emavol1','emavol2','emavol3','close','vol2pri','volume']
        dfVp['emavol1'] = talib.EMA(dfVp['volume'], timeperiod=5)
        dfVp['emavol2'] = talib.EMA(dfVp['volume'], timeperiod=10)
        dfVp['emavol3'] = talib.EMA(dfVp['volume'], timeperiod=20)
        dfVp =dfVp.drop(columns=["close"])
        dfVp = pd.merge( dfEV, dfVp)
    except Exception as errMsg: 
        print('價量計算發生錯誤-', errMsg)                   

    return dfVp