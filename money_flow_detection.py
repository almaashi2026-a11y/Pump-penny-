import yfinance as yf

def calculate_flow(symbol):
    try:
        stock = yf.Ticker(symbol)
        # نستخدم بيانات 30 يوم لنرصد فترة تجميع أطول وأقوى
        hist = stock.history(period="30d")
        
        if len(hist) < 30:
            return 0, "بيانات غير كافية", [0, 0]

        last_close = hist['Close'].iloc[-1]
        # التذبذب (Volatility) في آخر 15 يوم
        volatility = (hist['High'].tail(15) - hist['Low'].tail(15)).mean()
        # متوسط الفوليوم لآخر 20 يوم
        avg_vol = hist['Volume'].tail(20).mean()
        current_vol = hist['Volume'].iloc[-1]
        
        # شروط التجميع (Accumulation Logic):
        # 1. نطاق حركة السعر ضيق جداً (أقل من 3% من السعر) - "هدوء"
        # 2. الفوليوم الحالي يجب أن يكون ضعف متوسط الفوليوم (دخول سيولة مؤسسية)
        is_tight_range = volatility < (last_close * 0.03) 
        is_volume_spike = current_vol > (avg_vol * 2.0)
        
        if is_tight_range and is_volume_spike:
            strength = 9
            money_flow = "تجميع مؤسسي (مؤكد)"
            # أهداف طموحة لمرحلة الانفجار
            targets = [round(last_close * 1.20, 2), round(last_close * 1.50, 2)]
            return strength, money_flow, targets
        else:
            return 1, "تحت المراقبة", [0, 0]
            
    except Exception:
        return 0, "خطأ تقني", [0, 0]
        
