#!/usr/bin/env python3
"""
test_bot.py
-----------
اختبر الاتصال بـ Telegram على Render
تأكد من أن TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID معرّفة في Environment!
"""

import sys
import os

print("=" * 60)
print("🤖 اختبار اتصال Telegram Bot على Render")
print("=" * 60)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

print("\n📋 التحقق من المتغيرات:")
print(f"  ✓ TELEGRAM_BOT_TOKEN: {'✅ موجود' if TELEGRAM_BOT_TOKEN else '❌ ناقص'}")
print(f"  ✓ TELEGRAM_CHAT_ID: {'✅ موجود' if TELEGRAM_CHAT_ID else '❌ ناقص'}")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("\n⚠️  تحذير: البيانات غير كاملة!")
    print("\n📌 خطوات الحل:")
    print("   1. اذهب إلى Render Dashboard")
    print("   2. اختر المشروع > Environment")
    print("   3. أضف المتغيرات:")
    print("      - TELEGRAM_BOT_TOKEN = [توكن البوت من BotFather]")
    print("      - TELEGRAM_CHAT_ID = [معرّف الدردشة]")
    print("   4. اضغط Save و Deploy")
    sys.exit(1)

from telegram_alerts import send_telegram_alert

print("\n🔄 محاولة إرسال رسالة اختبار...")
print("-" * 60)

# إرسال الرسالة (بنفس توقيع الدالة الجديد: symbol, price, message, targets)
success = send_telegram_alert(
    "TEST_BOT",
    "0.15",
    "✅ اختبار الاتصال - إذا وصلت هذه الرسالة فالبوت يعمل على Render!",
    ["$0.25", "$0.30"]
)

print("-" * 60)

if success:
    print("\n✅ النتيجة: اتصال ناجح! 🎉")
    print("   البوت جاهز للعمل على Render 🚀")
    sys.exit(0)
else:
    print("\n❌ النتيجة: فشل الاتصال")
    print("\n🔍 تحقق من:")
    print("   1. هل الـ Token صحيح؟")
    print("   2. هل الـ Chat ID صحيح؟")
    print("   3. هل البوت موجود وفعال على Telegram؟")
    print("   4. هل الإنترنت متصل على Render؟")
    sys.exit(1)
