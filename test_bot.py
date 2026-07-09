# test_bot.py
from telegram_alerts import send_telegram_alert

# تجربة فورية
success = send_telegram_alert("TEST", 0.0, "🚀 البوت يعمل الآن بشكل صحيح!", [])
if success:
    print("✅ تم إرسال رسالة الاختبار بنجاح!")
else:
    print("❌ فشل الإرسال، تأكد من التوكن والشات آي دي في ملف config.py")
