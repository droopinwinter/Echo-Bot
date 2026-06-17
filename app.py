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
    URIAction
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

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
Line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

DASHBOARD = 'https://vqmt-apka-dashboard.vercel.app'
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
                messages=[TextMessage(text=
                    '你好！我是 VQMT/APKA 交易系統機器人\n'
                    '\n'
                    '📊 每日功能\n'
                    '  • 美股/台股信號 — 今日進出場建議\n'
                    '\n'
                    '📈 績效網站（每週更新）\n'
                    '  • 績效總覽 — 權益曲線/回撤/指標\n'
                    '  • 品種持倉 — APKA/VQMT 分數與持倉\n'
                    '  • 資金運用 — 倉位配置比例\n'
                    '\n'
                    '📘 策略說明\n'
                    '  • APKA / VQMT 介紹與參數查詢\n'
                    '\n'
                    '輸入任意文字可呼叫主選單'
                )]
            )
        )

@Line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        quickReply = QuickReply(
                items=[
                    QuickReplyItem(action=PostbackAction(label="美股信號",  data="SignUS",  display_text="美股信號")),
                    QuickReplyItem(action=PostbackAction(label="台股信號",  data="SignTW",  display_text="台股信號")),
                    QuickReplyItem(action=URIAction(label="績效總覽",      uri=f"{DASHBOARD}/")),
                    QuickReplyItem(action=URIAction(label="品種持倉",      uri=f"{DASHBOARD}/tickers.html")),
                    QuickReplyItem(action=URIAction(label="資金運用",      uri=f"{DASHBOARD}/capital_utilization.html")),
                    QuickReplyItem(action=URIAction(label="參數查詢",      uri=f"{DASHBOARD}/params.html")),
                    QuickReplyItem(action=URIAction(label="APKA說明",      uri=f"{DASHBOARD}/apka-intro.html")),
                    QuickReplyItem(action=URIAction(label="VQMT說明",      uri=f"{DASHBOARD}/vqmt-intro.html")),
                ]
        )
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(
                    text='請選擇功能\n'
                         '• 每日信號：美股/台股信號\n'
                         '• 績效網站：績效總覽/品種持倉/資金運用\n'
                         '• 策略說明：APKA/VQMT說明/參數查詢',
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