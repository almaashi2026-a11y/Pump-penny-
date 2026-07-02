"""
stage1_finnhub_filter.py
-------------------------
المرحلة الأولى: فلترة سريعة وواسعة على كل الرموز باستخدام Finnhub.
الهدف: تقليل آلاف الرموز إلى قائمة قصيرة من المرشحين قبل التحليل العميق.
"""

import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import config

# ============================================================
# كاش قائمة الرموز - نجيبها مرة وحدة ونحتفظ فيها بدل ما نطلبها
# كل دورة سكان (endpoint ثقيل ويسبب 429 Too Many Requests)
# ============================================================
_symbols_cache = {"symbols": [], "fetched_at": 0}
SYMBOLS_CACHE_TTL_SECONDS = 24 * 60 * 60  # 24 ساعة


def get_all_us_symbols(retries: int = 3) -> list:
    """
    يجيب قائمة كل رموز الأسهم الأمريكية من Finnhub، مع كاش لمدة 24 ساعة
    و retry logic لمقاومة 429 (خصوصاً أول تشغيل بعد إعادة نشر جديدة).
    """
    now = time.time()
    cache_age = now - _symbols_cache["fetched_at"]

    if _symbols_cache["symbols"] and cache_age < SYMBOLS_CACHE_TTL_SECONDS:
        print(f"[get_all_us_symbols] استخدام الكاش (عمره {int(cache_age/60)} دقيقة)")
        return _symbols_cache["symbols"]

    url = "https://finnhub.io/api/v1/stock/symbol"
    params = {"exchange": "US", "token": config.FINNHUB_API_KEY}

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=15)

            if response.status_code == 429:
                wait_time = 3 * (attempt + 1)
                print(f"[get_all_us_symbols] 429 - محاولة {attempt+1}، ننتظر {wait_time}ث")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            data = response.json()
            symbols = [
                item["symbol"]
                for item in data
                if item.get("type") == "Common Stock"
            ]

            _symbols_cache["symbols"] = symbols
            _symbols_cache["fetched_at"] = now
            print(f"[get_all_us_symbols] تم جلب {len(symbols)} رمز وتخزينهم بالكاش")
            return symbols
        except Exception as e:
            print(f"[get_all_us_symbols] خطأ: {e}")
            break

    if _symbols_cache["symbols"]:
        print("[get_all_us_symbols] استخدام الكاش القديم كخطة بديلة")
        return _symbols_cache["symbols"]
    return []


def check_symbol_basic_filter(symbol: str, retries: int = 2) -> dict | None:
    """
    يفحص رمز واحد: هل سعره وحجمه ضمن النطاق المطلوب؟
    فيه إعادة محاولة تلقائية (retry) لو صار 429.
    """
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": config.FINNHUB_API_KEY}

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 429:
                wait_time = 1.5 * (attempt + 1)
                time.sleep(wait_time)
                continue

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

    return None


def run_stage1_filter(symbols: list) -> list:
    """
    يشغّل الفلتر الأساسي على كل الرموز بشكل متوازي (threads)، مع تأخير
    بسيط بين الدفعات (batches) عشان نتجنب rate limit.
    """
    candidates = []
    batch_size = config.MAX_WORKERS_STAGE1 * 5

    for i in range(0, len(symbols), batch_size):
        batch = symbols[i : i + batch_size]

        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS_STAGE1) as executor:
            futures = {
                executor.submit(check_symbol_basic_filter, sym): sym
                for sym in batch
            }

            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    candidates.append(result)

        time.sleep(1)

    print(f"[Stage 1] {len(candidates)} مرشح من أصل {len(symbols)} رمز")
    return candidates
