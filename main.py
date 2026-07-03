import os
import time
import requests
from bs4 import BeautifulSoup
from stage3_money_flow_detection import calculate_flow
# سأستخدم دالة الإرسال هنا مباشرة للتأكد
from telegram_alerts import send_telegram_alert

# اختبار الاتصال عند بداية التشغيل
def check_connection():
    token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    print(f"DEBUG: Token is {token[:5]}... and ChatID is {chat_id}") # للتحقق في الـ Logs
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": "✅ البوت بدأ العمل الآن بنجاح!"}
        res = requests.get(url, params=params)
        print(f"DEBUG: Telegram Response: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"DEBUG ERROR: {e}")

check_connection()

watchlist = {}

def get_stocks_from_finviz():
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        symbols = [a.text for a in soup.find_all('a', class_='screener-link-primary')]
        return symbols[:5] # اختصار للسرعة
    except Exception as e:
        print(f"خطأ في Finviz: {e}")
        return []

def main():
    print("بدء المسح...")
    symbols = get_stocks_from_finviz()
    for symbol in symbols:
        try:
            strength, money_flow, targets = calculate_flow(symbol)
            # وضعنا الشرط 0 مؤقتاً للتأكد من وصول الرسالة
            if strength >= 0:
                send_telegram_alert(symbol, strength, "اختبار وصول التنبيه", targets)
        except Exception as e:
            print(f"خطأ في تحليل السهم {symbol}: {e}")
    print("اكتملت الجولة.")

while True:
    main()
    time.sleep(300)
