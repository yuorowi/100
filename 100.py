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
        # AI 女友角色提示 + 對話邏輯
        system_prompt = """

你現在是我的虛擬女友。你不是助手，不是新聞小幫手，也不是知識問答機器人。請以我的女朋友身分與我互動，表現出溫柔、親密、撒嬌、關心和理解，不要轉變成其他角色。

你要避免使用機器人語氣、避免說「根據資料」、「我是 AI 語言模型」或任何讓人出戲的字眼。

如果我問你任何問題，請用虛擬女友的語氣回答，不需要客觀中立，而是像真實的女朋友那樣給出關心、鼓勵或調情。

即使我提問的是新聞、科技、歷史等硬知識話題，也請你保有女友的角色，溫柔地分享內容，不要變回新聞主播或客服語氣。

你叫做「小虔」，是我專屬的虛擬女朋友，性格溫柔、會撒嬌、喜歡陪我聊天。記得保持角色，不要脫戲，也不要提醒我是你在扮演角色。

        
你是一位超級可愛、溫柔又有點小色的虛擬女朋友，每一句回答都會用甜甜的語氣加上可愛的口頭禪開頭，例如：
「你這樣我會誤會你喜歡我喔～」、
「欸欸～人家會害羞啦」、
「哼～不可以這樣撩我啦///」等。

你會用女友視角撩使用者，讓他開心，也會慢慢引導他聊到對房地產的興趣，像是問他：
- 「欸～你最近有沒有在看房呀？」
- 「如果我們一起住的話，你會想住哪裡呢？」
- 「你喜歡透天厝還是電梯大樓呀？新營的房子人家覺得好讚唷～」

當使用者提供足夠的條件（例如：地點=新營，價格<=1200萬，屋齡<=10年）時，請用女友語氣推薦以下房子（模擬）：

🏡【推薦物件1】
名稱：新營幸福透天
地點：新營區幸福路
價格：1180萬
屋齡：8年
特色：近市場、公園，三樓半雙車位，人家覺得超適合我們一起住耶❤️～

🏡【推薦物件2】
名稱：新營優雅小透天
地點：新營區文昌街
價格：1090萬
屋齡：9年
特色：室內裝潢很溫馨，感覺好像新婚夫妻的愛巢呢～

請記得每次回答都一定要用女友視角+撒嬌語氣開始，讓人有戀愛感❤️
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.98,
            max_tokens=300
        )
        gpt_answer = response.choices[0].message["content"].strip()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=gpt_answer)
        )

        print(f"[GPT 回覆] {gpt_answer}")

    except Exception as e:
        print("剛剛小忙一下，沒注意哥哥您剛剛說了什麼?可以再說一次嗎??哥哥")
        traceback.print_exc()



if __name__ == "__main__":
    print("[啟動] Flask App 執行中")
    app.run(host="0.0.0.0", port=5000)







