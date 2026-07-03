"""
stage4_reversal_detection.py
------------------------------
كشف "سهم الارتكاز" - سهم مرتد من آخر قاع حقيقي له (ارتداد حقيقي مو وهمي).

المنطق:
1. نحدد آخر قاع فعلي (Swing Low) خلال آخر عدة أيام تداول.
2. نتأكد إن السعر الحالي قريب من هذا القاع (ضمن نسبة معينة).
3. نتأكد إن فيه شمعة ارتداد حقيقية على فريم 5 دقايق:
   - إغلاق أعلى من الافتتاح (شمعة خضراء)
   - إغلاق فوق القاع بمسافة واضحة (مو ملامسة وبس)
   - أو نمط Hammer (فتيل سفلي طويل يدل على رفض السعر الأدنى)
4. نشترط RVOL أعلى من المتوسط على شمعة الارتداد - عشان نتأكد إن فيه
   سيولة حقيقية وراء الارتداد، مو مجرد تذبذب بدون فوليوم.
"""

import yfinance as yf
import pandas as pd

# ============================================================
# إعدادات سكانر الارتكاز (مستقلة كلياً عن config.py الأصلي)
# ============================================================
LOW_LOOKBACK_DAYS = 10          # عدد أيام التداول اللي نبحث فيها عن القاع
PROXIMITY_TO_LOW_PCT = 5.0      # السعر الحالي لازم يكون ضمن هالنسبة من القاع
MIN_BOUNCE_ABOVE_LOW_PCT = 1.5  # إغلاق الشمعة لازم يكون أعلى من القاع بهالنسبة على الأقل
HAMMER_WICK_RATIO = 2.0         # الفتيل السفلي لازم يكون أكبر من الجسم بهالمعدل
RVOL_BOUNCE_THRESHOLD = 1.8     # RVOL المطلوب على شمعة الارتداد


def get_last_real_low(symbol: str) -> dict | None:
    """
    يجيب آخر قاع فعلي للسهم خلال آخر LOW_LOOKBACK_DAYS يوم تداول
    (يستثني اليوم الحالي عشان يكون القاع "سابق" مو لحظي).
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=f"{LOW_LOOKBACK_DAYS + 3}d", interval="1d")

        if len(hist) < 3:
            return None

        past_days = hist.iloc[:-1]
        if past_days.empty:
            return None

        low_price = float(past_days["Low"].min())
        low_date = past_days["Low"].idxmin()

        return {"low_price": low_price, "low_date": low_date}

    except Exception as e:
        print(f"[get_last_real_low] خطأ بـ {symbol}: {e}")
        return None


def check_bounce_candle(df: pd.DataFrame) -> dict:
    """
    يفحص آخر شمعة على فريم 5 دقايق: هل هي شمعة ارتداد حقيقية؟
    (شمعة خضراء واضحة أو Hammer + فوليوم أعلى من المتوسط)
    """
    last = df.iloc[-1]

    open_price = float(last["Open"])
    close_price = float(last["Close"])
    high_price = float(last["High"])
    low_price = float(last["Low"])

    body = abs(close_price - open_price)
    lower_wick = min(open_price, close_price) - low_price
    upper_wick = high_price - max(open_price, close_price)

    is_bullish_candle = close_price > open_price
    is_hammer = (
        lower_wick > 0
        and body > 0
        and lower_wick >= (body * HAMMER_WICK_RATIO)
        and upper_wick < lower_wick
    )

    avg_volume = df["Volume"].mean()
    current_volume = float(last["Volume"])
    rvol = current_volume / avg_volume if avg_volume > 0 else 0

    return {
        "is_bullish_candle": bool(is_bullish_candle),
        "is_hammer": bool(is_hammer),
        "close_price": close_price,
        "rvol": round(rvol, 2),
        "rvol_ok": rvol >= RVOL_BOUNCE_THRESHOLD,
    }


def check_real_low_bounce(symbol: str) -> dict | None:
    """
    الدالة الرئيسية: تجمع كل الشروط وتقرر هل السهم "سهم ارتكاز" مؤكد.
    ترجع تفاصيل الإشارة لو الشروط تحققت، وإلا None.
    """
    try:
        low_info = get_last_real_low(symbol)
        if not low_info:
            return None

        low_price = low_info["low_price"]

        stock = yf.Ticker(symbol)
        df = stock.history(period="1d", interval="5m")

        if df.empty or len(df) < 10:
            return None

        current_price = float(df["Close"].iloc[-1])

        distance_from_low_pct = ((current_price - low_price) / low_price) * 100
        if distance_from_low_pct < 0 or distance_from_low_pct > PROXIMITY_TO_LOW_PCT:
            return None

        candle = check_bounce_candle(df)

        bounce_above_low_pct = ((candle["close_price"] - low_price) / low_price) * 100
        bounce_ok = bounce_above_low_pct >= MIN_BOUNCE_ABOVE_LOW_PCT

        pattern_ok = candle["is_bullish_candle"] or candle["is_hammer"]

        if not (pattern_ok and bounce_ok and candle["rvol_ok"]):
            return None

        return {
            "symbol": symbol,
            "price": current_price,
            "low_price": round(low_price, 4),
            "low_date": str(low_info["low_date"].date()),
            "distance_from_low_pct": round(distance_from_low_pct, 2),
            "bounce_above_low_pct": round(bounce_above_low_pct, 2),
            "pattern": "Hammer" if candle["is_hammer"] else "شمعة خضراء",
            "rvol": candle["rvol"],
        }

    except Exception as e:
        print(f"[check_real_low_bounce] خطأ بـ {symbol}: {e}")
        return None
