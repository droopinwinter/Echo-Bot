#collect_sql_cmd
#s_Stock_Ticker  = 'select top 1 * FROM [Stock].[dbo].[Ticker] '
s_Stock_Ticker  = 'select * FROM [Stock].[dbo].[Ticker] '
s_Stock_Ticker_TW  = 'select * FROM [Stock].[dbo].[Ticker_TW1] '
#xTicker = ''
#SqlMaxDate =''
#s_LastHour = ''
#s_LastDay  = ''
#s_LastWeek = ''
#d_Stock_RowHour = ''
#d_Stock_RowDay  = ''
#d_Stock_RowWeek = ''

def SLastHour( xTicker):
    return f"select top 1 max(Datetime) Date FROM [Stock].[dbo].[RowHour_{xTicker}]"

def SLastDay( xTicker):
    return f'select top 1 max(Date) Date FROM [Stock].[dbo].[RowDay_{xTicker}]'

def SLastWeek( xTicker):
    return f'select top 1 max(Date) Date FROM [Stock].[dbo].[RowWeek_{xTicker}]'

def DelLastHour( xTicker, SqlMaxDate):
    return f"DELETE [Stock].[dbo].[RowHour_{xTicker}] Where Datetime >= '{SqlMaxDate} 00:00:00.000'"

def DelLastDay( xTicker, SqlMaxDate):
    return f"DELETE [Stock].[dbo].[RowDay_{xTicker}] Where Date >= '{SqlMaxDate} 00:00:00.000'"

def DelLastWeek( xTicker, SqlMaxDate):
    return f"DELETE [Stock].[dbo].[RowWeek_{xTicker}] Where Date >= '{SqlMaxDate} 00:00:00.000'"

def DelDupDay( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date] ORDER BY (SELECT NULL))"+\
            f"	FROM [Stock].[dbo].[RowDay_{xTicker}]) AS T WHERE DupRank > 1"
def DelDupHour( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [Datetime] ORDER BY (SELECT NULL))"+\
            f"	FROM [Stock].[dbo].[RowHour_{xTicker}]) AS T WHERE DupRank > 1"  