import time
import requests
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

# ضع مفتاح الـ API الخاص بك هنا
FINNHUB_API_KEY = "YOUR_API_KEY_HERE"
watchlist = {}

def get_dynamic_stocks():
    try:
        # جلب قائمة الأسهم النشطة من Finnhub
        url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # نأخذ أول 20 سهم فقط كعينة للبدء (لتجنب ضغط السيرفر)
        # يمكنك تعديل هذا النطاق لاحقاً
        return [stock['symbol'] for stock in data[:20]]
    except Exception as e:
        print(f"خطأ في جلب الأسهم: {e}")
        return ["AAPL", "TSLA", "AMD", "PLTR", "SOFI"] # قائمة احتياطية

def main():
    print("بدء عملية المسح الشامل...")
    symbols = get_dynamic_stocks()
    
    for symbol in symbols:
        strength, money_flow, targets = calculate_flow(symbol)
        
        if strength >= 8:
            watchlist[symbol] = watchlist.get(symbol, 0) + 1
            # إذا استمر التجميع لـ 3 دورات متتالية (15 دقيقة)
            if watchlist[symbol] == 3:
                send_telegram_alert(symbol, strength, "تجميع مؤسسي قوي ومستمر", targets)
        else:
            watchlist[symbol] = 0
            
    print("...جولة المسح اكتملت. انتظار 5 دقائق...")

while True:
    main()
    time.sleep(300)
