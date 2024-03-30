from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import os
import time
import openpyxl
import datetime
import pandas as pd 

Web = [
 'https://hk.investing.com/etfs/spdr-s-p-500-technical'
,'https://hk.investing.com/etfs/powershares-qqqq-technical'
,'https://hk.investing.com/etfs/diamonds-trust-technical'
,'https://hk.investing.com/etfs/ishares-russell-2000-index-etf-technical'
,'https://hk.investing.com/etfs/ishares-phlx-sox-semiconductor-technical'
,'https://hk.investing.com/etfs/proshares-ultra-vix-short-term-fut-technical'
,'https://hk.investing.com/etfs/svix-technical'
,'https://hk.investing.com/commodities/crude-oil-technical'
,'https://hk.investing.com/indices/usdollar-technical'
,'https://hk.investing.com/etfs/direxion-30-yr-tr.-bull-3x-shrs-technical'
,'https://hk.investing.com/etfs/direxion-dly-semiconductor-bull-3x-technical'

,'https://hk.investing.com/equities/tesla-motors-technical'
,'https://hk.investing.com/equities/apple-computer-inc-technical'
,'https://hk.investing.com/equities/nvidia-corp-technical'
,'https://hk.investing.com/equities/microsoft-corp-technical'
,'https://hk.investing.com/equities/amazon-com-inc-technical'
,'https://hk.investing.com/equities/netflix,-inc.-technical'
,'https://hk.investing.com/equities/facebook-inc-technical'
,'https://hk.investing.com/equities/adv-micro-device-technical'
,'https://hk.investing.com/equities/google-inc-technical'
,'https://hk.investing.com/equities/micron-tech-technical'

,'https://hk.investing.com/etfs/bmo-rex-mcrsctrs-fang-index-3x-lvrg-technical'
,'https://hk.investing.com/etfs/direxion-dly-semiconductor-bull-3x-technical'
,'https://hk.investing.com/etfs/spdr-s-p-biotech-technical'
,'https://hk.investing.com/etfs/spdr-energy-select-sector-fund-technical'
,'https://hk.investing.com/etfs/financial-select-sector-spdr-fund-technical'
,'https://hk.investing.com/etfs/spdr-s-p-metals---mining-technical'
,'https://hk.investing.com/etfs/spdr---health-care-technical'
,'https://hk.investing.com/etfs/spdr---consumer-staples-technical'
,'https://hk.investing.com/etfs/ishares-dow-jones-us-real-est-technical'
,'https://hk.investing.com/etfs/spdr-select-sector---utilities-technical'
,'https://hk.investing.com/etfs/industrial-sector-spdr-trust-technical'
]

stk_list = [
 'SPY','QQQ','DIA','IWM','SOXX','UVXY','SVIX','DXY','CL','TMF','SOXL'
,'TSLA' ,'APPLE','NVDA','MSFT','AMZN','NFLX','META','AMD','GOOGL','MU'
,'FNGU','SOXL','XBI','XLE','CL','XLF','XME','XLV','XLP','IYR','XLU','XLI'
]

XL_row = [
 '4','5','6','7','8','9','10','11','12','13','14'
,'16','17','18','19','20','21','22','23','24'
,'27','28','29','30','32','33','34','35','36','37','38'    
]

os.chdir('C:/Users/tom.gau/OneDrive/')  # Colab 換路徑使用
wb = openpyxl.load_workbook('交易日誌_1120821-tom2022.xlsx')    # 開啟現有的 Excel 活頁簿物件
s2 = wb['2＿周技術分析']

loc_dt = datetime.datetime.today() 
loc_dt_format = loc_dt.strftime("%Y/%m/%d %H:%M:%S")
s2['M2'].value = loc_dt_format[1:10]
s2['N2'].value = loc_dt_format[12:20]

driver=webdriver.Chrome()

a = 0
while a<= 30: #30:
  
    driver.get(Web[a])
    time.sleep(5)
    price = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]").text
    name = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[2]/div/h2").text.replace('技術分析', '')
    print(name ,price,sep=",")
    s2['L'+XL_row[a]].value = price

    HR3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[8]/span").text
    HR2      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[7]").text
    Hmid     = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[5]/span").text
    HS2      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[3]/span").text
    HS3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[2]/span").text
    Hw1      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[6]/td[2]").text
    HSRSI    = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]").text
    HMACD    = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]").text
    HMA5     = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div/table/tbody/tr[1]/td[2]/div/div").text
    HMA10    = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div/table/tbody/tr[2]/td[2]/div/div").text
        
    print('小時技術分析-  Willams='+Hw1, '  SRSI='+ HSRSI, '  mid='+Hmid, '  R2='+ HR2, '  S2='+ HS2,'  MACD='+ HMACD ,sep=",")    #
    s2['AA'+XL_row[a]].value = '小時技術分析-  Willams='+Hw1+ '  SRSI='+ HSRSI+ '  mid='+ Hmid+ '  R2='+ HR2+ '  S2='+ HS2 +'  MACD='+ HMACD


    driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/button[7]").click()
    time.sleep(5)        
    DR3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[8]/span").text
    DR2      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[7]").text
    Dmid     = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[5]/span").text
    DS2      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[3]/span").text
    DS3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[2]/span").text
    Dw1      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[6]/td[2]").text
    DSRSI    = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]").text
    DMACD    = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]").text
    DMA5     = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div/table/tbody/tr[1]/td[2]/div/div").text
    DMA10    = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div/table/tbody/tr[2]/td[2]/div/div").text    
    print('日線技術分析-  Willams='+Dw1, '  SRSI='+ DSRSI, '  mid='+ Dmid, '  R2='+ DR2, '  S2='+ DS2,'  MACD=', DMACD ,sep=",") #
    #s2[XL_AB[a]].value = '日線技術分析-  Willams=',Dw1, '  SRSI=', DSRSI, '  mid=', Dmid, '  R2=', DR2, '  S2=', DS2 #,'  MACD=', DMACD
    s2['AB'+XL_row[a]].value = '日線技術分析-  Willams='+Dw1+ '  SRSI='+ DSRSI+ '  mid='+ Dmid+ '  R2='+ DR2+ '  S2='+ DS2 +'  MACD='+ DMACD

    driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/button[8]").click()
    time.sleep(5)   
    WR3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[8]/span").text
    WR2      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[7]").text
    Wmid     = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[5]/span").text
    WS2      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[3]/span").text
    WS3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[2]/span").text
    Ww1      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[6]/td[2]").text
    WSRSI    = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]").text
    WMACD    = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]").text   
    print('週線技術分析-  Willams='+Ww1, '  SRSI='+ WSRSI, '  mid='+ Wmid, '  R2='+ WR2, '  S2='+ WS2,'  MACD=', WMACD ,sep=",") #
    #s2[XL_AB[a]].value = '日線技術分析-  Willams=',Dw1, '  SRSI=', DSRSI, '  mid=', Dmid, '  R2=', DR2, '  S2=', DS2 #,'  MACD=', DMACD
    s2['AC'+XL_row[a]].value = '週線技術分析-  Willams='+Ww1+ '  SRSI='+ WSRSI+ '  mid='+ Wmid+ '  R2='+ WR2+ '  S2='+ WS2 +'  MACD='+ WMACD
    try:                      # 使用 try，測試內容是否正確          
        driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/button[9]").click()
        time.sleep(5)   
        MR3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[8]/span").text
        MR2      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[7]").text
        Mmid     = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[5]/span").text
        MS2      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[3]/span").text
        MS3      = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[4]/div/div/table/tbody/tr[1]/td[2]/span").text
        Mw1      = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[6]/td[2]").text
        MSRSI    = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]").text
        MMACD    = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]").text   
        print('月線技術分析-  Willams='+Mw1, '  SRSI='+ MSRSI, '  mid='+ Mmid, '  R2='+ MR2, '  S2='+ MS2,'  MACD=', MMACD ,sep=",") #
        #s2[XL_AB[a]].value = '日線技術分析-  Willams=',Dw1, '  SRSI=', DSRSI, '  mid=', Dmid, '  R2=', DR2, '  S2=', DS2 #,'  MACD=', DMACD
        s2['AC'+XL_row[a]].value = '月線技術分析-  Willams='+Mw1+ '  SRSI='+ MSRSI+ '  mid='+ Mmid+ '  R2='+ MR2+ '  S2='+ MS2 +'  MACD='+ MMACD
        
        fprice    = float(price)
        fHR3      = float(HR3)  
        fHR2      = float(HR2)  
        fHmid     = float(Hmid) 
        fHS2      = float(HS2)  
        fHS3      = float(HS3)  
        fHw1      = float(Hw1)  
        fHSRSI    = float(HSRSI)
        fHMACD    = float(HMACD)
        fHMA5     = float(HMA5) 
        fHMA10    = float(HMA10)    
                    
        fDR3      = float(DR3)  
        fDR2      = float(DR2)  
        fDmid     = float(Dmid) 
        fDS2      = float(DS2)  
        fDS3      = float(DS3)  
        fDw1      = float(Dw1)  
        fDSRSI    = float(DSRSI)
        fDMACD    = float(DMACD)
        fDMA5     = float(DMA5) 
        fDMA10    = float(DMA10)   
                    
        fWR3      = float(WR3)  
        fWR2      = float(WR2)  
        fWmid     = float(Wmid) 
        fWS2      = float(WS2)  
        fWS3      = float(WS3)  
        fWw1      = float(Ww1)  
        fWSRSI    = float(WSRSI)
        fWMACD    = float(WMACD)

        
        fMR3      = float(MR3)
        fMR2      = float(MR2) 
        fMmid     = float(Mmid) 
        fMS2      = float(MS2)  
        fMS3      = float(MS3)  
        fMw1      = float(Mw1)  
        fMSRSI    = float(MSRSI)
        fMMACD    = float(MMACD)

        

        #通道
        if   ( fprice < fDS2  and fprice < fWS2 ) or (  fprice < fDS2  and fprice < fWmid and fDMACD > 0 ):
            s2['B'+XL_row[a]].value = '2'
        elif ( fprice > fDR3  and fprice > fWmid and fWMACD < 0) or ( fprice > fDS3  and fprice > fWR2 and fDMACD < 0):
            s2['B'+XL_row[a]].value = '-2'
        elif fprice > fWmid and fprice < fDS2  and fWMACD > 0 :
            s2['B'+XL_row[a]].value = '1'
        elif fprice > fWmid and fprice > fDS2  and fWMACD < 0  :
            s2['B'+XL_row[a]].value = '-1'
        else:
            s2['B'+XL_row[a]].value = '0'

        #背離
        if (fHw1 < -70 and fDw1 < -50  and fWw1 > -20 ) or (fHw1 < -70 and fDw1 < -90  and fWw1 < -70  and fHw1> fDw1 > fWw1):
            s2['F'+XL_row[a]].value = '2'
        elif (fHw1 > -30 and fDw1 > -10  and fWw1 > -10  and fHw1< fDw1 < fWw1):
            s2['F'+XL_row[a]].value = '-2'
        elif fHw1 < -70 and fDw1 < -50  and fWw1 > -30 :
            s2['F'+XL_row[a]].value = '1'
        elif fHw1 > -30 and fDw1 > -30  and fWw1 < -50 :
            s2['F'+XL_row[a]].value = '-1'
        else:
            s2['F'+XL_row[a]].value = '0'    


        #震盪
        if (fHSRSI < -70 and fDSRSI < -50  and fWw1 > -20 ) or (fHw1 < -70 and fDw1 < -90  and fWw1 < -70  and fHw1> fDw1 > fWw1):
            s2['I'+XL_row[a]].value = '2'
        elif (fHw1 > -30 and fDw1 > -10  and fWw1 > -10  and fHw1< fDw1 < fWw1):
            s2['I'+XL_row[a]].value = '-2'
        elif fHSRSI < 20 and fDSRSI > 80  and (fDMACD > 0 or ( fDMACD > fWMACD and fHMACD >0 ) ) :
            s2['I'+XL_row[a]].value = '1'
        elif fHSRSI > 80 and fDSRSI > 80  and (fDMACD < 0 or ( fDMACD < fWMACD and fHMACD <0 ) )   :
            s2['I'+XL_row[a]].value = '-1'
        else:
            s2['I'+XL_row[a]].value = '0'                      

        '''  
        if willams.int <=-90 and price.float < S2.float:
            s2[XL_BB[a]].value = '2'
        elif willams.int >=-10 and price.float > R2.float :
            s2[XL_BB[a]].value = '-2'
        elif SPY.float >  mid.float:
            s2[XL_BB[a]].value = '1'
        elif SPY.float <  mid.float:
            s2[XL_BB[a]].value = '-1'
        '''          
    except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
        print('發生錯誤-', name.replace('技術分析','')+' :' , errMsg)
            
    a += 1
wb.save('交易日誌_1120821-tom2022.xlsx')  
time.sleep(5)