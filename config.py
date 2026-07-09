import os

# قراءة البيانات من إعدادات Render (Environment Variables)
# تأكد أن المفاتيح في Render مطابقة تماماً لهذه الأسماء
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

MOOMOO_IP = "127.0.0.1" 
MOOMOO_PORT = 11111
SCAN_INTERVAL_SECONDS = 5
ALERT_COOLDOWN_MINUTES = 5
