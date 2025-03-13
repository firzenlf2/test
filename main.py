# main.py (ChatGPT LINE Bot)

from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

# FastAPI app
app = FastAPI()

# LINE credentials (for ChatGPTLine)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Health check (Render ping, keep alive)
@app.get("/")
def read_root():
    return {"status": "ChatGPT Bot is running"}

# LINE webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers['X-Line-Signature']
    handler.handle(body.decode('utf-8'), signature)
    return "OK"

# LINE message handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    reply = chatgpt_response(user_text)  # Get ChatGPT response
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# ChatGPT API call
def chatgpt_response(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to gpt-4o if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Sorry, there was an error processing your request."
