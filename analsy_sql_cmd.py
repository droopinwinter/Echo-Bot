#analsy_sql_cmd


def DelDupDay( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date] ORDER BY (SELECT NULL))"+\
            f"	FROM [apka].[dbo].ApkaDay_{xTicker}) AS T WHERE DupRank > 1"
def DelDupHour( xTicker):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [Datetime] ORDER BY (SELECT NULL))"+\
            f"	FROM [apka].[dbo].ApkaHour_{xTicker}) AS T WHERE DupRank > 1"  