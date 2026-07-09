import requests
import config

def send_telegram_alert(symbol, price, message):
    # طباعة كاشفة للأخطاء في الـ Logs
    print(f"DEBUG: محاولة إرسال رسالة. التوكن: {config.TELEGRAM_BOT_TOKEN}, الشات آي دي: {config.TELEGRAM_CHAT_ID}")
    
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("❌ خطأ: التوكن أو الآيدي مفقود في إعدادات Render!")
        return False
        
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, data=payload)
        print(f"DEBUG: رد تليجرام: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending telegram: {e}")
        return False
