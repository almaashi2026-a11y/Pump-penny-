"""
test_bot.py
-----------
اختبر الاتصال بـ Telegram قبل تشغيل المسح الكامل
تأكد من أن TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID معرّفة في Render!
"""

import sys
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from telegram_alerts import send_telegram_alert

print("=" * 50)
print("🤖 اختبار اتصال Telegram Bot")
print("=" * 50)

# التحقق من البيانات
print("\n📋 التحقق من المتغيرات:")
print(f"  ✓ TELEGRAM_BOT_TOKEN: {'✅ موجود' if TELEGRAM_BOT_TOKEN else '❌ ناقص'}")
print(f"  ✓ TELEGRAM_CHAT_ID: {'✅ موجود' if TELEGRAM_CHAT_ID else '❌ ناقص'}")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("\n⚠️  تحذير: البيانات غير كاملة!")
    print("   إضف البيانات في Render > Environment Variables:")
    print("   1. TELEGRAM_BOT_TOKEN")
    print("   2. TELEGRAM_CHAT_ID")
    sys.exit(1)

# محاولة الإرسال
print("\n🔄 محاولة إرسال رسالة اختبار...")
print("-" * 50)

success = send_telegram_alert(
    symbol="TEST",
    strength=9,
    money_flow="اختبار اتصال البوت - إذا وصلت هذه الرسالة فالبوت يعمل!",
    targets=["$0.25", "$0.30"]
)

print("-" * 50)

if success:
    print("\n✅ النتيجة: اتصال ناجح!")
    print("   البوت جاهز للعمل 🚀")
    sys.exit(0)
else:
    print("\n❌ النتيجة: فشل الاتصال")
    print("   تحقق من:")
    print("   - الـ Token صحيح؟")
    print("   - الـ Chat ID صحيح؟")
    print("   - الإنترنت متصل على Render؟")
    sys.exit(1)
