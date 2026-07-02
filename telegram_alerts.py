import requests
import config


def send_telegram_alert(signal: dict) -> bool:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[send_telegram_alert] مفاتيح تيليجرام غير مضبوطة بمتغيرات البيئة")
        return False

    message = (
        f"🚀 *إشارة دخول جديدة*\n\n"
        f"الرمز: `{signal['symbol']}`\n"
        f"السعر: ${signal['price']:.4f}\n"
        f"RVOL: {signal['rvol']}x\n"
        f"التغيّر (15د): {signal['price_change_pct']}%\n"
        f"تدفق مالي كبير: ✅ مؤكد\n\n"
        f"_EMA9 > VWAP | RVOL > {config.RVOL_THRESHOLD}x | "
        f"تدفق ≥ {config.MONEY_FLOW_MULTIPLIER}x_"
    )

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[send_telegram_alert] تم إرسال تنبيه {signal['symbol']}")
        return True
    except Exception as e:
        print(f"[send_telegram_alert] خطأ بإرسال التنبيه: {e}")
        return False
