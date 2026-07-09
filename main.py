import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
sent_alerts = {}

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def main():
    print("DEBUG: السكربت يعمل الآن من النسخة المحدثة!")
    logging.info("Scanner Started...")
    
    # إرسال رسالة تجريبية عند التشغيل
    send_telegram_alert("SYSTEM", 0, "🚀 تم تشغيل السكنر وبدأ المسح...")
    
    while True:
        ret, data = quote_ctx.get_market_snapshot(['US'])
        if ret == RET_OK:
            for _, row in data.iterrows():
                symbol = row['code']
                price = row['last_price']
                vol = row['volume']
                avg_vol = row.get('prev_close_volume', 100000)
                vwap = row.get('vwap', price)

                if 0.20 <= price <= 10.0:
                    if vol > (avg_vol * 5) and price > vwap:
                        current_time = time.time()
                        if symbol not in sent_alerts or (current_time - sent_alerts[symbol] > config.ALERT_COOLDOWN_MINUTES * 60):
                            msg = f"🚀 **فرصة Block Buy:** {symbol}\n💰 السعر: {price}\n📊 السيولة: {vol:,}"
                            send_telegram_alert(symbol, price, msg)
                            sent_alerts[symbol] = current_time
        time.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
