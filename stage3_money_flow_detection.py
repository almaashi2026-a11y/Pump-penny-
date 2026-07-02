"""
stage3_money_flow_detection.py
--------------------------------
كشف "تدفق مالي كبير" على فريم 5 دقايق بدل انتظار فريم الساعة -
أنسب لأسهم البيني اللي تتحرك وتخلص خلال دقايق.
"""

import pandas as pd
import config


def calculate_dollar_volume(df: pd.DataFrame) -> pd.Series:
    """
    القيمة المالية لكل شمعة = السعر (متوسط الشمعة) × الحجم.
    """
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    return typical_price * df["Volume"]


def detect_large_money_flow(
    df: pd.DataFrame,
    lookback_bars: int = 3,
    flow_multiplier: float = 5.0,
) -> dict:
    """
    يفحص هل فيه تدفق مالي كبير خلال آخر N شمعة مقارنة بالمتوسط الطبيعي.
    """
    if df.empty or len(df) < lookback_bars + 5:
        return {"confirmed": False, "flow_ratio": 0, "recent_dollar_volume": 0}

    dollar_volume = calculate_dollar_volume(df)

    baseline = dollar_volume.iloc[:-lookback_bars]
    avg_bar_dollar_volume = baseline.mean() if len(baseline) > 0 else 0

    if avg_bar_dollar_volume == 0:
        return {"confirmed": False, "flow_ratio": 0, "recent_dollar_volume": 0}

    recent_dollar_volume = dollar_volume.tail(lookback_bars).sum()
    expected_normal_volume = avg_bar_dollar_volume * lookback_bars

    flow_ratio = (
        recent_dollar_volume / expected_normal_volume
        if expected_normal_volume > 0
        else 0
    )

    confirmed = flow_ratio >= flow_multiplier

    return {
        "confirmed": confirmed,
        "flow_ratio": round(flow_ratio, 2),
        "recent_dollar_volume": round(recent_dollar_volume, 2),
    }


def check_money_flow_confirmation(symbol: str, df_5m: pd.DataFrame) -> bool:
    """
    نقطة الدخول الرئيسية - تُستدعى من المرحلة 2 بنفس بيانات الـ5 دقايق
    (بدون استدعاء API إضافي).
    """
    result = detect_large_money_flow(
        df_5m,
        lookback_bars=config.MONEY_FLOW_LOOKBACK_BARS,
        flow_multiplier=config.MONEY_FLOW_MULTIPLIER,
    )

    if result["confirmed"]:
        print(
            f"💰 {symbol}: تدفق مالي كبير مؤكد - "
            f"{result['flow_ratio']}x المتوسط الطبيعي"
        )

    return result["confirmed"]
