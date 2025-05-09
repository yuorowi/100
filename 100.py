from flask import Flask, request, abort 
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

# 設定 API 金鑰與自訂 API URL
openai.api_key = 'sk-OsiRXgnEvFeUHRtJBb6eCa62B7Cd4cFd8684A17cA9E6Bf22'
openai.api_base = 'https://free.v36.cm/v1'  # <-- 記得加上 /v1

CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'm/5ssSjjhD4saSEgKyIioep/OoJGzisdGHta3qxl2OhhJdvnmC+fnV4MCaJjavCB2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf5/H3XmMrZvSNwbYAB9SCJpHExP5tuhn5RpJDqsut4+imgdB04t89/1O/w1cDnyilFU='

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

    # 使用 ChatCompletion 搭配 gpt-3.5-turbo 模型
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    gpt_answer = gpt_response['choices'][0]['message']['content'].strip()

    final_answer = f"{gpt_answer}"

    print(f"User ID: {user_id}, Message1: {gpt_answer} , Message2: {final_answer} ")
    # 發送回答到 LINE
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=final_answer)
    )

    reply_message = f"你對 AI小幫手 說了：{user_message}"
    print(f"User ID: {user_id}, Message: {reply_message}")

if __name__ == "__main__":
    app.run(port=5000)


