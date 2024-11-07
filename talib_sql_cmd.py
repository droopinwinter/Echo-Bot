#talib_sql_cmd
sql = 'select * FROM [Stock].[dbo].[TechAnalysis] '

sql3 = 'select max(Date) Date FROM [analsy].[dbo].AnalysDay_' +i.strip()
sql4 = "DELETE [analsy].[dbo].AnalysDay_"+ i.strip()+" Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
sql3 = "select * FROM [Stock].[dbo].[RowDay_"+i.strip()+"] where date >='"+SqlMinDate+" 00:00:00.000'"

sql3 = 'select max(Date) Date FROM [analsy].[dbo].AnalysHour_' +i.strip()
sql4 = "DELETE [analsy].[dbo].AnalysHour_"+ i.strip()+" Where Date >= '"+SqlMaxDate+" 00:00:00.000'"
sql3 = 'select top 1000 Datetime Date FROM [Stock].[dbo].[RowHour_'+i.strip()+'] order by date desc'
sql3 = "select * FROM [Stock].[dbo].[RowHour_"+i.strip()+"] where datetime >='"+SqlMinDate+" 00:00:00.000'"