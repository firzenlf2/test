# main.py

from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ LINE API credentials
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# ✅ OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Health check endpoint
@app.get("/")
def read_root():
    return {"status": "running"}

# ✅ Webhook for LINE
@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers.get('X-Line-Signature')

    try:
        handler.handle(body.decode('utf-8'), signature)
    except Exception as e:
        print(f"LINE Webhook Error: {e}")
        return "Error", 400

    return "OK", 200

# ✅ Handle LINE Message Event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    try:
        # Call ChatGPT (gpt-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )

        reply_text = response['choices'][0]['message']['content'].strip()

    except Exception as e:
        reply_text = f"ขออภัยค่ะ เกิดข้อผิดพลาด: {e}"

    # ✅ Reply to LINE user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
