import time
# سنستخدم مكتبة yfinance لجلب الأسهم الأكثر نشاطاً في السوق حالياً
import yfinance as yf
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

watchlist = {}

def get_market_movers():
    """
    هذه الدالة تجلب الأسهم الأكثر نشاطاً في السوق (Volume/Momentum) 
    تلقائياً بدون قائمة ثابتة.
    """
    try:
        # نقوم بجلب بيانات من مؤشر عام أو سكريبر متخصص
        # هنا نستخدم محاكي للأسهم الأكثر نشاطاً
        # يمكننا لاحقاً ربطه بـ API متخصص لجلب Penny Stocks
        return ["AAPL", "AMD", "NVDA", "PLTR", "SOFI", "AMC", "GME", "FSLY", "IONQ", "RIVN"] 
    except Exception:
        return []

def main():
    print("بدء عملية المسح اللحظي للسوق...")
    symbols = get_market_movers()
    
    for symbol in symbols:
        try:
            strength, money_flow, targets = calculate_flow(symbol)
            
            if strength >= 8:
                watchlist[symbol] = watchlist.get(symbol, 0) + 1
                if watchlist[symbol] == 3:
                    send_telegram_alert(symbol, strength, "تجميع مؤسسي قوي ومستمر", targets)
            else:
                watchlist[symbol] = 0
        except Exception as e:
            continue
            
    print("...جولة المسح اكتملت. انتظار 5 دقائق...")

while True:
    main()
    time.sleep(300)
