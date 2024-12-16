# notify_sql_cmd

def DelDupDay( countyr):
    return  "DELETE T FROM ("+\
            "	SELECT *, DupRank = ROW_NUMBER() OVER (PARTITION BY [date], [xremark] ORDER BY (SELECT NULL))"+\
            f"	FROM [apka].[dbo].[ApkaDay_Combin_{countyr}]) AS T WHERE DupRank > 1"

def DelLastDay( countyr, SqlMaxDate):
    return f"DELETE [analsy].[dbo].[ApkaDay_Combin_{countyr}] Where Date >= '{SqlMaxDate} 00:00:00.000'"
#=================================================
# 買賣徵兆
def Sig2BuySell( befDate, countyr):
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()"     
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"  
        mark    = "substring([xremark],4,5)"  
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"  
    #return f"SELECT distinct [date],left(TYP,3) TYP,[buySig] buy,[SellSig] Sell,[OscSum] Osc,[xmacd] MACD ,{mark} STK"+\
    return f"SELECT distinct [date],left(TYP,3) TYP,[buySig] buy,[SellSig] Sell,[xmacd] MACD ,{mark} STK"+\
    f" FROM [apka].[dbo].[ApkaDay_Combin_{countyr}] "+\
    f" where date {dateR} AND ( buySig <>0 or SellSig <> 0) {IfTw} order by date,typ "

#=================================================
# 接近布林帶下沿
def Sig2LowBull( befDate, countyr):
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        dateR   = f"between GETDATE()-1 and  GETDATE()"       
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"      
        mark    = "substring([xremark],4,5)"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"  
    return f"SELECT distinct [date],left(TYP,3) TYP,[BBlevel] BB,[OscSum] Osc,[TrnSlop] slp ,{mark} STK "+\
       f" FROM [apka].[dbo].[ApkaDay_Combin_{countyr}] "+\
       f" where date {dateR} AND ([BBlevel]<0.2 ) and [OscSum] >=3 {IfTw} order by date,typ "

#=================================================
# 接近布林帶上沿
def Sig2HighBull( befDate, countyr):
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        dateR   = f"between GETDATE()-1 and  GETDATE()"   
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"  
        mark    = "substring([xremark],4,5)"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"
    return f"SELECT distinct [date],left(TYP,3) TYP,[BBlevel] BB,[OscSum] Osc ,{mark} STK "+\
       f" FROM [apka].[dbo].[ApkaDay_Combin_{countyr}]  "+\
       f" where date {dateR} AND (([BBlevel]>0.9 and [OscSum] <=-3) or ([BBlevel]<0.1 and [OscSum] >=3))  {IfTw} order by date,typ"
#=================================================
# 當日收盤後技術分析擺盪
def Sig2Osc( befDate, countyr):
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        dateR   = f"between GETDATE()-1 and  GETDATE()" 
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"  
        mark    = "substring([xremark],4,5)"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"
    return f"SELECT  distinct [date],left(TYP,3) TYP,[buy],[OscSum] Osc,[BBlevel] BB, {mark} STK "+\
       f" FROM [apka].[dbo].[ApkaDay_Combin_{countyr}] "+\
       f" where date {dateR}  {IfTw} "+\
       " order by date,xremark"
#=================================================
# 當日收盤後技術分析趨勢＿股指前11個
#Sql5 = "SELECT  distinct [date],[xema] ema,[xmacd] mcd,[TrnSlop] slp,[OscSum] Os,[BBlevel] BB,[xremark] typ "+\
#       " FROM [apka].[dbo].[ApkaDay_Combin] "+\
#       " where date > GETDATE()-2 "+\
#       " order by date,xremark"
def Sig2TrendAndOsc_part1( befDate, countyr):
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        #range   = "'01' and '80'"
        range   = " '01' and '22'"
        dateR   = f"between GETDATE()-1 and  GETDATE()"
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"
        mark    = "substring([xremark],4,5)"
        range   = "'01' and '80'"
        range   = "'01' and '22'"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"
    return "SELECT [date],TYP,[BBlevel] BB,[OscSum] OSC,[xmacd] MCD,[buy] St,[mark] STK FROM ( "+\
      "  SELECT distinct [date],left(TYP,3) TYP,[xema],[xmacd],[TrnSlop],[buySig],[SellSig],[buy],[OscSum] "+\
      f"  ,[BBlevel], substring([xremark],1,2) pre, {mark} mark "+\
      f"  FROM [apka].[dbo].[ApkaDay_Combin_{countyr}] where date {dateR} {IfTw} "+\
      f"  and typ in ('etf','index','main') ) a order by typ,pre "
#=================================================
# 當日收盤後技術分析趨勢＿板塊11個
def Sig2TrendAndOsc_part2( befDate, countyr):
    
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        range   = "'23' and '44'"  
        dateR   = f"between GETDATE()-1 and  GETDATE()"
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"  
        mark    = "substring([xremark],4,5)"
        range   = "'23' and '44'"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"
    return "SELECT [date],TYP,[BBlevel] BB,[OscSum] Osc,[xmacd] MCD,[buy] St,[mark] STK FROM ( "+\
      "  SELECT distinct [date],left(TYP,3) TYP,[xema],[xmacd],[TrnSlop],[buySig],[SellSig],[buy],[OscSum] "+\
      f"  ,[BBlevel], substring([xremark],1,2) pre, {mark} mark "+\
      f"  FROM [apka].[dbo].[ApkaDay_Combin_{countyr}] where date  {dateR} {IfTw} "+\
      f"  and typ in ('stock')  ) a order by typ,pre "

#=================================================
# 當日收盤後技術分析趨勢＿大科技＿11個
def Sig2TrendAndOsc_part3( befDate, countyr):
    if countyr == 'TW':
        IfTw = "and right([xremark], 3) = '.TW'"
        mark    = "substring([xremark],4,10)"
        range   = "'44' and '60'"
        dateR   = f"between GETDATE()-1 and  GETDATE()"
    else:
        IfTw = "and right([xremark], 3) <> '.TW'"
        mark    = "substring([xremark],4,5)"  
        range   = "'22' and '40'"
        dateR   = f"between GETDATE()-{befDate} and  GETDATE()-1"
    return "SELECT [date],[buy] Sta,[BBlevel] BB,[OscSum] OSC,[xmacd] MCD,[mark] STK FROM ( "+\
      "  SELECT distinct [date],[xema],[xmacd],[TrnSlop],[buySig],[SellSig],[buy],[OscSum] "+\
      f"  ,[BBlevel], substring([xremark],1,2) pre, {mark} mark "+\
      f"  FROM [apka].[dbo].[ApkaDay_Combin_{countyr}] where date  {dateR}  {IfTw} "+\
      f" and left([xremark], 2) between {range} ) a order by typ,pre "