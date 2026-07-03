import requests
import os

def send_telegram_alert(symbol, strength, message, targets):

    TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

    if not TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN أو CHAT_ID غير موجودين")
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    targets_text = "\n".join([f"🎯 {t}" for t in targets]) if targets else "لا توجد أهداف"

    text = f"""
🚀 Pump Penny Scanner

📈 السهم: {symbol}

⭐ قوة الإشارة: {strength}/100

💰 التدفق المالي:
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
