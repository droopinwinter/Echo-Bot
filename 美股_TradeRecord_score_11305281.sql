DECLARE @CrTime Datetime
SET @CrTime = '2024-05-28 17:29:45.120'--GETDATE()-0.009

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

  SELECT top 20 * FROM [trade].[dbo].[TradeRecord_SPY]
  WHERE Ticker <> 'SPY ' and CreatDate >= @CrTime
