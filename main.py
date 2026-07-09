import time
import logging
from telegram_alerts import send_telegram_alert
import config
from moomoo import OpenQuoteContext, RET_OK

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def main():
    print(">>> SYSTEM STATUS: Scanner starting...")
    send_telegram_alert("SYSTEM", 0, "🚀 السكنر يعمل الآن ومستعد للمسح!")
    
    # محاولة الاتصال مع ضمان عدم توقف السكربت إذا فشل
    try:
        quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    while True:
        try:
            # إضافة كود المسح هنا
            ret, data = quote_ctx.get_market_snapshot(['US'])
            # ... باقي منطق الفلترة ...
        except Exception as e:
            # هذا الجزء هو الأهم: إذا حدث أي خطأ تقني، سيعيد المحاولة بدلاً من التوقف
            print(f"Loop error: {e}")
        
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
