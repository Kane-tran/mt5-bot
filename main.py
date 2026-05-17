from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

TOKEN  = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(msg: str) -> bool:
    """Gửi tin nhắn Telegram, trả về True nếu thành công."""
    if not TOKEN or not CHAT_ID:
        return False
    url  = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False


# Sử dụng api_route để chấp nhận cả GET (khi bạn tự vào web) và HEAD (khi UptimeRobot vào quét)
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "running"}


@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    """Dùng để UptimeRobot check định kỳ mà không bị spam Telegram"""
    return {"status": "ok"}


# Tách riêng một endpoint nếu bạn muốn chủ động kiểm tra xem Bot Telegram có hoạt động không
@app.get("/test-telegram")
def test_telegram():
    """Vào đường dẫn này thủ công để test riêng tính năng gửi Telegram"""
    ok = send_telegram("✅ Kênh thông báo hoạt động tốt!")
    return {"status": "ok" if ok else "telegram_error"}


@app.post("/signal")
async def signal(req: Request):
    try:
        data = await req.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

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
    elif action == "SELL_OPEN":
        msg = (
            f"🔴 SELL {symbol}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📉 Entry : {entry}\n"
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

    ok = send_telegram(msg)

    if ok:
        return {"status": "sent"}
    else:
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Telegram API failed"})
