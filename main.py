import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

# إعداد الاتصال
quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)

def main():
    # رسالة تأكيد للعمل
    send_telegram_alert("SYSTEM", 0, "🚀 تم تشغيل السكنر بنجاح وبدأ المسح...", [])
    logging.info("Scanner Started Successfully!")
    
    while True:
        # هنا سيستمر السكربت في مراقبة السوق
        time.sleep(60) 

if __name__ == "__main__":
    main()
