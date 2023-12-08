import asyncio
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'm/5ssSjjhD4saSEgKyIioep/OoJGzisdGHta3qxl2OhhJdvnmC+fnV4MCaJjavCB2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf5/H3XmMrZvSNwbYAB9SCJpHExP5tuhn5RpJDqsut4+imgdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

async def push_message_async(user_id, text):
    try:
        await line_bot_api.push_message(user_id, TextSendMessage(text=text))
    except LineBotApiError as e:
        print(f"Error pushing message to AI小幫手: {e}")

@app.route("/callback", methods=['POST'])
async def callback():
    signature = request.headers['X-Line-Signature']
    body = await request.get_data(as_text=True)

    try:
        await handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    user_message = event.message.text

    if event.source.user_id == '@007omugu':
        # 轉發使用者的訊息給 "AI小幫手"
        asyncio.create_task(push_message_async('@AI小幫手的LINE ID', user_message))

        # 顯示 "AI小幫手" 回傳的訊息
        reply_message = f"你對 AI小幫手 說了：{user_message}"
        await line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

if __name__ == "__main__":
    app.run(port=5000)

