from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'Ei9G4MF8Nl0DsiAqWJqNtPAVsjfMi6ljbFB+O9DcoxR505eQqiAcX/e+dl8kc0eV2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf589RA/9Gw7LbB/DuQhQaeI8Zg6f4EGlz57XHmxiPNuiRwdB04t89/1O/w1cDnyilFU='


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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
    # 僅回覆「您好」
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="您好")
    )

if __name__ == "__main__":
    app.run(port=5000)





