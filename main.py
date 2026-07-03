import os
import time
import requests
from bs4 import BeautifulSoup

from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SCAN_INTERVAL_SECONDS

# --- إعدادات البوت (تُقرأ من Environment Variables عبر config.py) ---
BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TELEGRAM_CHAT_ID


def verify_connection():
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ BOT_TOKEN أو CHAT_ID غير موجودين في Environment Variables على Render.")
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": "✅ تم الربط بنجاح! البوت الآن جاهز لاستقبال تنبيهات الأسهم."}
        response = requests.get(url, params=params)
        print(f"Connection Test Status: {response.status_code}")
    except Exception as e:
        print(f"Error in connection test: {e}")


# اختبار الربط عند التشغيل
verify_connection()


def get_stocks_from_finviz():
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        symbols = [a.text for a in soup.find_all('a', class_='screener-link-primary')]
        return symbols[:10]
    except Exception as e:
        print(f"خطأ في Finviz: {e}")
        return []


def main():
    print("بدء المسح...")
    symbols = get_stocks_from_finviz()
    for symbol in symbols:
        try:
            strength, money_flow, targets = calculate_flow(symbol)
            # ⚠️ الشرط 0 مؤقتاً للتأكد من وصول الرسائل - غيّره لعتبة حقيقية قبل الإنتاج
            if strength >= 0:
                send_telegram_alert(symbol, strength, "تنبيه اختبار", targets)
        except Exception as e:
            print(f"خطأ في معالجة {symbol}: {e}")
    print("اكتملت الجولة.")


while True:
    main()
    time.sleep(SCAN_INTERVAL_SECONDS)
