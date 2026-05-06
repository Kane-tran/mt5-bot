from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/signal")
async def signal(req: Request):
    data = await req.json()
    msg = f"🤖 MT5 Signal\n{data}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    return {"status": "sent"}