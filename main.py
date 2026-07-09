send_telegram_alert("TEST", 0, "✅ تم تشغيل السكنر وبدأ المسح بنجاح!")
import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
sent_alerts = {}

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def main():
    # هذه الجملة ستظهر فوراً في الـ Logs وتؤكد لنا أن الكود يقرأ من هذا الملف
    print(">>> SYSTEM STATUS: Config loaded successfully from file!")
    
    # رسالة التأكيد
    send_telegram_alert("SYSTEM", 0, "🚀 تم تشغيل السكنر وبدأ المسح بنجاح!")
    
    while True:
        # كود المسح كما هو...
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
