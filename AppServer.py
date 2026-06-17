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
import GetSqlMsg as Bll
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)

configuration = Configuration(access_token='be0tzYkk3VyLZ+zHNZDy98vfexagRGkGuFIODguqmHzaMLhP81SDXBOxeL2amDG3gdIdMZ3J3SbNhf+BDaLxfAokk3lnUtBGpFbnGI0qVh+rBzCT7wvKj/KNKtAH8OPRVT04Hvo/Sq0sRw4nhWiv+QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7c01a19c758e4d057d452c2c33275f7b')

stk_list = [
 'SPY','QQQ','DIA','IWM','SOXX','UVXY','SVIX','DXY','CL','TMF','SOXL'
,'TSLA' ,'APPLE','NVDA','MSFT','AMZN','NFLX','META','AMD','GOOGL','MU'
,'FNGU','SOXL','XBI','XLE','CL','XLF','XME','XLV','XLP','IYR','XLU','XLI'
]

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 加入好友事件
@handler.add(FollowEvent)
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

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == '美股交易圖':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=PostbackAction(
                            label="SPY",
                            data="SPY",
                            display_text="SPY"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="QQQ",
                            data="QQQ",
                            display_text="QQQ"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="DIA",
                            data="DIA",
                            display_text="DIA"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="SOXX",
                            data="SOXX",
                            display_text="SOXX"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="IWM",
                            data="IWM",
                            display_text="IWM"
                        ),
                    )
                ]
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='你好！ 請選擇交易項目圖表',
                        quick_reply=quickReply
                    )]
                )
            )
        elif text == '台股交易圖':
            quickReply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=PostbackAction(
                            label="0050",
                            data="0050",
                            display_text="0050"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="IWM",
                            data="IWM",
                            display_text="IWM"
                        ),
                    )
                ]
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='你好！ 請選擇交易項目圖表',
                        quick_reply=quickReply
                    )]
                )
            )
        else:
            quickReply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=PostbackAction(
                            label="美股信號",
                            data="SignUS",
                            display_text="美股信號"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="台股信號",
                            data="SignTW",
                            display_text="台股信號"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="美股評估",
                            data="EvaluUS",
                            display_text="今日美股評估"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="台股評估",
                            data="EvaluTW",
                            display_text="今日台股評估"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="月美股績效",
                            data="ProfitUS",
                            display_text="月美股績效排序"
                        ),
                    ),
                    QuickReplyItem(
                        action=PostbackAction(
                            label="月台股績效",
                            data="ProfitTW",
                            display_text="月台股績效排序"
                        ),
                    )
                ]
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='你好！ 請選擇今日分析項目',
                        quick_reply=quickReply
                    )]
                )
            )

@handler.add(PostbackEvent)
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
        else:
            xmsg = '?'    

        if xmsg =='?':
            for i in stk_list:
                if postback_data == i:
                    url = request.url_root + 'static/'+postback_data+'.png' #'chart/logo.jpg'
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
            if xmsg =='':
                xmsg = '查無本日資料，請繼續'
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=xmsg)]
                )
            )            

if __name__ == "__main__":
    app.run()