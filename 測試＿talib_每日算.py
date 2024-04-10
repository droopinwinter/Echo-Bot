import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
import time
from talib import abstract

# 準備一份你想要計算並且併入 df 的技術指標清單
ta_list = ['MACD','STOCHRSI', 'WILLR','BBANDS', 'EMA']
ta_list1 = [
	["STOCHRSId", "STOCHRSI","timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=3"],
	["STOCHRSIw", "STOCHRSI","timeperiod=70, fastk_period=70, fastd_period=6, fastd_matype=6"],
	["STOCHRSIm", "STOCHRSI","timeperiod=350, fastk_period=350, fastd_period=8, fastd_matype=8"],
	["WILLRd"   , "WILLR"   ,"timeperiod=14"],
	["WILLRw"   , "WILLR"   ,"timeperiod=70"],
	["WILLRm"   , "WILLR"   ,"timeperiod=350"],
	["MACDd"    , "MACD"    ,"fastperiod=12, slowperiod=26, signalperiod=9"],
	["MACDw"    , "MACD"    ,"fastperiod=60, slowperiod=130, signalperiod=9"],
	["MACDm"    , "MACD"    ,"fastperiod=300, slowperiod=650, signalperiod=9"],
	["BBANDSd"  , "BBANDS"  ,"timeperiod=5"],
	["BBANDSw"  , "BBANDS"  ,"timeperiod=25"],
	["BBANDSm"  , "BBANDS"  ,"timeperiod=125"],
	["EMA1"     , "EMA"     ,"timeperiod=6"],
	["EMA2"     , "EMA"     ,"timeperiod=12"],
	["EMA3"     , "EMA"     ,"timeperiod=18"],
	["EMA4"     , "EMA"     ,"timeperiod=24"],
	["EMA5"     , "EMA"     ,"timeperiod=36"],
	["EMA6"     , "EMA"     ,"timeperiod=48"],
	["EMA7"     , "EMA"     ,"timEMAeperiod=72"],
	["EMA8"     , "EMA"     ,"timeperiod=96"],
	["EMA9"     , "EMA"     ,"timeperiod=144"],
	["EMA10"    , "EMA"     ,"timeperiod=192"]
]
ta_list1_df = pd.DataFrame(ta_list1)
ta_list1_df.columns = ["name", "function", "parameter"]
#print(ta_list1_df)
#STOCHRSI([input_arrays], [timeperiod=14], [fastk_period=5], [fastd_period=3], [fastd_matype=0])
#WILLR(   [input_arrays], [timeperiod=14])
#MACD(    [input_arrays], [fastperiod=12], [slowperiod=26],  [signalperiod=9])
#BBANDS(  [input_arrays], [timeperiod=5],  [nbdevup=2.0],    [nbdevdn=2.0],    [matype=0])
#EMA(     [input_arrays], [timeperiod=30])
'''
for y in stk_list:
    try:
        data1 = pd.read_csv("price_"+stk_list[y]+".csv", index_col="date", parse_dates=True)
        data1 = data1.astype('float')
        for x in range(0,22):
            try:
                # x 為技術指標的代碼，透過迴圈填入，再透過 eval 計算出 output
                print( x,ta_list1_df.at[x,"function"]+','+ ta_list1_df.at[x,"parameter"] )
                output = eval('abstract.'+ta_list1_df.at[x,"function"]+'(data, '+ta_list1_df.at[x,"parameter"]+' )')
                # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
                #output.name = ta_list1_df.at[x,"NAME"].lower() if type(output) == pd.core.series.Series else None
                output.name = ta_list1_df.at[x,"name"].lower() if type(output) == pd.core.series.Series else None        
                # 透過 merge 把輸出結果併入 df DataFrame
                data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
                data = data.set_index('key_0')
                #print(ta_list1_df.iat[x, 0], ta_list1_df.iat[x, 1],ta_list1_df.iat[x, 2])
                
            except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
                print('發生錯誤-', ta_list1_df.at[x,"name"] , errMsg)                

        try:
            data1.to_csv("tech_idx_"+stk_list[y]+".csv")
        except Exception as errMsg:             
            print('發生錯誤-data.to_csv'+stk_list[y],  errMsg)        
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('發生錯誤-', stk_list[y] , errMsg)
'''

data = pd.read_csv("price_^DJI.csv", index_col="date", parse_dates=True)
data = data.astype('float')

for x in range(0,22):
    try:
        # x 為技術指標的代碼，透過迴圈填入，再透過 eval 計算出 output
        print( x,ta_list1_df.at[x,"function"]+','+ ta_list1_df.at[x,"parameter"] )
        output = eval('abstract.'+ta_list1_df.at[x,"function"]+'(data, '+ta_list1_df.at[x,"parameter"]+' )')
        # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
        #output.name = ta_list1_df.at[x,"NAME"].lower() if type(output) == pd.core.series.Series else None
        output.name = ta_list1_df.at[x,"name"].lower() if type(output) == pd.core.series.Series else None        
        # 透過 merge 把輸出結果併入 df DataFrame
        data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
        data = data.set_index('key_0')
        #print(ta_list1_df.iat[x, 0], ta_list1_df.iat[x, 1],ta_list1_df.iat[x, 2])
        
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('發生錯誤-', ta_list1_df.at[x,"name"] , errMsg)


#print(data)
try:
    data.to_csv("tech_idx_DJI.csv")
except Exception as errMsg:             
    print('發生錯誤-data.to_csv',  errMsg)
'''
data = pd.read_csv("price_^SPX1.csv", index_col="date", parse_dates=True)
data = data.astype('float')

#ta_list = talib.get_functions()
# 迴圈執行，看看結果吧！
for x in ta_list:
    try:
        # x 為技術指標的代碼，透過迴圈填入，再透過 eval 計算出 output
        output = eval('abstract.'+x+'(data)')
        # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
        output.name = x.lower() if type(output) == pd.core.series.Series else None
        # 透過 merge 把輸出結果併入 df DataFrame
        data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
        data = data.set_index('key_0')
    except:
        print(x+'_ERR')

#print(data)
data.to_csv("tech_idx_^SPX1.csv")

#EMA6 = talib.EMA(data.close, timeperiod = 6)
#print (EMA6)
time.sleep(5)

# 這裡示範全部 158 種技術指標



data = pd.read_csv("price_^SPX1.csv", index_col="Date", parse_dates=True)
sma = talib.SMA(data["Close"], 60)      # 簡單移動平均線 
ema = talib.EMA(data["Close"], 60)      # 指數移動平均線 
wma = talib.WMA(data["Close"], 60)      # 加權移動平均線 
trima = talib.TRIMA(data["Close"], 60)  # 三角移動平均線

plt.figure(figsize=(12,6)) 
plt.plot(data["Close"],label="close") 
#plt.plot(sma,label="sma") 
plt.plot(ema,label="ema") 
plt.plot(wma,label="wma") 
plt.plot(trima,label="trima") 
plt.legend() 
plt.show()

# 透過『get_functions』語法，查看 TA-Lib 提供的所有技術指標的代碼
all_ta_label = talib.get_functions()
# 看一下清單
print(all_ta_label)

# 共有 158 個技術指標可以運算
lenth = len(all_ta_label)

print(lenth)

# 透過『get_function_groups』，取得分類後的技術指標清單
all_ta_groups = talib.get_function_groups()
# 看一下這個字典
print(all_ta_groups)
# 有哪些大類別？
print(all_ta_groups.keys())
# 查看某類別底下的技術指標清單
print (all_ta_groups['Momentum Indicators'])
# 查看所有類別的指標數量
table = pd.DataFrame({
            '技術指標類別名稱': list(all_ta_groups.keys()),
            '該類別指標總數': list(map(lambda x: len(x), all_ta_groups.values()))
        })
print(table)


print(abstract.STOCHRSI )
print(abstract.WILLR )
print(abstract.BBANDS )
print(abstract.EMA )

'''
