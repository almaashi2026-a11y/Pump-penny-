import time
import logging
import requests
from bs4 import BeautifulSoup

from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    SCAN_INTERVAL_SECONDS
)

BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TELEGRAM_CHAT_ID

# الحد الأدنى لقوة الإشارة
MIN_SIGNAL_STRENGTH = 80

# عدم تكرار الإشارات
ALERT_COOLDOWN = 3600  # ساعة

sent_alerts = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def verify_connection():
    if not BOT_TOKEN or not CHAT_ID:
        logging.error("BOT_TOKEN أو CHAT_ID غير موجودين.")
        return

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.get(
            url,
            params={
                "chat_id": CHAT_ID,
                "text": "✅ Pump Penny Scanner Started"
            },
            timeout=20
        )

        logging.info("Telegram Connected Successfully.")

    except Exception as e:
        logging.error(f"Telegram Error: {e}")


def get_stocks_from_finviz():

    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"

    try:

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )

        soup = BeautifulSoup(response.text, "html.parser")

        symbols = [
            a.text
            for a in soup.find_all(
                "a",
                class_="screener-link-primary"
            )
        ]

        return list(set(symbols))

    except Exception as e:

        logging.error(f"Finviz Error: {e}")

        return []


def should_send(symbol):

    now = time.time()

    if symbol not in sent_alerts:
        sent_alerts[symbol] = now
        return True

    if now - sent_alerts[symbol] >= ALERT_COOLDOWN:
        sent_alerts[symbol] = now
        return True

    return False


def main():

    logging.info("Starting Scan...")

    symbols = get_stocks_from_finviz()

    logging.info(f"{len(symbols)} symbols found.")

    for symbol in symbols:

        try:

            strength, money_flow, targets = calculate_flow(symbol)

            if strength >= MIN_SIGNAL_STRENGTH:

                if should_send(symbol):

                    send_telegram_alert(
                        symbol,
                        strength,
                        money_flow,
                        targets
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
