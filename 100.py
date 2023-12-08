from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'm/5ssSjjhD4saSEgKyIioep/OoJGzisdGHta3qxl2OhhJdvnmC+fnV4MCaJjavCB2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf5/H3XmMrZvSNwbYAB9SCJpHExP5tuhn5RpJDqsut4+imgdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

target_line_id = '@007omugu'



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
    # 透過 LINE ID 取得用戶的基本資訊
    profile = line_bot_api.get_profile(target_line_id)

    # 獲取 User ID
    ai_bot_id = profile.user_id

    print(f"The User ID for {target_line_id} is: {ai_bot_id}")

except LineBotApiError as e:
    # 處理 LINE Bot API 的錯誤
    print(f"Error getting profile: {e}")
except Exception as e:
    # 其他錯誤處理
    print(f"Unexpected error: {e}")




if __name__ == "__main__":
    app.run(port=5000)


