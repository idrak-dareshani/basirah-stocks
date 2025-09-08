from fastapi import FastAPI, HTTPException, Query
from data_fetcher import get_price_history, fetch_company_profile_fmp, fetch_financial_statements_fmp
from sharia_screen import business_activity_screen, financial_ratio_screen
from technicals import compute_technical_indicators, compute_trend_score
from fundamentals import compute_fundamentals_score
from decision_engine import decide
import pandas as pd

app = FastAPI(title="Sharia Stock Analyst (MVP)")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analyze")
def analyze(ticker: str = Query(..., min_length=1)):
    ticker = ticker.upper().strip()
    # 1. Data fetch
    prices = get_price_history(ticker, period="24mo", interval="1d")
    if prices is None or prices.empty:
        raise HTTPException(status_code=404, detail="Ticker not found or no price data")
    profile = fetch_company_profile_fmp(ticker) or {}
    financials = fetch_financial_statements_fmp(ticker, limit=8) or []

    # 2. Indicators
    df_ind = compute_technical_indicators(prices)
    tech_score = compute_trend_score(df_ind)

    # 3. Fundamentals & marketcap avg
    try:
        latest_shares = profile.get("sharesOutstanding") or profile.get("sharesOutstanding","") 
        if latest_shares:
            market_caps = prices["Close"] * float(latest_shares)
            avg_market_cap = market_caps.mean()
        else:
            avg_market_cap = float(profile.get("mktCap") or profile.get("marketCap") or (prices["Close"].mean() * 1_000_000))
    except Exception:
        avg_market_cap = prices["Close"].mean() * 1_000_000

    fin_ratios = financial_ratio_screen(financials[0] if financials else {}, avg_market_cap)
    fund_score = compute_fundamentals_score(financials)
    sharia_business = business_activity_screen(profile)

    decision = decide(sharia_business.get("pass", False) and fin_ratios.get("pass", False),
                      fin_score=(100 if fin_ratios.get("pass", False) else 30),
                      tech_score=tech_score, fund_score=fund_score)

    # Prepare compact technical latest snapshot
    latest_tech = df_ind.iloc[-1].to_dict() if not df_ind.empty else {}

    return {
        "ticker": ticker,
        "profile": profile,
        "sharia_business": sharia_business,
        "financial_ratios": fin_ratios,
        "technical": {"latest": latest_tech, "trend_score": tech_score},
        "fundamentals_score": fund_score,
        "decision": decision
    }
