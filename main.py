import time
import logging

from stage1_finnhub_filter import get_all_us_symbols, run_stage1_filter
from stage2_entry_signal import run_stage2_analysis
from telegram_alerts import send_telegram_alert
from config import (
    SCAN_INTERVAL_SECONDS,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    ALERT_COOLDOWN_MINUTES,
)

ALERT_COOLDOWN_SECONDS = ALERT_COOLDOWN_MINUTES * 60

sent_alerts = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def verify_connection():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("TELEGRAM_BOT_TOKEN أو TELEGRAM_CHAT_ID غير موجودين.")
        return

    sent = send_telegram_alert("SYSTEM", "-", "✅ Momentum Scanner Started", [])
    if sent:
        logging.info("Telegram Connected Successfully.")
    else:
        logging.error("فشل الاتصال بـ Telegram - تأكد من التوكن والشات آي دي.")


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
    logging.info("Starting Scan...")

    symbols = get_all_us_symbols()
    if not symbols:
        logging.error("ما جينا أي رموز من Finnhub - تجاهل هذي الدورة.")
        return

    candidates = run_stage1_filter(symbols)
    logging.info(f"{len(candidates)} مرشح جاهز لتحليل Stage 2 (5 دقايق)")

    for candidate in candidates:
        symbol = candidate["symbol"]

        try:
            result = run_stage2_analysis(symbol)

            if result and should_send(symbol):
                message = (
                    f"RVOL: {result['rvol']}x\n"
                    f"تغيّر السعر (15د): {result['price_change_pct']}%\n"
                    f"EMA9 فوق VWAP: ✅\n"
                    f"تدفق مالي مؤكد: ✅"
                )

                send_telegram_alert(
                    symbol,
                    result["price"],
                    message,
                    []
                )

                logging.info(f"Alert Sent: {symbol}")

        except Exception as e:
            logging.error(f"{symbol}: {e}")

    logging.info("Scan Finished.")


if __name__ == "__main__":

    verify_connection()

    while True:

        try:
            main()
        except Exception as e:
            logging.error(e)

        time.sleep(SCAN_INTERVAL_SECONDS)
