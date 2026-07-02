import yfinance as yf

def calculate_flow(symbol):
    try:
        # جلب البيانات
        stock = yf.Ticker(symbol)
        hist = stock.history(period="5d")
        
        if len(hist) < 2:
            return 0, "مجهول", [0, 0]

        last_close = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        
        # حساب التغير
        price_change = ((last_close - prev_close) / prev_close) * 100
        
        # تقييم القوة (Score)
        strength = min(10, max(1, int(price_change * 2)))
        
        # الأهداف
        atr = (hist['High'] - hist['Low']).mean()
        targets = [round(last_close + (atr * 1.5), 2), round(last_close + (atr * 3), 2)]
        
        money_flow = "إيجابي" if price_change > 0 else "سلبي"
        
        return strength, money_flow, targets
    except Exception:
        return 0, "خطأ", [0, 0]
