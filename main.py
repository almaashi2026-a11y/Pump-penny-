import time
import logging
from moomoo import OpenQuoteContext, RET_OK
from telegram_alerts import send_telegram_alert # نعتمد على دالتك الموجودة مسبقاً
from config import MOOMOO_IP, MOOMOO_PORT # تأكد من إضافة هذه في ملف config

# إعداد الاتصال بـ Moomoo
quote_ctx = OpenQuoteContext(host=MOOMOO_IP, port=MOOMOO_PORT)
sent_alerts = {} 

def main():
    logging.info("Starting Moomoo Live Scanner...")
    
    while True:
        # جلب البيانات الحية (يمكنك تحديد قائمة الأسهم أو السوق 'US')
        ret, data = quote_ctx.get_market_snapshot(['US'])
        
        if ret == RET_OK:
            for _, row in data.iterrows():
                symbol = row['code']
                price = row['last_price']
                volume = row['volume']
                
                # فلتر: النطاق السعري المطلوب
                if 0.20 <= price <= 10.0:
                    
                    # فلتر: Block Buy (حجم ضخم يتجاوز المتوسط)
                    # ملاحظة: يمكنك استبدال row['avg_vol'] بمعادلة حسابية إذا لم تتوفر
                    if volume > (row.get('avg_vol', volume/2) * 3):
                        
                        # فلتر: Cooldown لمنع التكرار المزعج
                        current_time = time.time()
                        if symbol not in sent_alerts or (current_time - sent_alerts[symbol] > 300):
                            
                            # إرسال التنبيه
                            msg = f"🚀 {symbol} | Price: {price} | Vol: {volume}"
                            send_telegram_alert("BLOCK_BUY", price, msg, [])
                            sent_alerts[symbol] = current_time
        
        time.sleep(5) # تحديث كل 5 ثوانٍ لضمان السرعة

if __name__ == "__main__":
    main()
