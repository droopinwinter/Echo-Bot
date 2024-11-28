#symbol2Chtext
import pandas as pd

def TWsymbol2Chtext(xSymbol):
    match xSymbol:
        #case "": return "JavaScript"
        case "2330.TW":    return "台積電"
        case "2317.TW":    return "鴻海"
        case "2454.TW":    return "聯發科"
        case "2881.TW":    return "富邦金"
        case "2382.TW":    return "廣達"
        case "2882.TW":    return "國泰金"
        case "2412.TW":    return "中華電"
        case "2308.TW":    return "台達電"
        case "2891.TW":    return "中信金"
        case "3711.TW":    return "日月光投控"
        case "2303.TW":    return "聯電"
        case "2886.TW":    return "兆豐金"
        case "6505.TW":    return "台塑化"
        case "1216.TW":    return "統一"
        case "2884.TW":    return "玉山金"
        case "3045.TW":    return "台灣大"
        case "2885.TW":    return "元大金"
        case "0050.TW":    return "元大台灣50"
        case "2603.TW":    return "長榮"
        case "00632R.TW":  return "元大台灣50反1"
        case "00676R.TW":  return "富邦臺灣加權反1"
        case "00674R.TW":  return "期元大S&P黃金反1"
        case "00707R.TW":  return "期元大S&P日圓反1"
        case "^TWII":      return "台灣加權指數"
        case "^N225":      return "日經指數"
        case "^KS11":      return "韓國指數"
        case "006208.TW":  return "富邦台50"
        case "2357.TW":    return "華碩"
        case "00631L.TW":  return "元大台灣50正2"
        case "00642U.TW":  return "期元大S&P石油"
        case "00645.TW":   return "富邦日本"
        case "00661.TW":   return "元大日經225"
        case "00685L.TW":  return "群益臺灣加權正2"
        case "00738U.TW":  return "期元大道瓊白銀"
        case "00708L.TW":  return "期元大S&P黃金正2"
        case "00640L.TW":  return "富邦日本正2"
        case "00635U.TW":  return "期元大S&P黃金"
        case "00693U.TW":  return "期街口S&P黃豆"
        case "00763U.TW":  return "期街口道瓊銅"
        case "00683L.TW":  return "期元大美元指正2"
        case "00663L.TW":  return "國泰臺灣加權正2"
        case "00709.TW" :  return "富邦歐洲"
        case "00660.TW" :  return "元大歐洲50"
        case "00682U.TW":  return "期元大美元指數" 
               
def USdf2Chtext(df):
    df1=df.replace({"typ":{
                        '2330.TW':   '股_台積電'
                        ,'2317.TW':  '股_鴻海'
                        ,'2454.TW':  '股_聯發科'
                        ,'2881.TW':  '股_富邦金'
                        ,'2382.TW':  '股_廣達'
                        ,'2882.TW':  '股_國泰金'
                        ,'2412.TW':  '股_中華電'
                        ,'2308.TW':  '股_台達電'
                        ,'2891.TW':  '股_中信金'
                        ,'3711.TW':  '股_日月光投控'
                        ,'2303.TW':  '股_聯電'
                        ,'2886.TW':  '股_兆豐金'
                        ,'6505.TW':  '股_台塑化'
                        ,'1216.TW':  '股_統一'
                        ,'2884.TW':  '股_玉山金'
                        ,'3045.TW':  '股_台灣大'
                        ,'2885.TW':  '股_元大金'
                        ,'0050.TW':  '股_元大台灣50'
                        ,'2603.TW':  '股_長榮'
                        ,'2357.TW':  '股_華碩'
                        ,'^TWII':    '指_台灣加權指數'
                        ,'^N225':    '指_日經指數'
                        ,'^KS11':    '指_韓國指數'
                        ,'00642U.TW':'期_元大S&P石油'
                        ,'00674R.TW':'期_元大S&P黃金反1'
                        ,'00707R.TW':'期_元大S&P日圓反1'
                        ,'00738U.TW':'期_元大道瓊白銀'
                        ,'00708L.TW':'期_元大S&P黃金正2'
                        ,'00635U.TW':'期_元大S&P黃金'
                        ,'00693U.TW':'期_街口S&P黃豆'
                        ,'00763U.TW':'期_街口道瓊銅'
                        ,'00683L.TW':'期_元大美元指正2'
                        ,'00682U.TW':'期_元大美元指數'
                        ,'00645.TW': 'ETF_富邦日本'
                        ,'00661.TW': 'ETF_元大日經225'
                        ,'00685L.TW':'ETF_群益臺灣加權正2'
                        ,'006208.TW':'ETF_富邦台50'
                        ,'00631L.TW':'ETF_元大台灣50正2'
                        ,'00632R.TW':'ETF_元大台灣50反1'
                        ,'00676R.TW':'ETF_富邦臺灣加權反1'
                        ,'00663L.TW':'ETF_國泰臺灣加權正2'
                        ,'00709.TW': 'ETF_富邦歐洲'
                        ,'00660.TW': 'ETF_元大歐洲50'
                        ,'00640L.TW':'ETF_富邦日本正2'
                        ,'SPY':  '指_標普500指'
                        ,'QQQ':  '指_納斯達克100指'
                        ,'DIA':  '指_道瓊斯30指'
                        ,'IWM':  '指_羅素小盤股指'
                        ,'SOXX': '指_費城半導體指'
                        ,'CL':   '期_WTI原油期貨'
                        ,'TLT':  '期_20年美債ETF正'
                        ,'TMV':  '期_20年美債ETF反3'
                        ,'^TWII':'指_台灣加權指'
                        ,'^N225':'指_日經255指'
                        ,'^KS11':'指_南韓綜合指'
                        ,'FNGU': 'ETF_大科技正3'
                        ,'SOXL': 'ETF_費半正3'
                        ,'XBI':  'ETF_生物科技'
                        ,'XLE':  'ETF_能源股'
                        ,'XLF':  'ETF_金融股'
                        ,'XME':  'ETF_礦業金屬股'
                        ,'XLV':  'ETF_醫療保健股'
                        ,'XLP':  'ETF_日常消費'
                        ,'IYR':  'ETF_房地產股'
                        ,'XLU':  'ETF_公用事業'
                        ,'XLI':  'ETF_工業股'
                        ,'TSLA': '股_特斯拉'
                        ,'AAPL': '股_蘋果'
                        ,'NVDA': '股_英偉達'
                        ,'MSFT': '股_微軟'
                        ,'AMZN': '股_亞馬遜'
                        ,'NFLX': '股_奈飛'
                        ,'META': '股_臉書'
                        ,'AMD':  '股_美國超微'
                        ,'GOOGL':'股_谷哥'
                        ,'INTC': '股_英特爾'
                        ,'MU':   '股_美光'
                        ,'TSM':  '股_台積電ADR'
                          },
                        "buy":{
                          1: '做多'
                         ,2: '做多'
                         ,3: '做多'
                         ,4: '做多'
                         ,5: '做多'
                         ,6: '做多'
                         ,7: '做多'
                         ,8: '做多'
                         ,9: '做多'
                         ,10: '做多'
                         ,20: '做多'
                         ,101: '止盈'
                         ,102: '止盈'
                         ,103: '止盈'
                         ,104: '止盈'
                         ,105: '止盈'
                         ,106: '止盈'
                         ,107: '止盈'
                         ,108: '止盈'
                         ,109: '止盈'
                         ,110: '止盈'
                         ,120: '止盈'
                         ,-1: '做空'
                         ,-2: '做空'
                         ,-3: '做空'
                         ,-4: '做空'
                         ,-5: '做空'
                         ,-6: '做空'
                         ,-7: '做空'
                         ,-8: '做空'
                         ,-9: '做空'
                         ,-10:'做空'
                         ,-20:'做空'
                          },
                        "Sta":{
                          1: '多'
                         ,2: '多'
                         ,3: '多'
                         ,4: '多'
                         ,5: '多'
                         ,6: '多'
                         ,7: '多'
                         ,8: '多'
                         ,9: '多'
                         ,10: '多'
                         ,20: '多'
                         ,-1: '空'
                         ,-2: '空'
                         ,-3: '空'
                         ,-4: '空'
                         ,-5: '空'
                         ,-6: '空'
                         ,-7: '空'
                         ,-8: '空'
                         ,-9: '空'
                         ,-10:'空'
                         ,-20:'空'
                          },
                        "Sell":{
                          -101: '回補'
                         ,-102: '回補'
                         ,-103: '回補'
                         ,-104: '回補'
                         ,-105: '回補'
                         ,-106: '回補'
                         ,-107: '回補'
                         ,-108: '回補'
                         ,-109: '回補'
                         ,-110: '回補'
                         ,-120: '回補'
                         ,101: '止盈'
                         ,102: '止盈'
                         ,103: '止盈'
                         ,104: '止盈'
                         ,105: '止盈'
                         ,106: '止盈'
                         ,107: '止盈'
                         ,108: '止盈'
                         ,109: '止盈'
                         ,110: '止盈'
                         ,120: '止盈'
                         ,-1: '做空'
                         ,-2: '做空'
                         ,-3: '做空'
                         ,-4: '做空'
                         ,-5: '做空'
                         ,-6: '做空'
                         ,-7: '做空'
                         ,-8: '做空'
                         ,-9: '做空'
                         ,-10:'做空'
                         ,-20:'做空'
                          }})
    return df1

def buy2Chtext(df):
    df1=df.replace({"buy":{
                          1: '做多'
                         ,2: '做多'
                         ,3: '做多'
                         ,4: '做多'
                         ,5: '做多'
                         ,6: '做多'
                         ,7: '做多'
                         ,8: '做多'
                         ,9: '做多'
                         ,10: '做多'
                         ,20: '做多'
                         ,-1: '做空'
                         ,-2: '做空'
                         ,-3: '做空'
                         ,-4: '做空'
                         ,-5: '做空'
                         ,-6: '做空'
                         ,-7: '做空'
                         ,-8: '做空'
                         ,-9: '做空'
                         ,-10:'做空'
                         ,-20:'做空'
                          }})
    return df1
'''
def buydf2Chtext(df):
    df['bi'].replace(to_replace=r'[AB]''[-20--1'],value='持空單',regex=True,inplace=True)
    df['bi'].replace('[20-1' ],value='持多單',regex=True,inplace=True)
    df['bi'].replace('[0'    ],value='觀望中',regex=True,inplace=True)
    return df

def buySigdf2Chtext(df):
    df['buy'].replace(['[120-101','多止盈'],regex=True,inplace=True)
    df['buy'].replace(['[20-1'   ,'做多單'],regex=True,inplace=True)
    return df

def SellSigdf2Chtext(df):
    df['Sell'].replace(['[-120--101','空止盈'],regex=True,inplace=True)
    df['Sell'].replace(['[-20--1'  ,'做空單'],regex=True,inplace=True)    
    return df
'''

