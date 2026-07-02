from telegram_alerts import send_telegram_alert

try:
    send_telegram_alert("TEST", 0, "تجربة اتصال البوت - إذا وصلت هذه الرسالة فالبوت يعمل!", ["اختبار"])
    print("تم إرسال الرسالة بنجاح!")
except Exception as e:
    print(f"حدث خطأ أثناء الاتصال: {e}")
