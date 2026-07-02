import yfinance as yf

def calculate_flow(symbol):
    # جلب البيانات التاريخية لآخر 5 أيام لتحليل الزخم
    stock = yf.Ticker(symbol)
    hist = stock.history(period="5d")
    
    if len(hist) < 2:
        return 0, 0, []

    # حساب مؤشرات بسيطة لكنها قوية (الخلطة السرية)
    last_close = hist['Close'].iloc[-1]
    prev_close = hist['Close'].iloc[-2]
    volume_change = hist['Volume'].iloc[-1] / hist['Volume'].mean()
    
    # تحديد قوة السهم (Score من 1-10)
    # إذا زاد السعر مع فوليوم عالي، القوة تزيد
    price_change = ((last_close - prev_close) / prev_close) * 100
    strength = min(10, int(price_change * volume_change)) 
    
    # حساب أهداف تقديرية بناءً على التقلب (ATR-like approach)
    atr = (hist['High'] - hist['Low']).mean()
    targets = [round(last_close + (atr * 1.5), 2), round(last_close + (atr * 3), 2)]
    
    # صافي تدفق السيولة (Money Flow Proxy)
    money_flow = "إيجابي" if price_change > 0 else "سلبي"
    
    return strength, money_flow, targets
  
