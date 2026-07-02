import requests
import os

def send_telegram_alert(symbol, strength, message, targets):
    # جلب البيانات من إعدادات Render
    TOKEN = os.environ.get('BOT_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    
    if not TOKEN or not CHAT_ID:
        print("خطأ: لم يتم العثور على BOT_TOKEN أو CHAT_ID في إعدادات البيئة")
        return False
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    targets_text = ", ".join(targets) if targets else "لا توجد أهداف"
    
    text = (f"🚨 سهم مرصود: {symbol}\n"
            f"قوة التجميع: {strength}/10\n"
            f"السبب: {message}\n"
            f"الأهداف: {targets_text}")
    
    try:
        params = {'chat_id': CHAT_ID, 'text': text}
        response = requests.get(url, params=params)
        return response.status_code == 200
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")
        return False
