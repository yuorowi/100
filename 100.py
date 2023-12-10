from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai


openai.api_key = 'sess-x0YEGN1vWNJnOoeeWMRYyICVviPOyBu6aPKVVcHh'

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

    gpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=50
    )
    gpt_answer = gpt_response.choices[0].text.strip()

    final_answer = f"{gpt_answer}"

    print(f"User ID: {user_id}, Message1: {gpt_answer}")
    # 發送回答到 LINE
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=final_answer)
    )

   
    reply_message = f"你對 AI小幫手 說了：{user_message}"
    print(f"User ID: {user_id}, Message: {reply_message}")




if __name__ == "__main__":
    app.run(port=5000)

