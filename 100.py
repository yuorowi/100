from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.exceptions import LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai


CHANNEL_SECRET = 'bd1f67e47488ef7d287541cfb175e6ec'
CHANNEL_ACCESS_TOKEN = 'm/5ssSjjhD4saSEgKyIioep/OoJGzisdGHta3qxl2OhhJdvnmC+fnV4MCaJjavCB2BZBoRK6UYoAY8Y2D1L2iVizgzRwU3Q2QblOcdFlf5/H3XmMrZvSNwbYAB9SCJpHExP5tuhn5RpJDqsut4+imgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

engine = "davinci"


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
    user_id = event.source.user_id
    message_text = event.message.text

    try:
        gpt_response = openai.Completion.create(
            engine=engine,
            prompt=message_text,
            max_tokens=50
        )
        gpt_answer = gpt_response.choices[0].text.strip()

        final_answer = f"answer: {gpt_answer}"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=final_answer)
        )
    except openai.error.RateLimitError:
        
        error_message = "Sorry, I'm currently overloaded. Please try again later."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=error_message)
        )
    except LineBotApiError as e:
      
        error_message = f"Line Bot API error: {e.error.message}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=error_message)
        )



if __name__ == "__main__":
    app.run(debug=True)
