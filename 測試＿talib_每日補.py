import yfinance as yf
import time
import pymssql
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
from datetime import timedelta
import talib
from talib import abstract

try:
    # 初始化数据库连接引擎 create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数
    conn = pymssql.connect(host="192.9.12.226:1433", user='sa', password='abc123', database='Stock',charset='GBK')
    cursor = conn.cursor()    
    engine = create_engine("mssql+pymssql://sa:abc123@192.9.12.226:1433/Stock?charset=GBK")

    sql = 'select * FROM [Stock].[dbo].[TechAnalysis] '
    pd_TechAnalysis = pd.read_sql(sql, engine)

    sql2 = 'select * FROM [Stock].[dbo].[Ticker] '
    CurrDate = datetime.now().strftime("%Y-%m-%d")
    pd_read_sql = pd.read_sql(sql2, engine)
    for i in pd_read_sql.Stock:
        print('Stock_'+i)
        try:
            #日K
            sql3 = 'select max(Date) Date FROM [Stock].[dbo].' +i.strip()+'_AnalysDay '
            SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
            sql4 = "DELETE [Stock].[dbo]."+ i.strip()+'_AnalysDay ' +"Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
            cursor.execute(sql4)
            conn.commit()

            sql3 = 'select top 1000 Date FROM [Stock].[dbo].[RowDay_'+i.strip()+'] order by date desc'
            SqlMinDate = pd.read_sql(sql3, engine).iat[999, 0].strftime("%Y-%m-%d")
            sql3 = "select * FROM [Stock].[dbo].[RowDay_"+i.strip()+"] where date >='"+SqlMinDate+" 00:00:00.000'"
            data = pd.read_sql(sql3, engine, parse_dates=True)
            data.columns = ["date","open", "high", "low", "close", "adj close", "colume"]
            for x in range(0,22):
                rztcoul = pd_TechAnalysis.at[x,"RztLabel"].strip().split(',')
                try:
                    output = eval('abstract.'+pd_TechAnalysis.at[x,"function"].strip()+'(data, '+pd_TechAnalysis.at[x,"parameter"].strip()+' )')
                    output.columns = rztcoul
                    # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
                    output.name = pd_TechAnalysis.at[x,"name"].lower() if type(output) == pd.core.series.Series else None
                    # 透過 merge 把輸出結果併入 df DataFrame
                    data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
                    data = data.set_index('key_0')
                except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
                    print('abstract發生錯誤-', pd_TechAnalysis.at[x,"name"] , errMsg)    

            try:          
                data1 = data[data["date"] >= SqlMaxDate+" 00:00:00.000"]  
                data1.reset_index(drop=True)
                data.to_sql( i.strip()+'_AnalysDay',engine,if_exists='append', index=False)
            except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
                print('回存資料庫錯誤_', i.strip() , errMsg)    
        except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print('Day發生錯誤-'+i.strip() , errMsg)            

        try:
            #小時K
            sql3 = 'select max(Date) Date FROM [Stock].[dbo].' +i.strip()+'_AnalysHour '
            SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
            sql4 = "DELETE [Stock].[dbo]."+ i.strip()+'_AnalysHour ' +"Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
            cursor.execute(sql4)
            conn.commit()

            sql3 = 'select top 1000 Datetime Date FROM [Stock].[dbo].[RowHour_'+i.strip()+'] order by date desc'
            SqlMinDate = pd.read_sql(sql3, engine).iat[999, 0].strftime("%Y-%m-%d")
            sql3 = "select * FROM [Stock].[dbo].[RowHour_"+i.strip()+"] where datetime >='"+SqlMinDate+" 00:00:00.000'"
            data = pd.read_sql(sql3, engine, parse_dates=True)
            data.columns = ["date","open", "high", "low", "close", "adj close", "colume"]
            for x in range(0,22):
                rztcoul = pd_TechAnalysis.at[x,"RztLabel"].strip().split(',')
                try:
                    output = eval('abstract.'+pd_TechAnalysis.at[x,"function"].strip()+'(data, '+pd_TechAnalysis.at[x,"parameter"].strip()+' )')
                    output.columns = rztcoul
                    # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
                    output.name = pd_TechAnalysis.at[x,"name"].lower() if type(output) == pd.core.series.Series else None
                    # 透過 merge 把輸出結果併入 df DataFrame
                    data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
                    data = data.set_index('key_0')
                except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
                    print('abstract發生錯誤-', pd_TechAnalysis.at[x,"name"] , errMsg)    

            try:          
                data1 = data[data["date"] >= SqlMaxDate+" 00:00:00.000"]  
                data1.reset_index(drop=True)
                data.to_sql( i.strip()+'_AnalysHour',engine,if_exists='append', index=False)
            except Exception as errMsg:# 如果 try 的內容發生錯誤，就執行 except 裡的內容
                print('回存資料庫錯誤_', i.strip() , errMsg)    
        except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print('發生錯誤-'+i.strip() , errMsg)            

        
        #週K
        '''
        sql3 = 'select top 1 max(Date) Date FROM [Stock].[dbo].[RowWeek_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowWeek_"+i.strip()+"] Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        yf.download(i,start = SqlMaxDate, end=CurrDate,interval='1wk').to_sql( 'RowWeek_'+i.strip(),engine,if_exists='append', index=True)

        '''

        #yf.download(i,period='2y',interval='1h').to_csv('RowHr_'+i.strip()+'.csv')#to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        #小時K
        '''
        sql3 = 'select top 1 max(Datetime) Date FROM [Stock].[dbo].[RowHour_'+i.strip()+'] '
        SqlMaxDate = pd.read_sql(sql3, engine).iat[0, 0].strftime("%Y-%m-%d")
        sql4 = "DELETE [Stock].[dbo].[RowHour_"+i.strip()+"] Where Datetime >= '"+SqlMaxDate+" 00:00:00.000'"
        cursor.execute(sql4)
        conn.commit()
        '''

        #rzt = yf.download(i,start = SqlMaxDate.iat[0, 0].strftime("%Y-%m-%d"), end=CurrDate.strftime("%Y-%m-%d"),interval='1h')
        #print(rzt)
        '''
        #初始下載歷史資料
        yf.download(i,period='1d',interval='1h').to_sql( 'RowHour_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5) 
        yf.download(i,period='1d',interval='1d').to_sql( 'RowDay_'+i.strip(),engine,if_exists='append', index=True)
        time.sleep(5)
        if datetime.now().isoweekday() == 5: 
            yf.download(i,period='1wk',interval='1wk').to_sql( 'RowWeek_'+i.strip(),engine,if_exists='append', index=True)#to_csv('RowWeek_'+i.strip()+'.csv')#

        '''
        time.sleep(5)   
    #print(pd_read_sql.kdatetime)
    '''
    stock = yf.Ticker('^IXIC')
    yf.download('^SPX',period='1d',interval='90m').to_sql('test_table',engine,if_exists='append', index=True)

    '''
 
  
except Exception as errMsg:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
    print('連線SQL發生錯誤-' , errMsg)


