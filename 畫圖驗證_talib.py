import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

data = pd.read_csv("tech_idx_^SPX1_1Y.csv", index_col="key_0", parse_dates=True)


'''
#畫布林通道
plt.figure(num =1, figsize=(18,9)) 
plt.plot(data["close"],label="close" ,color = 'blue') 
plt.plot(data["upperband_x"],label="UBd" ,color = 'green') 
plt.plot(data["middleband_x"],label="MLd" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["lowerband_x"],label="LBd" ,color = 'red'  ) 
plt.plot(data["upperband_y"],label="UBw" ,color = 'green' , linestyle = '--') 
plt.plot(data["middleband_y"],label="MLw" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["lowerband_y"],label="LBw" ,color = 'red' , linestyle = '--')  
plt.plot(data["upperband"],label="UBm"  ,color = 'green' , linestyle = '-.') 
plt.plot(data["middleband"],label="MLm" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["lowerband"],label="LBm" ,color = 'red' , linestyle = '-.')  
#plt.plot(data["Close"],label="trima") 
plt.legend() 
plt.show()4777


#畫EMA趨勢線
plt.figure(num =3, figsize=(17,7)) 
plt.plot(data["close"],label="close" ,color = 'blue') 
plt.plot(data["ema1"],label="ema1" , linewidth = 0.5, linestyle = '-' ,color = 'red') 
plt.plot(data["ema2"],label="ema2" , linewidth = 0.5, linestyle = '--',color = 'red')  
plt.plot(data["ema3"],label="ema3" , linewidth = 0.5, linestyle = '-.',color = 'red') 
plt.legend() 
plt.show()

#畫STOCHRSI趨勢線
plt.figure(num =3, figsize=(17,7)) 
plt.plot(data["fastk_x"],label="kd" , linewidth = 0.5, linestyle = ':' ,color = 'red') 
plt.plot(data["fastd_x"],label="dd" , linewidth = 0.5, linestyle = '-.',color = 'red')  
plt.plot(data["fastk_y"],label="kw" , linewidth = 1, linestyle = '-' ,color = 'blue') 
plt.plot(data["fastd_y"],label="dw" , linewidth = 1, linestyle = '--',color = 'blue')  
plt.plot(data["fastk"],label  ="km" , linewidth = 1, linestyle = '-' ,color = 'green') 
plt.plot(data["fastd"],label  ="dm" , linewidth = 1, linestyle = '--',color = 'green')  

#畫Willrd指標
plt.figure(num =2, figsize=(18,9)) 
plt.plot(data["willrd"],label="Wd" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["willrw"],label="Ww" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["willrm"],label="wm" , linewidth = 0.5, linestyle = '--') 

#劃MACD
plt.plot(data["macd_y"]      ,label= "MACDw" , linewidth = 0.5, linestyle = '-') 
plt.plot(data["macdsignal_y"],label="sMACDw" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["macdhist_y"]  ,label="hMACDw" , linewidth = 0.5, linestyle = '-.') 

'''
plt.figure(num =2, figsize=(18,9))
plt.plot(data["macd_x"]      ,label= "MACDd" , linewidth = 0.5, linestyle = '-') 
plt.plot(data["macdsignal_x"],label="sMACDd" , linewidth = 0.5, linestyle = '--') 
plt.plot(data["macdhist_x"]  ,label="hMACDd") 


plt.legend() 
plt.show()