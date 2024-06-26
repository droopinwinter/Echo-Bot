#import yfinance as yf
#tsm = yf.Ticker('TSM')
#print(tsm.info)
# 語法是 yf.download(
#    股票代號,
#    start=開始日期,
#    end=完結日期
#    )
#yf.download('^IXIC',start='2016-01-01',end='2021-01-01')

import yfinance as yf
import time


stk_list = [
 'SPY','QQQ','DIA','IWM','SOXX','UVXY','SVIX','DXY','CL','TMF','SOXL'
,'TSLA' ,'APPLE','NVDA','MSFT','AMZN','NFLX','META','AMD','GOOGL','MU'
,'FNGU','SOXL','XBI','XLE','CL','XLF','XME','XLV','XLP','IYR','XLU','XLI'
]

stk_list1 = [
 'DX-Y.NYB',
]
# 先測試一檔試看看
stock = yf.Ticker('DX-Y.NYB')
yf.download('DX-Y.NYB',period='1mo',interval='90m').to_csv('Hprice_IXIC.csv')
# 取得價量資料＋股利發放資料＋股票分割資料
'''
stock.history(period = 'max')

# 創立一個紀錄失敗股票的 list
failed_list = []

# 開始迴圈抓資料囉！
for i in stk_list1:
    try : 
        # 打印出目前進度
        print('processing: ' + i)
        # 填入股票代碼後直接下載成 csv 格式
        stock = yf.Ticker(i)
        stock.history(period = 'max').to_csv('price_'+i+'.csv')
        # 停一秒，再抓下一檔，避免對伺服器造成負擔而被鎖住
        time.sleep(1)
    except :
        failed_list.append(i)
        continue

'''
