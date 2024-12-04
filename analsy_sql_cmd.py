#analsy_sql_cmd

s_Stock_Ticker = 'select * FROM [Stock].[dbo].[Ticker_apk] '
s_Stock_Ticker_TW  = 'select * FROM [Stock].[dbo].[Ticker_TW1] '

def SLastDay( xTicker):
    return f'select max(Date) Date FROM [apka].[dbo].[ApkaDay_{xTicker}]'    

def DelLastDay( xTicker, SqlMaxDate):
    return f"DELETE [apka].[dbo].[ApkaDay_{xTicker}] Where Date >= '{SqlMaxDate} 00:00:00.000'"

def DelDupDay_Combin(Country):
    return  "DELETE T FROM ("+\
            f"SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date] ORDER BY (SELECT NULL)) FROM [apka].[dbo].[ApkaDay_Combin_{Country}]"+\
            ") AS T WHERE DupRank > 1 "

def DelDupDay( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date] ORDER BY (SELECT NULL))"+\
            f"	FROM [apka].[dbo].[ApkaDay_{xTicker}]) AS T WHERE DupRank > 1"
 
def sqlCommand( xcode, kind, Bef1YerDate):
    BaseSql = "select  distinct [date],[open],[high],[low],[close],[colume],[fastk_d],[fastd_d],[fastk_w],[fastd_w],[fastk_m],[fastd_m],[willrd],[willrw],[willrm],\
            [MACD_d],[signal_d],[histg_d],[MACD_w],[signal_w],[histg_w],[MACD_m],[signal_m],[histg_m],[upp_d],[mid_d],[low_d],[upp_w],[mid_w],[low_w],[upp_m],[mid_m],[low_m],\
            [ema1],[ema2],[ema3],[ema4],[ema5],[ema6],[ema7],[ema8],[ema9],[ema10]\
            FROM [analsy].[dbo]."
    if   kind ==1:
        sql = BaseSql +f"[AnalysDay_{xcode}] Where date between '2023-05-03 00:00:00.000' and '2024-05-29 00:00:00.000' order by date " #between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' "
    elif   kind ==2:
        sql = BaseSql +f"[AnalysDay_{xcode}] WHere date > '2021-05-28 00:00:00.000' order by date " #between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' "        
    elif kind ==3:
        sql = BaseSql +f"[AnalysHour3_{xcode}] WHere date > '2024-01-03 00:00:00.000' order by date " #AnalysHour3_SPY
    elif kind ==4:#Bef1YerDate.strftime("%Y-%m-%d, %H:%M:%S")
        sql = BaseSql +f"[AnalysDay_{xcode}] WHere date > '"+Bef1YerDate.strftime("%Y-%m-%d %H:%M:%S") +"' order by date " #between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' " 
    elif kind ==5:#Bef1YerDate.strftime("%Y-%m-%d, %H:%M:%S")
        sql = BaseSql +f"[AnalysDay_{xcode}] order by date "#between '2021-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' "                  
    else:
        sql = f"select  distinct [date],[open],[high],[low],[close],[colume],[fastk_d],[fastd_d],[fastk_w],[fastd_w],[fastk_m],[fastd_m],[willrd],[willrw],[willrm],\
                [MACD_d],[signal_d],[histg_d],[MACD_w],[signal_w],[histg_w],[MACD_m],[signal_m],[histg_m],[upp_d],[mid_d],[low_d],[upp_w],[mid_w],[low_w],[upp_m],[mid_m],[low_m],\
                [ema1],[ema2],[ema3],[ema4],[ema5],[ema6],[ema7],[ema8],[ema9],[ema10]\
                FROM [analsy].[dbo].[AnalysDay_{xcode}] WHere date between '202-05-03 00:00:00.000' and '2022-05-03 00:00:00.000' "        
    return sql