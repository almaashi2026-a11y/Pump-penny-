# main.py
import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

# إعداد الاتصال بـ Moomoo
quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
sent_alerts = {} 

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def main():
    logging.info("Scanner Started via Moomoo API...")
    
    while True:
        # جلب البيانات الحية للسوق الأمريكي
        ret, data = quote_ctx.get_market_snapshot(['US'])
        
        if ret == RET_OK:
            for _, row in data.iterrows():
                symbol = row['code']
                price = row['last_price']
                volume = row['volume']
                
                # فلتر: النطاق السعري المطلوب
                if 0.20 <= price <= 10.0:
                    
                    # فلتر: Block Buy (حجم يتجاوز 3 أضعاف متوسط الحجم)
                    # ملاحظة: إذا كان avg_vol غير متاح في العمود، يمكنك وضع رقم ثابت كحد أدنى
                    if volume > (row.get('prev_close_volume', volume/2) * 3):
                        
                        # فلتر: Cooldown لمنع تكرار التنبيهات
                        current_time = time.time()
                        if symbol not in sent_alerts or (current_time - sent_alerts[symbol] > config.ALERT_COOLDOWN_MINUTES * 60):
                            
                            msg = f"🚀 {symbol} | السعر: {price} | الحجم: {volume}"
                            send_telegram_alert(symbol, price, msg, [])
                            sent_alerts[symbol] = current_time
                            logging.info(f"Alert sent for: {symbol}")
        
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
