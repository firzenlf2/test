import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Allow multiple methods to prevent 405 errors
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root():
    return {"message": "Hello, world!"}

# Webhook route that must return 200 for LINE verification
@app.post("/webhook")
async def webhook():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Automatically use the assigned port
    uvicorn.run(app, host="0.0.0.0", port=port)
