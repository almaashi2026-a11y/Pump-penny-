import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

# تهيئة الاتصال بخادم Moomoo
quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
sent_alerts = {}

# إعداد الـ Logs لمراقبة العمل على Render
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def main():
    logging.info("Scanner Started: System initializing...")
    
    # رسالة فورية للتأكد من أن السكربت بدأ العمل ووصل للتوكن
    send_telegram_alert("SYSTEM", 0, "🚀 تم تشغيل السكنر بنجاح وبدأ المسح الآن!")
    
    while True:
        # جلب بيانات السوق
        ret, data = quote_ctx.get_market_snapshot(['US'])
        
        if ret == RET_OK:
            for _, row in data.iterrows():
                symbol = row['code']
                price = row['last_price']
                vol = row['volume']
                avg_vol = row.get('prev_close_volume', 100000)
                vwap = row.get('vwap', price)

                # الفلاتر الذكية لاكتشاف الصفقات المؤسسية
                if 0.20 <= price <= 10.0:
                    # شرط: حجم تداول (5x) + اتجاه صاعد (فوق الـ VWAP)
                    if vol > (avg_vol * 5) and price > vwap:
                        
                        current_time = time.time()
                        # التهدئة (Cooldown) لمنع إغراق تليجرام بالتنبيهات
                        if symbol not in sent_alerts or (current_time - sent_alerts[symbol] > config.ALERT_COOLDOWN_MINUTES * 60):
                            
                            msg = (f"🚀 **فرصة Block Buy مؤكدة**\n"
                                   f"📈 السهم: {symbol}\n"
                                   f"💰 السعر: {price}\n"
                                   f"📊 السيولة: {vol:,}\n"
                                   f"✅ الحالة: صعود فوق VWAP")
                            
                            send_telegram_alert(symbol, price, msg)
                            sent_alerts[symbol] = current_time
                            logging.info(f"Alert Sent: {symbol}")
        
        # الانتظار قبل المسح التالي
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
