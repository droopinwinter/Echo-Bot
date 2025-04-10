from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    ImageMessage    
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent,
    PostbackEvent
)
import GetTxtMsg as Bll
from datetime import datetime
from datetime import timedelta
import os
import os.path

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
Line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

stk_list = [
 'SPY','QQQ','DIA','IWM','SOXX','UVXY','SVIX','DXY','CL','TMF','SOXL'
,'TSLA' ,'APPLE','NVDA','MSFT','AMZN','NFLX','META','AMD','GOOGL','MU'
,'FNGU','SOXL','XBI','XLE','CL','XLF','XME','XLV','XLP','IYR','XLU','XLI'
]
##########################################################################
def ReadText(UseWay, Country):
    #path ="D:\\AI-Line-Bot\\static\\"+ UseWay+"_"+Country+ ".txt"
    path = UseWay+"_"+Country+ ".txt"
    f = open(path, 'r')
    return f.read()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        Line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 加入好友事件
@Line_handler.add(FollowEvent)
def handle_follow(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text ='你好 我是每日每台股交易訊號通知機器人'
                                      +'\n 我使用日K的MACD,Gmma,SRSI,BBand,willan,EFI,Nine7種技術分析'
                                      +'\n 依照1.趨勢2.波段3.極端這3種規則提供下列功能'
                                      +'\n 1.回覆-每日收盤後可進出場標的'
                                      +'\n 2.回覆-主板塊與活躍股整合趨勢'
                                      +'\n 3.回覆-排序出近月內最佳獲利品種'
                                      +'\n 4.回覆-提供標的的進出場交易與獲利圖表'
                                      +'\n 5.列出系統追蹤名單'
                                      )]
            )
        )

@Line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == 'us':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem( action=PostbackAction( label="SPY"  ,data="picSPY"  ,display_text="SPY"   ),),
                    QuickReplyItem( action=PostbackAction( label="QQQ"  ,data="picQQQ"  ,display_text="QQQ"   ),),
                    QuickReplyItem( action=PostbackAction( label="DIA"  ,data="picDIA"  ,display_text="DIA"   ),),
                    QuickReplyItem( action=PostbackAction( label="SOXX" ,data="picSOXX" ,display_text="SOXX"  ),),
                    QuickReplyItem( action=PostbackAction( label="IWM"  ,data="picIWM"  ,display_text="IWM"   ),),
                    QuickReplyItem( action=PostbackAction( label="CL"   ,data="picCL"   ,display_text="CL"    ),),
                    QuickReplyItem( action=PostbackAction( label="TLT"  ,data="picTLT"  ,display_text="TLT"   ),),
                    QuickReplyItem( action=PostbackAction( label="TMV"  ,data="picTMV"  ,display_text="TMV"   ),),
                    QuickReplyItem( action=PostbackAction( label="^TWII",data="pic^TWII",display_text="^TWII" ),),
                    QuickReplyItem( action=PostbackAction( label="^N225" ,data="pic^N225" ,display_text="^N225" ),),
                    QuickReplyItem( action=PostbackAction( label="^KS11" ,data="pic^KS11" ,display_text="^KS11"),)
                ]
            )            
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, 
                                    messages=[TextMessage(text='請選擇-美股指數-交易績效圖',quick_reply=quickReply)])
            )
        elif text == 'etf':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem( action=PostbackAction( label="FNGU"  ,data="picFNGU",display_text="尖牙正3" ),),
                    QuickReplyItem( action=PostbackAction( label="SOXL"  ,data="picSOXL",display_text="費半正3" ),),
                    QuickReplyItem( action=PostbackAction( label="XBI"   ,data="picXBI" ,display_text="生技指" ),),
                    QuickReplyItem( action=PostbackAction( label="XLE"   ,data="picXLE" ,display_text="能源指" ),),
                    QuickReplyItem( action=PostbackAction( label="XLF"   ,data="picXLF" ,display_text="金融指" ),),
                    QuickReplyItem( action=PostbackAction( label="XME"   ,data="picXME" ,display_text="金礦指" ),),
                    QuickReplyItem( action=PostbackAction( label="XLV"   ,data="picXLV" ,display_text="醫保指" ),),
                    QuickReplyItem( action=PostbackAction( label="XLP"   ,data="picXLP" ,display_text="消費指" ),),
                    QuickReplyItem( action=PostbackAction( label="IYR"   ,data="picIYR" ,display_text="地產指" ),),
                    QuickReplyItem( action=PostbackAction( label="XLU"   ,data="picXLU" ,display_text="公用指" ),),
                    QuickReplyItem( action=PostbackAction( label="XLI"   ,data="picXLI" ,display_text="工業指" ),)
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, 
                                    messages=[TextMessage(text='請選擇-美股板塊-交易績效圖',quick_reply=quickReply)])
            )
        elif text == 'fngu':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem( action=PostbackAction( label="TSLA"   ,data="picTSLA"  ,display_text="特斯拉" ),),
                    QuickReplyItem( action=PostbackAction( label="AAPL"   ,data="picAAPL"  ,display_text="蘋果"   ),),
                    QuickReplyItem( action=PostbackAction( label="NVDA"   ,data="picNVDA"  ,display_text="英偉達"),),
                    QuickReplyItem( action=PostbackAction( label="MSFT"   ,data="picMSFT"  ,display_text="微軟"  ),),
                    QuickReplyItem( action=PostbackAction( label="AMZN"   ,data="picAMZN"  ,display_text="亞馬遜" ),),
                    QuickReplyItem( action=PostbackAction( label="NFLX"   ,data="picNFLX"  ,display_text="奈飛"  ),),
                    QuickReplyItem( action=PostbackAction( label="META"   ,data="picMETA"  ,display_text="臉書"  ),),
                    QuickReplyItem( action=PostbackAction( label="AMD"    ,data="picAMD"   ,display_text="美超微" ),),
                    QuickReplyItem( action=PostbackAction( label="GOOGL"  ,data="picGOOGL" ,display_text="谷哥"  ),),
                    QuickReplyItem( action=PostbackAction( label="INTC"   ,data="picINTC"  ,display_text="英特爾" ),),
                    QuickReplyItem( action=PostbackAction( label="MU"     ,data="picMU"    ,display_text="美光"  ),),
                    QuickReplyItem( action=PostbackAction( label="TSM"    ,data="picTSM"   ,display_text="台積電ADR"),)
                ]
            ) 
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, 
                                    messages=[TextMessage(text='請選擇-尖牙股-交易績效圖',quick_reply=quickReply)])
            )
        elif text == '台指':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem( action=PostbackAction( label="元大台灣50"     ,data= "pic0050TW"     ,display_text="0050.TW"    ),),
                    QuickReplyItem( action=PostbackAction( label="元大台灣50正2"  ,data=  "pic00631LTW"  ,display_text="00631L.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="富邦台50"       ,data= "pic006208TW"  ,display_text="006208.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="富邦日本"       ,data= "pic00645TW"    ,display_text="00645.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="期元大S&P石油"   ,data=  "pic00642UTW" ,display_text="00642U.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="期元大美元指數"  ,data= "pic00682UTW"   ,display_text="00682U.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="元大美債20反1"   ,data=  "pic00681RTW" ,display_text="00681R.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="國泰20年美債正2" ,data= "pic00688LTW"   ,display_text="00688L.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="期元大道瓊白銀"   ,data= "pic00738UTW"  ,display_text="00738U.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="期街口S&P黃豆"   ,data=  "pic00693UTW"  ,display_text="00693U.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="期街口道瓊銅"    ,data=  "pic00763UTW"  ,display_text="00763U.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="期元大S&P日圓反1",data= "pic00707RTW"   ,display_text="00707R.TW" ),)
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, 
                                    messages=[TextMessage(text='請選擇-台指-交易績效圖',quick_reply=quickReply)])
            )
        elif text == '台股科':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem( action=PostbackAction( label="台積電"    ,data="pic2330TW"  ,display_text="2330.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="聯發科"    ,data="pic2454TW"  ,display_text="2454.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="聯電"      ,data="pic2303TW"  ,display_text="2303.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="日月光"    ,data="pic3711TW"  ,display_text="3711.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="華碩"      ,data="pic2357TW"  ,display_text="2357.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="廣達"      ,data="pic2382TW"  ,display_text="2382.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="台達電"    ,data="pic2308TW"  ,display_text="2308.TW" ),),
                    QuickReplyItem( action=PostbackAction( label="鴻海"      ,data="pic2317TW"  ,display_text="2317.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="國泰費半"  ,data="pic00830TW" ,display_text="00830.TW"),),
                    QuickReplyItem( action=PostbackAction( label="元全球AI"  ,data="pic00762TW" ,display_text="00762.TW" ),)
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, 
                                    messages=[TextMessage(text='請選擇-台科技股-交易績效圖',quick_reply=quickReply)])
            )
        elif text == '台股傳':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem( action=PostbackAction( label="富邦金"    ,data="pic2881TW"  ,display_text="2881.TW"   ),),
                    QuickReplyItem( action=PostbackAction( label="國泰金"    ,data="pic2882TW"  ,display_text="2882.TW"   ),),
                    QuickReplyItem( action=PostbackAction( label="玉山金"    ,data="pic2884TW"  ,display_text="2884.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="元大金"    ,data="pic2885TW"  ,display_text="2885.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="中信金"    ,data="pic2891TW"  ,display_text="2891.TW"   ),),
                    QuickReplyItem( action=PostbackAction( label="長榮"      ,data="pic2603TW"  ,display_text="2603.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="台塑化"    ,data="pic6505TW"  ,display_text="6505.TW"  ),),
                    QuickReplyItem( action=PostbackAction( label="統一"      ,data="pic1216TW"  ,display_text="1216.TW"   ),)
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, 
                                    messages=[TextMessage(text='請選擇-台傳統股-交易績效圖',quick_reply=quickReply)])
            )
        else:
            quickReply = QuickReply(
                items=[
                    QuickReplyItem(action=PostbackAction(label="美股信號",  data="SignUS",  display_text="美股信號"),),
                    QuickReplyItem(action=PostbackAction(label="台股信號",  data="SignTW",  display_text="台股信號"),),
                    QuickReplyItem(action=PostbackAction(label="美股評估",  data="EvaluUS", display_text="今日美股評估"),),
                    QuickReplyItem(action=PostbackAction(label="台股評估",  data="EvaluTW", display_text="今日台股評估"),),
                    QuickReplyItem(action=PostbackAction(label="月美股績效",data="ProfitUS",display_text="月美股績效排序"),),
                    QuickReplyItem(action=PostbackAction(label="月台股績效",data="ProfitTW",display_text="月台股績效排序"),)
                ]
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='你好！ 請選擇今日分析項目\n 輸入關鍵字 us,fngu,etf\n或 台股傳,台股科,台指\n 可下載交易紀錄與績效圖',
                        quick_reply=quickReply)]
                )
            )

@Line_handler.add(PostbackEvent)
def handle_postback(event):
    xToday = datetime.now()
    Bef1Date = xToday - timedelta(days=1)
    sToday = xToday.strftime("%Y-%m-%d")
    StrDate = Bef1Date.strftime("%Y-%m-%d")   
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        postback_data = event.postback.data
        if postback_data == 'SignUS':
            xmsg = Bll.NotifySign('2',StrDate,'US')
        elif postback_data == 'SignTW':
            xmsg = Bll.NotifySign('1',StrDate,'TW')
        elif postback_data == 'EvaluUS':
            xmsg = Bll.GetEvaluate_US('2',StrDate)
        elif postback_data == 'EvaluTW':
            xmsg = Bll.GetEvaluate_TW('1',StrDate)
        elif postback_data == 'ProfitUS':
            xmsg = Bll.GetProfit('US')
        elif postback_data == 'ProfitTW':
            xmsg = Bll.GetProfit('TW')
        elif postback_data[:3] == 'pic':
            xStack = postback_data[3:]
            if  os.path.isfile(xStack+'.jpg'):
                url = request.url_root +xStack+'.jpg' #'chart/logo.jpg'
                url = url.replace("http", "https")
                app.logger.info("url=" + url)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            ImageMessage(original_content_url=url, preview_image_url=url)
                        ]
                    )
                )
            else:
                xmsg = ''
        else:
            xmsg = ''

        if xmsg =='':
            xmsg = '查無本日資料，請繼續'
        line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,messages=[TextMessage(text=xmsg)]
                )
        )            

if __name__ == "__main__":
    app.run()