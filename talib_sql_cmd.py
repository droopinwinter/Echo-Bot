#talib_sql_cmd
s_Stock_TechAnalysis = 'select * FROM [Stock].[dbo].[TechAnalysis] '
s_Stock_Ticker  = 'select * FROM [Stock].[dbo].[Ticker] '

def SLastHour( xTicker):
    return f'select max(Date) Date FROM [analsy].[dbo].AnalysHour_{xTicker}'

def SLastDay( xTicker):
    return f'select max(Date) Date FROM [analsy].[dbo].AnalysDay_{xTicker}'    

def S1000StockHour( xTicker):
    return f'select top 1000 Datetime Date FROM [Stock].[dbo].[RowHour_{xTicker}] order by date desc'

def S1000StockDay( xTicker):
    return f'select top 1000 Date FROM [Stock].[dbo].[RowDay_{xTicker}] order by date desc'



def DelLastDay( xTicker, SqlMaxDate):
    return f"DELETE [analsy].[dbo].AnalysDay_{xTicker} Where Date >= '{SqlMaxDate} 00:00:00.000'"

def DelLastHour( xTicker, SqlMaxDate):
    return f"DELETE [analsy].[dbo].AnalysHour_{xTicker} Where Date >= '{SqlMaxDate} 00:00:00.000'"


def SPeriodDay( xTicker,SqlMinDate):
    return f"select * FROM [Stock].[dbo].[RowDay_{xTicker}] where date >='{SqlMinDate} 00:00:00.000'"

def SPeriodHour( xTicker,SqlMinDate):
    return f"select * FROM [Stock].[dbo].[RowHour_{xTicker}] where datetime >='{SqlMinDate} 00:00:00.000'"


def DelDupDay( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date] ORDER BY (SELECT NULL))"+\
            f"	FROM [analsy].[dbo].AnalysDay_{xTicker}) AS T WHERE DupRank > 1"
def DelDupHour( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date] ORDER BY (SELECT NULL))"+\
            f"	FROM [analsy].[dbo].AnalysHour_{xTicker}) AS T WHERE DupRank > 1"  