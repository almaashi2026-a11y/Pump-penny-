import yfinance as yf

def calculate_flow(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="30d")
        
        if len(hist) < 30:
            return 0, "بيانات غير كافية", [0, 0]

        last_close = hist['Close'].iloc[-1]
        volatility = (hist['High'].tail(15) - hist['Low'].tail(15)).mean()
        avg_vol = hist['Volume'].tail(20).mean()
        current_vol = hist['Volume'].iloc[-1]
        
        # الشروط الجديدة
        is_tight_range = volatility < (last_close * 0.03)
        is_volume_spike = current_vol > (avg_vol * 2.0)
        
        # تصنيف الفرص
        if is_tight_range and is_volume_spike:
            return 9, "تجميع مؤسسي (مؤكد)", [round(last_close * 1.20, 2), round(last_close * 1.50, 2)]
        
        elif is_volume_spike: # هنا التنبيه السريع لأي سهم ينفجر فجأة
            return 7, "انفجار سريع (Pump)", [round(last_close * 1.10, 2), round(last_close * 1.20, 2)]
        
        else:
            return 1, "تحت المراقبة", [0, 0]
            
    except Exception:
        return 0, "خطأ تقني", [0, 0]
        
