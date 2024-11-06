s_Stock_Ticker  = 'select * FROM [Stock].[dbo].[Ticker] '
xTicker = ''
SqlMaxDate =''
s_Stock_RowHour = 'select top 1 max(Datetime) Date FROM [Stock].[dbo].[RowHour_%s]' % (xTicker) 
s_Stock_RowDay  = 'select top 1 max(Date)     Date FROM [Stock].[dbo].[RowDay_%s]'  % (xTicker) 
s_Stock_RowWeek = 'select top 1 max(Date)     Date FROM [Stock].[dbo].[RowWeek_%s]' % (xTicker)
d_Stock_RowHour = "DELETE [Stock].[dbo].[RowHour_%s] Where Datetime >= '%s 00:00:00.000'"  % (xTicker,SqlMaxDate)
d_Stock_RowDay  = "DELETE [Stock].[dbo].[RowDay_%s] Where Date >= '%s 00:00:00.000'"  % (xTicker,SqlMaxDate)
d_Stock_RowWeek = "DELETE [Stock].[dbo].[RowWeek_%s] Where Date >= '%s 00:00:00.000'"  % (xTicker,SqlMaxDate)