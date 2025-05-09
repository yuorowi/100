from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging

# 用你自己的 Channel Token 和 Secret
CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'Ei9G4MF8Nl0DsiAqWJqNtPAVsjfMi6ljbFB+O9DcoxR505eQqiAcX/e+dl8kc0eV2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf589RA/9Gw7LbB/DuQhQaeI8Zg6f4EGlz57XHmxiPNuiRwdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

# 設定日誌紀錄
logging.basicConfig(level=logging.DEBUG)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    # 輸出收到的請求資料到日誌
    app.logger.debug('Request Body: %s', body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 輸出收到的訊息內容到日誌
    app.logger.debug('Received message: %s', event.message.text)
    
    # 回復訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Hi")
    )

if __name__ == "__main__":
    app.run(port=5000)





