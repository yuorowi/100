from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage



CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'm/5ssSjjhD4saSEgKyIioep/OoJGzisdGHta3qxl2OhhJdvnmC+fnV4MCaJjavCB2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf5/H3XmMrZvSNwbYAB9SCJpHExP5tuhn5RpJDqsut4+imgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

whitelisted_ids = ['@007omugu']


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
    
    if event.source.user_id == '@007omugu':

        if event.source.user_id in whitelisted_ids:
          
            try:
                ai_bot_id = '@007omugu'
                line_bot_api.push_message(ai_bot_id, TextSendMessage(text=user_message))
            except LineBotApiError as e:
                print(f"Error pushing message to AI小幫手: {e}")

      
            reply_message = f"你對 AI小幫手 說了：{user_message}"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_message)
            )
        else:
            print(f"User {event.source.user_id} is not whitelisted.")
    
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="很抱歉，您不在白名單中，請先加為好友。")
            )

if __name__ == "__main__":
    app.run(port=5000)
