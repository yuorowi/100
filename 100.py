from flask import Flask, request, abort 
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import traceback
import os

# GPT API Key 設定（openai 0.28.1 寫法）
openai.api_key = 'sk-OsiRXgnEvFeUHRtJBb6eCa62B7Cd4cFd8684A17cA9E6Bf22'
openai.api_base = 'https://free.v36.cm/v1'  # 自訂 API server URL

# LINE 設定
CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'Ei9G4MF8Nl0DsiAqWJqNtPAVsjfMi6ljbFB+O9DcoxR505eQqiAcX/e+dl8kc0eV2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf589RA/9Gw7LbB/DuQhQaeI8Zg6f4EGlz57XHmxiPNuiRwdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print(f"[Webhook 接收到訊息] Body:\n{body}")  # 印出訊息內容以確認

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("[簽章錯誤] Signature 無效")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    print(f"[收到使用者訊息] User ID: {user_id}, 訊息: {user_message}")

    try:
        # 使用舊版 openai 寫法
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        gpt_answer = response.choices[0].message["content"].strip()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=gpt_answer)
        )

        print(f"[GPT 回覆] {gpt_answer}")
    except Exception as e:
        print("[錯誤] 發生例外：")
        traceback.print_exc()

if __name__ == "__main__":
    print("[啟動] Flask App 執行中")
    app.run(host="0.0.0.0", port=5000)







