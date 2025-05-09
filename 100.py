from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import time  # 引入 time 模組

CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'Ei9G4MF8Nl0DsiAqWJqNtPAVsjfMi6ljbFB+O9DcoxR505eQqiAcX/e+dl8kc0eV2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf589RA/9Gw7LbB/DuQhQaeI8Zg6f4EGlz57XHmxiPNuiRwdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # 只回覆 "您好"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="您好")
    )

    reply_message = f"你對 AI小幫手 說了：{user_message}"
    print(f"User ID: {user_id}, Message: {reply_message}")

if __name__ == "__main__":
    app.run(port=5000)




