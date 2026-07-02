def send_telegram_alert(symbol, strength, message, targets):
    TOKEN = "8834876470:AAF8v7HCm6cV1U9VFCPvB1y1QHhEV-MGPKQ" 
    CHAT_ID = "Abdulrhmanscan_bot" 
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # تحويل قائمة الأهداف إلى نص آمن
    targets_text = ", ".join(targets) if targets else "لا توجد أهداف محددة"
    
    text = (f"🚨 سهم مرصود: {symbol}\n"
            f"قوة التجميع: {strength}/10\n"
            f"السبب: {message}\n"
            f"الأهداف: {targets_text}")
    
    try:
        params = {'chat_id': CHAT_ID, 'text': text}
        response = requests.get(url, params=params)
        return response.status_code == 200
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")
        return False
