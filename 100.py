from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction

# 用你自己的 Channel Token 和 Secret
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
    # 顯示來自使用者的訊息
    print(f"收到訊息：{event.message.text}")

    # 發送按鈕選單
    buttons_template = ButtonsTemplate(
        title="請選擇",
        text="選擇一個選項",
        actions=[
            MessageAction(label="選項1", text="選項1"),
            MessageAction(label="選項2", text="選項2")
        ]
    )
    template_message = TemplateSendMessage(
        alt_text="這是按鈕選單訊息", template=buttons_template
    )

    # 回覆選單
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_selected_option(event):
    # 顯示用戶選擇的選項
    print(f"用戶選擇的選項：{event.message.text}")

    # 根據選擇的選項回應
    if event.message.text == "選項1":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你選擇了選項1")
        )
    elif event.message.text == "選項2":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你選擇了選項2")
        )

if __name__ == "__main__":
    app.run(port=5000)






