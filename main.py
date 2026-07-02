import time
import requests
from bs4 import BeautifulSoup
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

watchlist = {}

def get_stocks_from_finviz():
    # الرابط يفلتر الأسهم بسعر (0.20 - 10) والأسهم النشطة
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # استخراج رموز الأسهم من جدول Finviz
        symbols = [a.text for a in soup.find_all('a', class_='screener-link-primary')]
        return symbols[:20] # نأخذ أول 20 سهم نشط
    except Exception as e:
        print(f"خطأ في جلب الأسهم من Finviz: {e}")
        return ["AAPL", "AMD", "NVDA"] # قائمة احتياطية

def main():
    print("بدء المسح الذكي من Finviz...")
    symbols = get_stocks_from_finviz()
    
    for symbol in symbols:
        try:
            strength, money_flow, targets = calculate_flow(symbol)
            if strength >= 8:
                watchlist[symbol] = watchlist.get(symbol, 0) + 1
                if watchlist[symbol] == 3:
                    send_telegram_alert(symbol, strength, "تجميع مؤسسي قوي (Finviz Alert)", targets)
            else:
                watchlist[symbol] = 0
        except Exception:
            continue
            
    print("...اكتملت الجولة. انتظار 5 دقائق...")

while True:
    main()
    time.sleep(300)
