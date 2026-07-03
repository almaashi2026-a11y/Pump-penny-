import time
import logging
import requests
from bs4 import BeautifulSoup
from stage3_money_flow_detection import calculate_flow
from telegram_alerts import send_telegram_alert

BOT_TOKEN = "8895817474:AAHxy3y7WfwNSFfYUY9qPNZmo4xCvlURB8o"
CHAT_ID = "8895817474"
SCAN_INTERVAL_SECONDS = 300 
MIN_SIGNAL_STRENGTH = 80
ALERT_COOLDOWN = 3600  

sent_alerts = {}

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def is_high_volume(symbol):
    try:
        url = f"https://finviz.com/quote.ashx?t={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        vol_cell = soup.find(text="Volume")
        if vol_cell:
            vol_text = vol_cell.find_next("td").text.replace(",", "")
            return int(vol_text) > 500000
        return False
    except:
        return False

def verify_connection():
    if not BOT_TOKEN or not CHAT_ID or CHAT_ID == "ضع_رقم_الـ_CHAT_ID_هنا":
        logging.error("Configuration error!")
        return False
    return True

def get_stocks_from_finviz():
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_u10,sh_price_o0.2&ft=4"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        symbols = [a.text for a in soup.find_all("a", class_="screener-link-primary")]
        return list(set(symbols))
    except Exception as e:
        logging.error(f"Finviz Error: {e}")
        return []

def main():
    logging.info("Starting Scan...")
    symbols = get_stocks_from_finviz()
    for symbol in symbols:
        try:
            if not is_high_volume(symbol):
                continue
            strength, money_flow, targets = calculate_flow(symbol)
            if strength >= MIN_SIGNAL_STRENGTH and (symbol not in sent_alerts or (time.time() - sent_alerts[symbol] >= ALERT_COOLDOWN)):
                send_telegram_alert(symbol, strength, money_flow, targets)
                sent_alerts[symbol] = time.time()
                logging.info(f"Alert Sent: {symbol}")
        except Exception as e:
            logging.error(f"{symbol}: {e}")

if __name__ == "__main__":
    if verify_connection():
        while True:
            main()
            time.sleep(SCAN_INTERVAL_SECONDS)
