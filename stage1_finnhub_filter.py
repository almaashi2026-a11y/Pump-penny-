"""
stage1_finnhub_filter.py
-------------------------
المرحلة الأولى: فلترة سريعة وواسعة على كل الرموز باستخدام Finnhub.
الهدف: تقليل آلاف الرموز إلى قائمة قصيرة من المرشحين قبل التحليل العميق.
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import config


def get_all_us_symbols() -> list:
    """
    يجيب قائمة كل رموز الأسهم الأمريكية من Finnhub.
    """
    url = "https://finnhub.io/api/v1/stock/symbol"
    params = {"exchange": "US", "token": config.FINNHUB_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        symbols = [
            item["symbol"]
            for item in data
            if item.get("type") == "Common Stock"
        ]
        return symbols
    except Exception as e:
        print(f"[get_all_us_symbols] خطأ: {e}")
        return []


def check_symbol_basic_filter(symbol: str) -> dict | None:
    """
    يفحص رمز واحد: هل سعره وحجمه ضمن النطاق المطلوب؟
    """
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": config.FINNHUB_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        quote = response.json()

        current_price = quote.get("c", 0)
        if current_price == 0:
            return None

        if not (config.PRICE_MIN <= current_price <= config.PRICE_MAX):
            return None

        return {
            "symbol": symbol,
            "price": current_price,
            "change_pct": quote.get("dp", 0),
        }
    except Exception:
        return None


def run_stage1_filter(symbols: list) -> list:
    """
    يشغّل الفلتر الأساسي على كل الرموز بشكل متوازي (threads).
    """
    candidates = []

    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS_STAGE1) as executor:
        futures = {
            executor.submit(check_symbol_basic_filter, sym): sym
            for sym in symbols
        }

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                candidates.append(result)

    print(f"[Stage 1] {len(candidates)} مرشح من أصل {len(symbols)} رمز")
    return candidates
