import yfinance as yf
import requests
import pandas as pd
from config import settings
import logging

FMP_BASE = "https://site.financialmodelingprep.com/api/v3"


def fetch_price_history_yf(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    t = yf.Ticker(ticker)
    df = t.history(period=period, interval=interval)
    # Ensure Close exists
    if df.empty:
        return df
    df = df.reset_index()
    df.rename(columns={"Date": "Date"}, inplace=True)
    return df

def fetch_company_profile_fmp(ticker: str) -> dict:
    if not settings.FMP_API_KEY:
        return {}
    url = f"{FMP_BASE}/profile/{ticker}?apikey={settings.FMP_API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else {}

def fetch_financial_statements_fmp(ticker: str, statement="income-statement", limit=8) -> list:
    if not settings.FMP_API_KEY:
        return []
    url = f"{FMP_BASE}/{statement}/{ticker}?limit={limit}&apikey={settings.FMP_API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

def get_price_history(ticker: str, period="24mo", interval="1d") -> pd.DataFrame:
    # Wrapper -- use yfinance for MVP
    try:
        df = fetch_price_history_yf(ticker, period=period, interval=interval)
        # Ensure Close column is present
        if "Close" not in df.columns and "close" in df.columns:
            df.rename(columns={"close":"Close"}, inplace=True)
        return df
    except Exception as e:
        logging.exception("Error fetching price history: %s", e)
        return pd.DataFrame()
