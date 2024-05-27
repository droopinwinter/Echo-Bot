SELECT TOP (1000) [Ticker]
      ,[LongShort]
      ,[Buydate]
      ,[Selldate]
      ,[buyPrice]
      ,[SellPrice]
      ,[profit]
      ,[CreatDate]
  FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 10 and  12 and profit >0
  and CreatDate >= '2024-05-26 21:15:43.023'


SELECT * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 10 and  12 and profit >0
  and CreatDate >= '2024-05-26 22:54:16.880'

SELECT * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 10 and  12 and profit <0
  and CreatDate >= '2024-05-26 22:54:16.880'

SELECT * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 20 and  21 and profit >0
  and CreatDate >= '2024-05-26 22:54:16.880'

SELECT * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 20 and  21 and profit <0
  and CreatDate >= '2024-05-26 22:54:16.880'

  SELECT * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 1 and  9 and profit >0
  and CreatDate >= '2024-05-26 22:54:16.880'

    SELECT * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE LongShort between 1 and  9 and profit <0
  and CreatDate >= '2024-05-26 21:18:43.023'


  DECLARE  @Dtime datetime
  SET @Dtime = '2024-05-26 22:54:16.880'
  
SELECT count(*) cnt, sum(profit) TotEarn 
FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 20 and  21 and profit >0
and CreatDate >= @Dtime

SELECT count(*) cnt, sum(profit) TotEarn 
FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 20 and 21 and profit <0
and CreatDate >= @Dtime

SELECT count(*) cnt, sum(profit) TotEarn 
FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 1 and  10 and profit >0
and CreatDate >= @Dtime

SELECT count(*) cnt, sum(profit) TotEarn 
FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 1 and 10 and profit <0
and CreatDate >= @Dtime