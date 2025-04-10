#symbol2Chtext


def TWsymbol2Chtext(xSymbol):
  match xSymbol:
    #case "": return "JavaScript"
    case "2330.TW":    return "TSMC"
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
    case"SPY"   : return"標普指"
    case"QQQ"   : return"納斯達克指"
    case"DIA"   : return"道瓊指"
    case"IWM"   : return"羅素指"
    case"SOXX"  : return"費半指"
    case"CL"    : return"WTI原油"
    case"TLT"   : return"20年美債正"
    case"TMV"   : return"20年美債反3"
    case"^TWII" : return"台灣指數"
    case"FNGU"  : return"尖牙正3"
    case"SOXL"  : return"費半正3"
    case"XBI"   : return"生技股"
    case"XLE"   : return"能源股"
    case"XLF"   : return"金融股"
    case"XME"   : return"金礦股"
    case"XLV"   : return"醫保股"
    case"XLP"   : return"消費股"
    case"IYR"   : return"地產股"
    case"XLU"   : return"公用股"
    case"XLI"   : return"工業股"
    case"TSLA"  : return"特斯拉"
    case"AAPL"  : return"蘋果"  
    case"NVDA"  : return"英偉達"
    case"MSFT"  : return"微軟"  
    case"AMZN"  : return"亞馬遜" 
    case"NFLX"  : return"奈飛"  
    case"META"  : return"臉書"  
    case"AMD"   : return"美超微" 
    case"GOOGL" : return"谷哥"  
    case"INTC"  : return"英特爾" 
    case"MU"    : return"美光"  
    case"TSM"   : return"台積電ADR"
    case"^N225" : return"日經指數"
    case"^KS11" : return"韓國指數"
    case "00762.TW"   :"元大全球AI"
    case "00832.TW"   :"國泰費城半導體"
    case "00688L.TW"  :"國泰20年美債正2"
    case "006881R.TW" :"元大美債20反"
    case "00830.TW"   :"國泰費城半導體"
    case _:            return xSymbol 

def USsymbol2Chtext(xSymbol):
  match xSymbol:
    case"SPY"   : return"標普500指"
    case"QQQ"   : return"納斯達克指"
    case"DIA"   : return"道瓊指"
    case"IWM"   : return"羅素指"
    case"SOXX"  : return"費半指"
    case"CL"    : return"WTI原油"
    case"TLT"   : return"20年美債正"
    case"TMV"   : return"20年美債反3"
    case"^TWII" : return"台灣指數"
    case"FNGU"  : return"尖牙正3"
    case"SOXL"  : return"費半正3"
    case"XBI"   : return"生技股"
    case"XLE"   : return"能源股"
    case"XLF"   : return"金融股"
    case"XME"   : return"金礦股"
    case"XLV"   : return"醫保股"
    case"XLP"   : return"消費股"
    case"IYR"   : return"地產股"
    case"XLU"   : return"公用股"
    case"XLI"   : return"工業股"
    case"TSLA"  : return"特斯拉"
    case"AAPL"  : return"蘋果"  
    case"NVDA"  : return"英偉達"
    case"MSFT"  : return"微軟"  
    case"AMZN"  : return"亞馬遜" 
    case"NFLX"  : return"奈飛"  
    case"META"  : return"臉書"  
    case"AMD"   : return"美超微" 
    case"GOOGL" : return"谷哥"  
    case"INTC"  : return"英特爾" 
    case"MU"    : return"美光"  
    case"TSM"   : return"台積電"
    case"^N225" : return"日經指數"
    case"^KS11" : return"韓國指數"
    case _     :  return xSymbol

def USdf2Chtext(df):
    df1=df.replace({"STK":{
                        '2330.TW':   '台積電'
                        ,'2317.TW':  '鴻海'
                        ,'2454.TW':  '聯發科'
                        ,'2881.TW':  '富邦金'
                        ,'2382.TW':  '廣達'
                        ,'2882.TW':  '國泰金'
                        ,'2412.TW':  '中華電'
                        ,'2308.TW':  '台達電'
                        ,'2891.TW':  '中信金'
                        ,'3711.TW':  '日月光'
                        ,'2303.TW':  '聯電'
                        ,'2886.TW':  '兆豐金'
                        ,'6505.TW':  '台塑化'
                        ,'1216.TW':  '統一'
                        ,'2884.TW':  '玉山金'
                        ,'3045.TW':  '台灣大'
                        ,'2885.TW':  '元大金'
                        ,'0050.TW':  '元台灣50'
                        ,'2603.TW':  '長榮'
                        ,'2357.TW':  '華碩'
                        ,'^TWII':    '台灣指數'
                        ,'^N225':    '日經指數'
                        ,'^KS11':    '韓國指數'
                        ,'00642U.TW':'元石油'
                        ,'00674R.TW':'元黃金反1'
                        ,'00707R.TW':'元日圓反1'
                        ,'00738U.TW':'元白銀'
                        ,'00708L.TW':'元黃金正2'
                        ,'00635U.TW':'元黃金'
                        ,'00693U.TW':'街口黃豆'
                        ,'00763U.TW':'街口銅'
                        ,'00681R.TW':'元美債20反1'
                        ,'00688L.TW':'國泰美債正2'
                        ,'00645.TW': '富邦日本'
                        ,'00661.TW': '元日經'
                        ,'00685L.TW':'群益台正2'
                        ,'006208.TW':'富邦台50'
                        ,'00631L.TW':'元台灣50正2'
                        ,'00632R.TW':'元台灣50反1'
                        ,'00676R.TW':'富邦臺灣反1'
                        ,'00663L.TW':'國泰臺灣正2'
                        ,'00709.TW': '富邦歐洲'
                        ,'00660.TW': '元歐洲50'
                        ,'00640L.TW':'富邦日本正2'
                        ,'00911.TW': '兆豐半導'
                        ,'00830.TW':'國泰費半'
                        ,'00762.TW':'元全球AI'
                        ,'00682U.TW':'元美元指數'
                        ,'00683L.TW':'元美元指正2'
                        ,'SPY':  '標普500指'
                        ,'QQQ':  '納斯達克指'
                        ,'DIA':  '道瓊指'
                        ,'IWM':  '羅素指'
                        ,'SOXX': '費半指'
                        ,'CL':   'WTI原油'
                        ,'TLT':  '20年美債正'
                        ,'TMV':  '20年美債反3'
                        ,'^TWII':'台灣指'
                        ,'^N225':'日經指'
                        ,'^KS11':'南韓指'
                        ,'FNGU': '尖牙正3'
                        ,'SOXL': '費半正3'
                        ,'XBI':  '生技股'
                        ,'XLE':  '能源股'
                        ,'XLF':  '金融股'
                        ,'XME':  '金礦股'
                        ,'XLV':  '醫保股'
                        ,'XLP':  '消費股'
                        ,'IYR':  '地產股'
                        ,'XLU':  '公用股'
                        ,'XLI':  '工業股'
                        ,'TSLA': '特斯拉'
                        ,'AAPL': '蘋果'
                        ,'NVDA': '英偉達'
                        ,'MSFT': '微軟'
                        ,'AMZN': '亞馬遜'
                        ,'NFLX': '奈飛'
                        ,'META': '臉書'
                        ,'AMD':  '美超微'
                        ,'GOOGL':'谷哥'
                        ,'INTC': '英特爾'
                        ,'MU':   '美光'
                        ,'TSM':  '台積電'
                          },
                        "buy":{
                          1: '波段做多'
                         ,2: '波段做多'
                         ,3: '波段做多'
                         ,4: '波段做多'
                         ,5: '波段做多'
                         ,6: '波段做多'
                         ,7: '波段做多'
                         ,8: '波段做多'
                         ,9: '波段做多'
                         ,0: ' '
                         ,10: '極端做多'
                         ,20: '漲勢做多'
                         ,-1: '波段做空'
                         ,-2: '波段做空'
                         ,-3: '波段做空'
                         ,-4: '波段做空'
                         ,-5: '波段做空'
                         ,-6: '波段做空'
                         ,-7: '波段做空'
                         ,-8: '波段做空'
                         ,-9: '波段做空'
                         ,-10:'極端做空'
                         ,-20:'跌勢做空'
                          },
                        "St":{
                          1: '波段多'
                         ,2: '波段多'
                         ,3: '波段多'
                         ,4: '波段多'
                         ,5: '波段多'
                         ,6: '波段多'
                         ,7: '波段多'
                         ,8: '波段多'
                         ,9: '波段多'
                         ,0: '一一一'
                         ,10: '極端多'
                         ,20: '趨勢多'
                         ,-1: '波段空'
                         ,-2: '波段空'
                         ,-3: '波段空'
                         ,-4: '波段空'
                         ,-5: '波段空'
                         ,-6: '波段空'
                         ,-7: '波段空'
                         ,-8: '波段空'
                         ,-9: '波段空'
                         ,-10:'極端空'
                         ,-20:'趨勢空'
                          },
                        "Sell":{
                          -101: '波段回補'
                         ,-102: '波段回補'
                         ,-103: '波段回補'
                         ,-104: '波段回補'
                         ,-105: '波段回補'
                         ,-106: '波段回補'
                         ,-107: '波段回補'
                         ,-108: '波段回補'
                         ,-109: '波段回補'
                         ,-110: '短空回補'
                         ,-120: '跌勢回補'
                         ,0: ' '
                         ,101: '波段止盈'
                         ,102: '波段止盈'
                         ,103: '波段止盈'
                         ,104: '波段止盈'
                         ,105: '波段止盈'
                         ,106: '波段止盈'
                         ,107: '波段止盈'
                         ,108: '波段止盈'
                         ,109: '波段止盈'
                         ,110: '短多止盈'
                         ,120: '漲勢止盈'
                         ,202: '波段止損'
                         ,203: '波段止損'
                         ,204: '波段止損'
                         ,205: '波段止損'
                         ,206: '波段止損'
                         ,207: '波段止損'
                         ,208: '波段止損'
                         ,209: '波段止損'
                         ,210: '短多止損'
                         ,220: '漲勢止損'
                         ,-220: '跌勢止損'
                         ,220:  '漲勢止損'
                         ,-210: '回檔止損'
                         ,210:  '反彈止損'
                          },
                        "TYP":{
                          'ind'  : '指'
                         ,'etf'  : '基'
                         ,'sto'  : '股'
                         ,'mai'  : '期'
                          }                          
                          })
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

