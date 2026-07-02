import yfinance as yf
import pandas as pd
import config
from stage3_money_flow_detection import check_money_flow_confirmation


def fetch_5m_data(symbol: str) -> pd.DataFrame:
    try:
        df = yf.download(symbol, period=config.FIVE_MIN_BARS_LOOKBACK, interval="5m", progress=False)
        return df
    except Exception as e:
        print(f"[fetch_5m_data] خطأ بجلب بيانات {symbol}: {e}")
        return pd.DataFrame()


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["EMA9"] = df["Close"].ewm(span=config.EMA_PERIOD, adjust=False).mean()
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = (typical_price * df["Volume"]).cumsum() / df["Volume"].cumsum()
    return df


def check_entry_conditions(df: pd.DataFrame) -> dict:
    if df.empty or len(df) < 10:
        return {"passed": False, "reason": "بيانات غير كافية"}

    df = calculate_indicators(df)
    ema9_above_vwap = bool(df["EMA9"].iloc[-1] > df["VWAP"].iloc[-1])

    avg_volume = df["Volume"].mean()
    current_volume = df["Volume"].iloc[-1]
    rvol = current_volume / avg_volume if avg_volume > 0 else 0
    rvol_ok = rvol > config.RVOL_THRESHOLD

    if len(df) < 3:
        price_change_pct = 0
    else:
        price_change_pct = ((df["Close"].iloc[-1] - df["Close"].iloc[-3]) / df["Close"].iloc[-3]) * 100
    price_change_ok = price_change_pct >= config.PRICE_CHANGE_15M_THRESHOLD

    all_passed = ema9_above_vwap and rvol_ok and price_change_ok

    return {
        "passed": all_passed,
        "ema9_above_vwap": ema9_above_vwap,
        "rvol": round(rvol, 2),
        "rvol_ok": rvol_ok,
        "price_change_pct": round(price_change_pct, 2),
        "price_change_ok": price_change_ok,
    }


def run_stage2_analysis(symbol: str) -> dict | None:
    df = fetch_5m_data(symbol)
    if df.empty:
        return None

    entry_result = check_entry_conditions(df)
    if not entry_result["passed"]:
        return None

    money_flow_confirmed = check_money_flow_confirmation(symbol, df)
    if not money_flow_confirmed:
        print(f"⚠️ {symbol}: شروط الدخول متوفرة بس بدون تدفق مالي كافي - تجاهل")
        return None

    return {
        "symbol": symbol,
        "price": float(df["Close"].iloc[-1]),
        "rvol": entry_result["rvol"],
        "price_change_pct": entry_result["price_change_pct"],
        "money_flow_confirmed": True,
    }
