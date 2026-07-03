"""
stage3_money_flow_detection.py
-------------------------------
المرحلة الثالثة: تأكيد التدفق المالي الكبير (Money Flow Confirmation).
بديل عن تأكيد الترند الساعي - يكشف قفزة الفوليوم الدولاري (Price × Volume)
خلال آخر عدة شمعات (MONEY_FLOW_LOOKBACK_BARS) مقارنة بمتوسط الفوليوم
الدولاري على باقي الفريم، حسب المضاعف المطلوب (MONEY_FLOW_MULTIPLIER).
"""

import pandas as pd
import config


def check_money_flow_confirmation(symbol: str, df: pd.DataFrame) -> bool:
    try:
        if df.empty or len(df) < config.MONEY_FLOW_LOOKBACK_BARS + 5:
            return False

        dollar_volume = df["Close"] * df["Volume"]

        recent = dollar_volume.tail(config.MONEY_FLOW_LOOKBACK_BARS)
        baseline = dollar_volume.iloc[: -config.MONEY_FLOW_LOOKBACK_BARS]

        if baseline.empty or baseline.mean() == 0:
            return False

        recent_avg = float(recent.mean())
        baseline_avg = float(baseline.mean())

        return recent_avg >= (baseline_avg * config.MONEY_FLOW_MULTIPLIER)

    except Exception as e:
        print(f"[check_money_flow_confirmation] خطأ بـ {symbol}: {e}")
        return False
