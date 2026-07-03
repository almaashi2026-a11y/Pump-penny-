"""
main_reversal.py
-----------------
سكانر "أسهم الارتكاز" - يكتشف الأسهم المرتدة من آخر قاع حقيقي لها.

هذا Worker مستقل كلياً عن main.py (Momentum Scanner v3) - يشتغل كخدمة
Render منفصلة بنفس الريبو، عشان ما يأثر على السكانر الأصلي أبداً.
"""

import time
import logging

from stage1_finnhub_filter import get_all_us_symbols, run_stage1_filter
from stage4_reversal_detection import check_real_low_bounce
from telegram_alerts import send_telegram_alert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

SCAN_INTERVAL_SECONDS = 300       # 5 دقايق بين كل دورة سكان
ALERT_COOLDOWN_SECONDS = 60 * 60  # ساعة - نفس الرمز ما يتكرر خلالها

sent_alerts = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | REVERSAL | %(levelname)s | %(message)s"
)


def verify_connection():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("TELEGRAM_BOT_TOKEN أو TELEGRAM_CHAT_ID غير موجودين.")
        return

    sent = send_telegram_alert("SYSTEM", "-", "✅ Reversal Scanner (أسهم الارتكاز) Started", [])
    if sent:
        logging.info("Telegram Connected Successfully.")
    else:
        logging.error("فشل الاتصال بـ Telegram.")


def should_send(symbol: str) -> bool:
    now = time.time()

    if symbol not in sent_alerts:
        sent_alerts[symbol] = now
        return True

    if now - sent_alerts[symbol] >= ALERT_COOLDOWN_SECONDS:
        sent_alerts[symbol] = now
        return True

    return False


def main():
    logging.info("Starting Reversal Scan...")

    symbols = get_all_us_symbols()
    if not symbols:
        logging.error("ما جينا أي رموز من Finnhub - تجاهل هذي الدورة.")
        return

    candidates = run_stage1_filter(symbols)
    logging.info(f"{len(candidates)} مرشح جاهز لفحص الارتداد من القاع")

    for candidate in candidates:
        symbol = candidate["symbol"]

        try:
            result = check_real_low_bounce(symbol)

            if result and should_send(symbol):
                message = (
                    f"📍 آخر قاع: ${result['low_price']} بتاريخ {result['low_date']}\n"
                    f"📏 المسافة من القاع: {result['distance_from_low_pct']}%\n"
                    f"🕯️ النمط: {result['pattern']}\n"
                    f"⬆️ الارتداد فوق القاع: {result['bounce_above_low_pct']}%\n"
                    f"📊 RVOL: {result['rvol']}x"
                )

                send_telegram_alert(
                    f"🔄 {symbol}",
                    result["price"],
                    message,
                    []
                )

                logging.info(f"Alert Sent: {symbol}")

        except Exception as e:
            logging.error(f"{symbol}: {e}")

    logging.info("Reversal Scan Finished.")


if __name__ == "__main__":

    verify_connection()

    while True:

        try:
            main()
        except Exception as e:
            logging.error(e)

        time.sleep(SCAN_INTERVAL_SECONDS)
