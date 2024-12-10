#apka_score_volume
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

def score_volume( data ):
    df = data 
    data.columns = ['Date','Volacu','Vap1','Vap2','Close','Vap3','Volume']
    for j in range(1,len(data)):
        try:
            data.at[j,'Volacu'] =data.at[j,"Volume"]*(data.at[j,"Close"] - data.at[j-1,"Close"])
        except Exception as errMsg: 
            print('每K線計算發生錯誤-', str(data.at[j,'date']) , errMsg)                   

    data['Vap1'] = talib.EMA(data['Volacu'], timeperiod=2)
    data['Vap2'] = talib.EMA(data['Volacu'], timeperiod=13)
    data['Vap3'] = talib.EMA(data['Volacu'], timeperiod=26)
    data =data.drop(columns=["Close", "Volume"])
    df.columns   = ['Date','EmaVol1','EmaVol2','EmaVol3','Close','Vol2Pri','Volume']
    df['EmaVol1'] = talib.EMA(data['Volume'], timeperiod=5)
    df['EmaVol2'] = talib.EMA(data['Volume'], timeperiod=10)
    df['EmaVol3'] = talib.EMA(data['Volume'], timeperiod=20)
    df =df.drop(columns=["Close"])
    data = pd.merge( data, df)
    return data