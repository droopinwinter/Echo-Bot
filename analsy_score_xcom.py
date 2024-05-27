#analsy_score_xcom
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np

def score_xcom(apkaCom):
    cmb = pd.DataFrame()
    for i in range(10,len(apkaCom)):
        xema = apkaCom.at[i,"xema"] 
        yema = apkaCom.at[i,"yema"] 
        xmacd= apkaCom.at[i,"xmacd"]
        OscSum = apkaCom.at[i,"OscSum"]
        xremark= ''        
        xcmb =0
        xstate = 0
        for j in range(1,3):
            xstate +=(apkaCom.at[i-j+1,"xmacd"] - apkaCom.at[i-j,"xmacd"])

        if  (yema > apkaCom.at[i-1,"yema"] and yema>0) and ( xmacd >0 or xmacd > apkaCom.at[i-1,"xmacd"] ) and ( OscSum> apkaCom.at[i-1,"OscSum"]):
            for  j in range(2,5):
                if apkaCom.at[i-1,"yema"] == apkaCom.at[i-j,"yema"]: 
                    xremark = '確認漲勢_K線回採GMMA_週期倍率' +  str(apkaCom.at[i,"EamCnt"] )
                    xcmb = xcmb + 2
        elif ( yema < apkaCom.at[i-1,"yema"] and yema<0 ) and ( xmacd <0 or xmacd < apkaCom.at[i-1,"xmacd"] ) and ( OscSum< apkaCom.at[i-1,"OscSum"]):
            for  j in range(2,5):
                if apkaCom.at[i-1,"yema"] == apkaCom.at[i-j,"yema"]:             
                    xremark = '確認跌勢_K線反彈GMMA_週期倍率' +  str(apkaCom.at[i,"EamCnt"] )
                    xcmb = xcmb - 2
        if xmacd > apkaCom.at[i-1,"xmacd"] and OscSum> apkaCom.at[i-1,"OscSum"]:
            #牛市修正<找買點 或牛市到頂轉空
            xcmb = xcmb+ 2
            xremark = '金叉轉多'
        if xmacd < apkaCom.at[i-1,"xmacd"] and OscSum< apkaCom.at[i-1,"OscSum"]:
            #牛市修正<找買點 或牛市到頂轉空
            xcmb = xcmb- 2
            xremark = '死叉轉空'
            
        if xema >=0 and xmacd>=0:
            #牛市修正<找買點 或牛市到頂轉空
            if xema ==2 and xmacd == 1 and apkaCom.at[i,"OscSum"] <=2:
                xcmb = xcmb + apkaCom.at[i,"OscSum"]  
                xremark = '多頭震盪'
            else:
                xcmb = xcmb + apkaCom.at[i,"OscSum"]+ xmacd + xema+ yema
                xremark = '強勢多頭'
        elif xema >0 and xmacd<0:
            #牛市修正<找買點 或牛市到頂轉空
            if xema ==2 and xmacd == -1:
                xcmb = xcmb + apkaCom.at[i,"OscSum"] 
                xremark = '多頭小修'
            else:
                xcmb = xcmb + apkaCom.at[i,"OscSum"] +xmacd
                xremark = '多頭大修'
        elif xema <0 and xmacd>0:
            xcmb = xcmb + apkaCom.at[i,"OscSum"] +xmacd
            xremark = '空頭反彈'
        elif xema <0 and xmacd<0:
                #震盪沒有方向<觀望
            xcmb = xcmb + apkaCom.at[i,"OscSum"]
            xremark = '空頭'
        else:
            xcmb =apkaCom.at[i,"OscSum"]
            xremark = '未知'
        a = [ apkaCom.at[i,'date'], xcmb, xremark, xstate]
        cmb = pd.concat([cmb, pd.DataFrame([a])], ignore_index=True)
    cmb.columns = ["date", "xcmb","xremark", "xstate"]
    return cmb
 