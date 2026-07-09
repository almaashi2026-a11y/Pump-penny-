import time
import logging
# الاستيرادات في الأعلى لضمان تعريف الدوال
from telegram_alerts import send_telegram_alert
import config
from moomoo import OpenQuoteContext, RET_OK

# إعداد اللوجر
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)

def main():
    print(">>> SYSTEM STATUS: Scanner is starting...")
    
    # الاستدعاء الآن داخل الدالة ولن يسبب خطأ
    send_telegram_alert("SYSTEM", 0, "🚀 تم تشغيل السكنر بنجاح وبدأ المسح!")
    
    while True:
        # هنا يوضع منطق المسح الخاص بك
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
