#talib_sql_cmd
s_Stock_TechAnalysis = 'select * FROM [Stock].[dbo].[TechAnalysis] '

def SLastHour( xTicker):
    return f'select max(Date) Date FROM [analsy].[dbo].AnalysHour_{xTicker}'

def SLastDay( xTicker):
    return f'select max(Date) Date FROM [analsy].[dbo].AnalysDay_{xTicker}'    

def S1000Day( xTicker):
    return f'select top 1000 Datetime Date FROM [Stock].[dbo].[RowHour_{xTicker}] order by date desc'

sql4 = "DELETE [analsy].[dbo].AnalysDay_"+ i.strip()+" Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
sql3 = "select * FROM [Stock].[dbo].[RowDay_"+i.strip()+"] where date >='"+SqlMinDate+" 00:00:00.000'"


sql4 = "DELETE [analsy].[dbo].AnalysHour_"+ i.strip()+" Where Date >= '"+SqlMaxDate+" 00:00:00.000'"

sql3 = "select * FROM [Stock].[dbo].[RowHour_"+i.strip()+"] where datetime >='"+SqlMinDate+" 00:00:00.000'"