import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert
import config

quote_ctx = OpenQuoteContext(host=config.MOOMOO_IP, port=config.MOOMOO_PORT)
sent_alerts = {}

def main():
    while True:
        ret, data = quote_ctx.get_market_snapshot(['US'])
        if ret == RET_OK:
            for _, row in data.iterrows():
                symbol = row['code']
                price = row['last_price']
                volume = row['volume']
                
                # المعايير الذهبية للأفضلية:
                # 1. السعر بين 0.20 و 10 دولار
                # 2. حجم التداول الحالي (Volume) > 5 أضعاف حجم التداول السابق (Average)
                # 3. السعر الحالي أعلى من متوسط الـ 5 دقائق (VWAP)
                
                avg_vol = row.get('prev_close_volume', 10000)
                
                if 0.20 <= price <= 10.0:
                    # فلتر الـ Block Buy الحقيقي
                    if volume > (avg_vol * 5): 
                        
                        # التهدئة (Cooldown)
                        if symbol not in sent_alerts or (time.time() - sent_alerts[symbol] > 300):
                            
                            msg = (f"🚀 **فرصة Block Buy قوية**\n"
                                   f"السهم: {symbol}\n"
                                   f"السعر: {price}\n"
                                   f"قوة السيولة: {volume:,}")
                            
                            send_telegram_alert(symbol, price, msg, [])
                            sent_alerts[symbol] = time.time()
        
        time.sleep(5)
