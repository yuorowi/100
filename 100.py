from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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

    try:
        ai_bot_id = '@007omugu'
        
        # 將詢問的訊息轉發給 LINE ID 為 "@007omugu" 的帳號
        line_bot_api.push_message(ai_bot_id, TextSendMessage(text=user_message))
        
        # 取得 LINE ID 為 "@007omugu" 的帳號所回傳的訊息
        messages = line_bot_api.get_message_content(event.message.id)
        print(f"User ID: {user_id}, Message1: {messages}")

    except LineBotApiError as e:
        print(f"Error pushing or replying message: {e}")

    # 顯示 "AI小幫手" 回傳的訊息
    reply_message = f"你對 AI小幫手 說了：{user_message}"
    print(f"User ID: {user_id}, Message: {reply_message}, Message1: {messages}")

    line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=f"你對 AI小幫手 說了：{user_message}"),
             TextSendMessage(text=messages.text)]
        )




if __name__ == "__main__":
    app.run(port=5000)

