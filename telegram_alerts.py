import os
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(symbol, strength, money_flow, targets):
    """
    إرسال تنبيه على Telegram
    
    Args:
        symbol: رمز السهم (مثلاً "AAPL")
        strength: قوة الإشارة (0-10)
        money_flow: وصف تدفق السيولة
        targets: قائمة الأهداف [target1, target2]
    """
    # التحقق من أن البيانات موجودة
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ خطأ: متغيرات Telegram غير معرّفة في Render!")
        print(f"   TELEGRAM_BOT_TOKEN: {'✅ موجود' if TELEGRAM_BOT_TOKEN else '❌ ناقص'}")
        print(f"   TELEGRAM_CHAT_ID: {'✅ موجود' if TELEGRAM_CHAT_ID else '❌ ناقص'}")
        return False
    
    # صيغة الرسالة
    message = (
        f"🚀 **فرصة انفجار محتملة!**\n\n"
        f"📈 **السهم:** ${symbol}\n"
        f"🔥 **قوة الزخم (Score):** {strength}/10\n"
        f"💰 **تدفق السيولة:** {money_flow}\n"
        f"🎯 **الأهداف المتوقعة:** {targets[0]} | {targets[1]}\n\n"
        f"🔗 [شاهد السهم على Finviz](https://finviz.com/quote.ashx?t={symbol})"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, params=params, timeout=10)
        
        # التحقق من الرد
        if response.status_code == 200:
            print(f"✅ تم إرسال التنبيه للسهم {symbol} بنجاح!")
            return True
        else:
            print(f"❌ فشل الإرسال. كود الخطأ: {response.status_code}")
            print(f"   الرد: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ انقطع الاتصال بـ Telegram (timeout)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ فشل الاتصال بـ Telegram")
        return False
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return False
