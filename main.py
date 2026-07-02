import time
import requests
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

# ضع مفتاح الـ API الخاص بك هنا
FINNHUB_API_KEY = "YOUR_API_KEY_HERE"
watchlist = {}

def get_dynamic_stocks():
    try:
        url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # تحقق من أن البيانات قائمة (List) قبل معالجتها لتجنب خطأ الـ slice
        if isinstance(data, list) and len(data) > 0:
            # نأخذ أول 20 سهم ونستخرج الرمز (symbol) منها
            return [stock.get('symbol') for stock in data[:20] if stock.get('symbol')]
        else:
            print("تحذير: البيانات المستلمة غير صالحة أو فارغة، جارِ استخدام القائمة الاحتياطية")
            return ["AAPL", "TSLA", "AMD", "PLTR", "SOFI"]
            
    except Exception as e:
        print(f"خطأ في جلب الأسهم من Finnhub: {e}")
        # قائمة احتياطية لضمان عدم توقف السكربت
        return ["AAPL", "TSLA", "AMD", "PLTR", "SOFI"]

def main():
    print("بدء عملية المسح الشامل...")
    symbols = get_dynamic_stocks()
    
    for symbol in symbols:
        strength, money_flow, targets = calculate_flow(symbol)
        
        if strength >= 8:
            # تحديث عداد التجميع للسهم
            watchlist[symbol] = watchlist.get(symbol, 0) + 1
            
            # إذا استمر التجميع لـ 3 دورات متتالية (15 دقيقة)
            if watchlist[symbol] == 3:
                send_telegram_alert(symbol, strength, "تجميع مؤسسي قوي ومستمر", targets)
        else:
            # إذا توقف التجميع، نصفر العداد
            watchlist[symbol] = 0
            
    print("...جولة المسح اكتملت. انتظار 5 دقائق...")

while True:
    main()
    time.sleep(300) # انتظار 5 دقائق بين كل دورة
