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
 
    action = data.get("action", "")
    symbol = data.get("symbol", "")
    entry  = data.get("entry", 0)
    sl     = data.get("sl", 0)
    tp1    = data.get("tp1", 0)
    tp2    = data.get("tp2", 0)
    lots   = data.get("lots", 0)
 
    if action == "BUY_OPEN":
        msg = (
            f"🟢 BUY {symbol}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 Entry : {entry}\n"
            f"🛑 SL    : {sl}\n"
            f"🎯 TP1   : {tp1}\n"
            f"🎯 TP2   : {tp2}\n"
            f"📦 Lots  : {lots}"
        )
    elif action == "TP1_HIT":
        msg = (
            f"✅ TP1 HIT {symbol}\n"
            f"━━━━━━━━━━━━━━\n"
            f"🎯 TP1   : {tp1}\n"
            f"➡️ SL dời về breakeven: {entry}"
        )
    elif action == "TP2_HIT":
        msg = (
            f"🏆 TP2 HIT {symbol}\n"
            f"━━━━━━━━━━━━━━\n"
            f"🎯 TP2   : {tp2}\n"
            f"💰 Lệnh đã đóng toàn bộ!"
        )
    elif action == "SL_HIT":
        msg = (
            f"🔴 SL HIT {symbol}\n"
            f"━━━━━━━━━━━━━━\n"
            f"🛑 SL    : {sl}\n"
            f"📉 Lệnh đã đóng."
        )
    elif action == "RSI_EXIT":
        msg = (
            f"⚠️ RSI EXIT {symbol}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📊 RSI overbought — đóng lệnh sớm."
        )
    else:
        msg = f"📨 {symbol} | {action}\nEntry: {entry} | SL: {sl} | TP1: {tp1} | TP2: {tp2}"
 
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
 
    return {"status": "sent"}
 