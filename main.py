import os
import time
import requests
from bs4 import BeautifulSoup
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

# --- إعدادات البوت المباشرة (تم دمج التوكين هنا لضمان العمل) ---
BOT_TOKEN = "8710391806:AAF7y3qVI2qwZjMkMTcIkeL73tLFdaK2GE"
CHAT_ID = "8710391806"

# دالة اختبار للتحقق من الاتصال
def verify_connection():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": "✅ تم الربط بنجاح! البوت يعمل الآن."}
        response = requests.get(url, params=params)
        print(f"Connection Test Status: {response.status_code}")
    except Exception as e:
        print(f"Error in connection test: {e}")

# استدعاء الاختبار مرة واحدة
verify_connection()

watchlist = {}

def get_stocks_from_finviz():
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        symbols = [a.text for a in soup.find_all('a', class_='screener-link-primary')]
        return symbols[:10]
    except Exception as e:
        print(f"خطأ في جلب البيانات: {e}")
        return []

def main():
    print("بدء المسح...")
    symbols = get_stocks_from_finviz()
    for symbol in symbols:
        try:
            strength, money_flow, targets = calculate_flow(symbol)
            # تم ضبط الشرط على 0 مؤقتاً للتأكد من وصول التنبيهات
            if strength >= 0:
                send_telegram_alert(symbol, strength, "اختبار النظام", targets)
        except Exception as e:
            print(f"خطأ في معالجة {symbol}: {e}")
    print("اكتملت الجولة.")

while True:
    main()
    time.sleep(300)
