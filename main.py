import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

# إعداد الاتصال
quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
sent_alerts = {}

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def main():
    logging.info("Scanner Started: Detecting Block Buys...")
    
    while True:
        # جلب بيانات السوق الحية
        ret, data = quote_ctx.get_market_snapshot(['US'])
        
        if ret == RET_OK:
            for _, row in data.iterrows():
                symbol = row['code']
                price = row['last_price']
                volume = row['volume']
                avg_vol = row.get('prev_close_volume', 10000) # استخدام حجم الإغلاق كمرجع
                
                # 1. فلتر السعر (Penny Stocks)
                if 0.20 <= price <= 10.0:
                    
                    # 2. فلتر Block Buy (الحجم الحالي أكبر من 3 أضعاف المتوسط)
                    is_block_buy = volume > (avg_vol * 3)
                    
                    if is_block_buy:
                        # 3. فلتر التكرار (Cooldown)
                        current_time = time.time()
                        if symbol not in sent_alerts or (current_time - sent_alerts[symbol] > config.ALERT_COOLDOWN_MINUTES * 60):
                            
                            # تنسيق رسالة التنبيه
                            msg = (f"🚨 **Block Buy Detected!**\n"
                                   f"📈 السهم: {symbol}\n"
                                   f"💰 السعر: {price}\n"
                                   f"📊 الحجم: {volume:,}")
                            
                            send_telegram_alert(symbol, price, msg, [])
                            sent_alerts[symbol] = current_time
                            logging.info(f"Alert Sent: {symbol}")
        
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
