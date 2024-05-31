DECLARE @CrTime Datetime
SET @CrTime = GETDATE()-0.0145

SELECT '+·¥ºÝ-¬Õ' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 10 and  11 and profit >0
  and CreatDate >= @CrTime
UNION
SELECT '+·¥ºÝ-Á«' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 10 and  11 and profit <0
  and CreatDate >= @CrTime
UNION
SELECT '-·¥ºÝ-¬Õ' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -10 and  -11 and profit >0
  and CreatDate >= @CrTime
UNION
SELECT '-·¥ºÝ-Á«' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -10 and  -11 and profit <0
  and CreatDate >= @CrTime
UNION
SELECT '+EMA-¬Õ' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 1 and  9 and profit >0
  and CreatDate >= @CrTime
UNION
SELECT '+EMA-Á«' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 1 and  9 and profit <0
  and CreatDate >= @CrTime
UNION
SELECT '-EMA-¬Õ' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -1 and  -9 and profit >0
  and CreatDate >= @CrTime
UNION
SELECT '-EMA-Á«' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -1 and  -9 and profit <0
  and CreatDate >= @CrTime
UNION
SELECT '+MACD-¬Õ' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 10 and  20 and profit >0
  and CreatDate >= @CrTime
UNION
SELECT '+MACD-Á«' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between 10 and  20 and profit <0
  and CreatDate >= @CrTime
  UNION
SELECT '-MACD-¬Õ' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -10 and  -20 and profit >0
  and CreatDate >= @CrTime
UNION
SELECT '-MACD-Á«' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -10 and  -20 and profit <0
  and CreatDate >= @CrTime
UNION
SELECT 'TOT' TYP, count(*) cnt, SUM([profit]) Earn  FROM [trade].[dbo].[TradeRecord_SPY]
WHERE LongShort between -10 and  -20 and profit <0
  and CreatDate >= @CrTime

  SELECT top 50 * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE Ticker like '%Total' and CreatDate >= @CrTime
