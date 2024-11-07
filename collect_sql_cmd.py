#collect_sql_cmd
s_Stock_Ticker  = 'select * FROM [Stock].[dbo].[Ticker] '
#xTicker = ''
#SqlMaxDate =''
#s_LastHour = ''
#s_LastDay  = ''
#s_LastWeek = ''
#d_Stock_RowHour = ''
#d_Stock_RowDay  = ''
#d_Stock_RowWeek = ''

def SLastHour( xTicker):
    return "select top 1 max(Datetime) Date FROM [Stock].[dbo].[RowHour_%s]" % (xTicker)

def SLastDay( xTicker):
    return 'select top 1 max(Date)     Date FROM [Stock].[dbo].[RowDay_%s]'  % (xTicker) 

def SLastWeek( xTicker):
    return 'select top 1 max(Date)     Date FROM [Stock].[dbo].[RowWeek_%s]' % (xTicker)


def DelDupHour( xTicker, SqlMaxDate):
    return "DELETE [Stock].[dbo].[RowHour_%s] Where Datetime >= '%s 00:00:00.000'"  % (xTicker,SqlMaxDate)

def DelDupDay( xTicker, SqlMaxDate):
    return "DELETE [Stock].[dbo].[RowDay_%s] Where Date >= '%s 00:00:00.000'"  % (xTicker,SqlMaxDate)

def DelDupWeek( xTicker, SqlMaxDate):
    return "DELETE [Stock].[dbo].[RowWeek_%s] Where Date >= '%s 00:00:00.000'"  % (xTicker,SqlMaxDate)