import time
from stage1_finviz_scraper import get_live_movers
# افترض أننا سنقوم بتعريف دالة تحليل التدفق المالي لاحقاً
from stage3_money_flow_detection import calculate_flow 

def scan_market():
    print("بدء عملية المسح...")
    symbols = get_live_movers() # سحب الأسهم من الفلتر
    
    for symbol in symbols:
        # هنا سأقوم بدمج منطق التحليل الفني والسيولة
        strength, money_flow, targets = calculate_flow(symbol)
        
        if strength > 7: # إذا كانت قوة السهم أكبر من 7
            send_telegram_alert(symbol, strength, money_flow, targets)

    print("جولة المسح اكتملت. انتظار 5 دقائق...")
    time.sleep(300) # انتظار 5 دقائق لضمان عدم حظر الـ IP

# تشغيل الماكينة 24/7
if __name__ == "__main__":
    while True:
        scan_market()
        
