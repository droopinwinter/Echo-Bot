from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import datetime as dt

# 填入美國時區資訊
pytrends = TrendReq(hl = 'en-US', tz = 360)

# 如果想要知道現在美國地區的人都在搜尋什麼，可以這樣查詢
pytrends.trending_searches(pn = 'united_states')

# kw_list 就是 keyworld list 的意思，我們這邊有興趣的是股票代碼被搜尋的熱度變化，以 AAPL 為例
kw_list = ['AAPL']

# 然後就可以透過 build_payload 建立查詢作業，再用 interest_over_time() 呈現數據
# 其中的　timeframe 參數很重要！它會改變你的數據格式
#  填入 'all' 就是全期資料，資料會以月頻率更新；
#  填入 'today 5-y' 就是至今的五年，只能設定 5 年，資料會以週頻率更新；
#  填入 'today 3-m' 就是至今的三個月，只能設定 1,2,3 月，資料會以日頻率更新；
#  填入 'now 7-d' 就是至今的七天，只能設定 1,7 天，資料會以小時頻率更新；
#  填入 'now 1-H' 就是至今的一小時，只能設定 1,4 小時，資料會以每分鐘頻率更新；
#  填入 '2015-01-01 2019-01-01' 就是 2015 年初至 2019 年初
pytrends.build_payload(kw_list, timeframe = 'today 3-m')
pytrends.interest_over_time()

# 如果需要長期間的高頻的資料，可以這樣查詢
# 但建議做大樣本查詢的時候，sleep 參數最好設定一下！否則流量的問題有可能查詢作業會被中斷喔！
pytrends.get_historical_interest(kw_list, 
                                 year_start = 2018, month_start = 1, day_start = 1, hour_start = 0,
                                 year_end = 2019, month_end = 2, day_end = 1, hour_end = 0, sleep = 0)
pytrends.interest_over_time()

# 建立一個 DataFrame 存放所有股票代碼的搜尋熱度數據，這裡以日頻率資料作為示範
# 剛剛的高頻查詢方式可以滿足這裡日頻率的要求，但如果要查滿多年的高頻資料，可能要等上很久
# 偏偏 timeframe 的設定有諸多限制，我希望資料是日頻率的話，只能選擇 'today 3-m' 的查詢方式
# 但我想要建一份長期資料例如 10 年資料表，該怎麼辦呢？
# 有一個取巧方式就是用日期對日期的方式查詢，日期之間的差距不要超過 270 天，回傳的資料就會是日頻率
# 所以用迴圈，每 270 天推進，抓到的資料就會是日頻率
trend_data = pd.DataFrame(index = pd.date_range(start = '2008-01-01', end = dt.datetime.today(), freq = 'D'))

# 還記得 stk_list 嗎？沒錯就是我們上面從 slickchart 抓下來的 S&P 500 成份股喔，我們稍微做一個排序
stk_list = stk_list.sort_values()

# 開始迴圈爬搜尋熱度資料吧！
for rnd in range(int(np.ceil(len(trend_data) / 270))):
    # 打印出目前的回合
    print('processing round :' + str(rnd))
    # 設定目前這回合 270 天的日期資訊
    date_list = list(trend_data.index[270*rnd:270*(rnd+1)])
    start_date = date_list[0].strftime('%Y-%m-%d')
    end_date = date_list[-1].strftime('%Y-%m-%d')
    
    # 第二層迴圈，在這個日期區間，查詢每一檔股票的日頻搜尋熱度資料，並填入表格
    for stk in stk_list:
        kw_list = [stk]
        pytrends.build_payload(kw_list, timeframe = start_date + ' ' + end_date)
        try : 
            trend_data.loc[date_list, stk] = pytrends.interest_over_time()[stk]
        except : 
            trend_data.loc[date_list, stk] = np.nan
    time.sleep(5)
trend_data


#資料合併在一起的時候，每一段資料標準化的依據都是不同的！因此我們還需要做一些調整
# 設定全期間的日期
start_date = trend_data.index[0].strftime('%Y-%m-%d')
end_date = trend_data.index[-1].strftime('%Y-%m-%d')

# 迴圈讓逐檔個股標準化調整
for stk in stk_list:
    # 查詢全期的搜尋熱度值
    kw_list = [stk]
    pytrends.build_payload(kw_list, timeframe = start_date + ' ' + end_date)
    pytrends.interest_over_time()[stk]
    
    # 創立一個暫時性的 DataFrame，填入全期的搜尋熱度值
    temp_df = pd.DataFrame({'period': trend_data[stk]})
    temp_df['full_period'] = pytrends.interest_over_time()[stk]
    
    # 因為全期的搜尋，被限制只能取得月頻資料，因此我們要進行缺值填補的動作
    temp_df = temp_df.fillna(method = 'pad')
    
    # 全期的數值依據全期的最大值計算相對比例，在 Google Trend 的模式下也就是除以 100
    temp_df['full_period_ratio'] = temp_df.full_period / temp_df.full_period.max()
    
    # 進行原表格數據標準化調整，然後取代原表格數據
    temp_df['corrected_period'] = temp_df.period * temp_df.full_period_ratio
    trend_data[stk] = temp_df.corrected_period

# 看看最終的 Google Trends 搜尋熱度資料吧！
trend_data