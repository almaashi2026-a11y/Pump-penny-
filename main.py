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
                vol = row['volume']
                avg_vol = row.get('prev_close_volume', 100000)
                vwap = row.get('vwap', price) # سعر الـ VWAP اللحظي

                # -- الفلاتر الذكية --
                # 1. النطاق السعري
                if 0.20 <= price <= 10.0:
                    # 2. فلتر السيولة الضخمة (5x المتوسط)
                    is_huge_vol = vol > (avg_vol * 5)
                    # 3. فلتر الاتجاه (السعر فوق الـ VWAP)
                    is_uptrend = price > vwap

                    if is_huge_vol and is_uptrend:
                        # 4. فلتر التكرار (Cooldown)
                        if symbol not in sent_alerts or (time.time() - sent_alerts[symbol] > 300):
                            
                            msg = (f"🚀 **فرصة Block Buy مؤكدة**\n"
                                   f"السهم: {symbol}\n"
                                   f"السعر: {price}\n"
                                   f"حجم التداول: {vol:,}\n"
                                   f"الحالة: فوق VWAP")
                            
                            send_telegram_alert(symbol, price, msg, [])
                            sent_alerts[symbol] = time.time()
        
        time.sleep(5) # مسح كل 5 ثوانٍ
