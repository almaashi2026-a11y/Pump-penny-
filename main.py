import time
# استيراد الوظائف من الملفات التي أنشأناها
from stage1_finviz_scraper import get_live_movers
from stage3_money_flow_detection import calculate_flow 
from telegram_alerts import send_telegram_alert # <--- هذا السطر كان ناقصاً

def scan_market():
    print("بدء عملية المسح...")
    symbols = get_live_movers() 
    
    for symbol in symbols:
        try:
            # تحليل السهم
            strength, money_flow, targets = calculate_flow(symbol)
            
            # إرسال تنبيه فقط إذا كان السهم قوي جداً
            if strength >= 7: 
                send_telegram_alert(symbol, strength, money_flow, targets)
        except Exception as e:
            print(f"خطأ في تحليل {symbol}: {e}")
            continue # إكمال الفحص حتى لو فشل سهم واحد

    print("جولة المسح اكتملت. انتظار 5 دقائق...")
    time.sleep(300)

if __name__ == "__main__":
    while True:
        scan_market()
