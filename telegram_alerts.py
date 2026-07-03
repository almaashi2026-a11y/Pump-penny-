import requests
import config

def send_telegram_alert(symbol, price, message, targets):

    TOKEN = config.TELEGRAM_BOT_TOKEN
    CHAT_ID = config.TELEGRAM_CHAT_ID

    if not TOKEN or not CHAT_ID:
        print("❌ TELEGRAM_BOT_TOKEN أو TELEGRAM_CHAT_ID غير موجودين")
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    targets_text = "\n".join([f"🎯 {t}" for t in targets]) if targets else ""

    text = f"""
🚀 Momentum Scanner Alert

📈 السهم: {symbol}
💵 السعر: {price}

📊 التفاصيل:
{message}

{targets_text}
"""

    try:
        response = requests.get(
            url,
            params={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=20
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False
