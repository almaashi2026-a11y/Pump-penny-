import time
from datetime import datetime, timedelta

import config
from stage1_finnhub_filter import get_all_us_symbols, run_stage1_filter
from stage2_entry_signal import run_stage2_analysis
from telegram_alerts import send_telegram_alert

last_alert_time = {}


def is_in_cooldown(symbol: str) -> bool:
    if symbol not in last_alert_time:
        return False
    elapsed = datetime.now() - last_alert_time[symbol]
    return elapsed < timedelta(minutes=config.ALERT_COOLDOWN_MINUTES)


def run_single_scan_cycle():
    print(f"\n{'='*50}")
    print(f"بدء دورة سكان جديدة - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")

    all_symbols = get_all_us_symbols()
    if not all_symbols:
        print("⚠️ ما قدرنا نجيب قائمة الرموز - تخطي هذي الدورة")
        return

    stage1_candidates = run_stage1_filter(all_symbols)

    alerts_sent = 0
    for candidate in stage1_candidates:
        symbol = candidate["symbol"]
        if is_in_cooldown(symbol):
            continue

        signal = run_stage2_analysis(symbol)
        if signal is None:
            continue

        success = send_telegram_alert(signal)
        if success:
            last_alert_time[symbol] = datetime.now()
            alerts_sent += 1

    print(f"✅ انتهت الدورة - تم إرسال {alerts_sent} تنبيه")


def main():
    print("🚀 بدء تشغيل السكانر...")
    while True:
        try:
            run_single_scan_cycle()
        except Exception as e:
            print(f"❌ خطأ غير متوقع بدورة السكان: {e}")
        time.sleep(config.SCAN_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
