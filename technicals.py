import pandas as pd
import pandas_ta as ta

def compute_technical_indicators(price_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.copy()
    if "Close" not in df.columns:
        raise ValueError("price_df must contain 'Close' column")
    # Ensure index by Date if present
    if "Date" in df.columns:
        df = df.set_index("Date")

    df["SMA50"] = ta.sma(df["Close"], length=50)
    df["SMA200"] = ta.sma(df["Close"], length=200)
    df["RSI14"] = ta.rsi(df["Close"], length=14)
    macd = ta.macd(df["Close"])
    df = pd.concat([df, macd], axis=1)
    return df.dropna()

def compute_trend_score(df: pd.DataFrame) -> float:
    if df.empty:
        return 50.0
    latest = df.iloc[-1]
    score = 50.0
    try:
        if latest.get("SMA50") > latest.get("SMA200"):
            score += 20
        rsi = latest.get("RSI14") or 50
        if rsi < 30:
            score -= 10
        elif rsi > 70:
            score -= 5
        price = latest.get("Close")
        sma50 = latest.get("SMA50") or price
        score += min(20, max(-20, (price / sma50 - 1) * 100))
    except Exception:
        pass
    return max(0, min(100, score))
