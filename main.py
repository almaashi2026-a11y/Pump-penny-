import os
import time
import requests
from bs4 import BeautifulSoup
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

# --- دالة اختبار إضافية لضمان وصول الرسالة فور التشغيل ---
def send_startup_test():
    try:
        token = os.environ.get('BOT_TOKEN')
        chat_id = os.environ.get('CHAT_ID')
        if token and chat_id:
            requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=🚀 الصياد يعمل الآن ومستعد للمسح!")
    except Exception as e:
        print(f"خطأ في رسالة الاختبار: {e}")

# تنفيذ رسالة الاختبار عند تشغيل السكربت لأول مرة
send_startup_test()

watchlist = {}

def get_stocks_from_finviz():
    # الرابط يفلتر الأسهم بسعر (0.20 - 10) والأسهم النشطة
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        symbols = [a.text for a in soup.find_all('a', class_='screener-link-primary')]
        return symbols[:20] 
    except Exception as e:
        print(f"خطأ في جلب الأسهم من Finviz: {e}")
        return []

def main():
    print("بدء المسح الذكي من Finviz...")
    symbols = get_stocks_from_finviz()
    
    for symbol in symbols:
        try:
            strength, money_flow, targets = calculate_flow(symbol)
            
            if strength >= 0:
                watchlist[symbol] = watchlist.get(symbol, 0) + 1
                if watchlist[symbol] == 3:
                    send_telegram_alert(symbol, strength, "تجميع مؤسسي قوي (Finviz Alert)", targets)
            else:
                watchlist[symbol] = 0
        except Exception as e:
            print(f"خطأ في معالجة السهم {symbol}: {e}")
            continue
            
    print("...اكتملت الجولة. انتظار 5 دقائق...")

while True:
    main()
    time.sleep(300)
