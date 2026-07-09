import time
import logging
from moomoo import OpenQuoteContext, RET_OK
# تأكد أن الاستيراد هنا
from telegram_alerts import send_telegram_alert 
import config

quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)

def main():
    print(">>> SYSTEM STATUS: Starting scanner...")
    # الآن الدالة معرفة هنا، سيتم استدعاؤها بشكل صحيح
    send_telegram_alert("SYSTEM", 0, "🚀 تم تشغيل السكنر وبدأ المسح بنجاح!")
    
    while True:
        # كود المسح...
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
