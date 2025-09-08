from fastapi import FastAPI, HTTPException
import yfinance as yf
import pandas as pd

app = FastAPI()

def shariah_screening(info: dict, market_cap: float) -> dict:
    """
    Apply Shariah screening rules based on AAOIFI/DJIMI thresholds.
    """
    results = {}

    # --- Exclusion by Sector/Industry ---
    sector = info.get("sector", "").lower()
    industry = info.get("industry", "").lower()
    summary = info.get("longBusinessSummary", "").lower()

    prohibited_sectors = [
        "bank", "financial", "insurance", "alcohol", "brewery",
        "tobacco", "casino", "gambling", "defense", "weapons",
        "hotel", "entertainment", "broadcasting", "music",
        "brewing"
    ]
    prohibited = any(word in sector or word in industry or word in summary for word in prohibited_sectors)
    results["Sector Allowed"] = not prohibited

    # --- Debt Ratio ---
    total_debt = info.get("totalDebt", 0) or 0
    results["Debt Ratio"] = round(total_debt / market_cap, 2) if market_cap > 0 else None
    results["Debt Pass"] = results["Debt Ratio"] is not None and results["Debt Ratio"] < 0.3

    # --- Cash + Securities (approx using totalCash from Yahoo) ---
    cash = info.get("totalCash", 0) or 0
    results["Cash Ratio"] = round(cash / market_cap, 2) if market_cap > 0 else None
    results["Cash Pass"] = results["Cash Ratio"] is not None and results["Cash Ratio"] < 0.3

    # --- Receivables (approx using balanceSheet) ---
    try:
        bs = yf.Ticker(info["symbol"]).balance_sheet
        receivables = bs.loc["Net Receivables"].iloc[0] if "Net Receivables" in bs.index else 0
    except Exception:
        receivables = 0
    results["Receivables Ratio"] = round(receivables / market_cap, 2) if market_cap > 0 else None
    results["Receivables Pass"] = results["Receivables Ratio"] is not None and results["Receivables Ratio"] < 0.3

    # --- Interest Income (Yahoo doesn’t provide clearly, so we approximate with interestExpense/totalRevenue) ---
    total_revenue = info.get("totalRevenue", 1)
    interest_expense = info.get("interestExpense", 0) or 0
    results["Interest %"] = round(abs(interest_expense) / total_revenue, 2) if total_revenue > 0 else None
    results["Interest Pass"] = results["Interest %"] is not None and results["Interest %"] < 0.05

    # --- Final Decision ---
    results["Shariah Compliant"] = (
        results["Sector Allowed"] and
        results["Debt Pass"] and
        results["Cash Pass"] and
        results["Receivables Pass"] and
        results["Interest Pass"]
    )

    return results

@app.post("/analyze")
async def analyze(ticker: str):
    try:
        stock = yf.Ticker(ticker)

        # --- Company Info ---
        info = stock.info
        #print(info)
        market_cap = info.get("marketCap", 0)

        # --- Financial Data (simplified example from Yahoo) ---
        financials = {
            "totalDebt": info.get("totalDebt", 0),
            "totalRevenue": info.get("totalRevenue", 0),
            "interestIncome": info.get("interestExpense", 0),  # Yahoo reports expense instead of income
        }

        # --- Price Data ---
        hist = stock.history(period="6mo", interval="1d").reset_index()
        print(hist)

        # Force Date column into plain Python strings
        hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")

        prices = [
            {"Date": str(row["Date"]), "Close": float(row["Close"])}
            for _, row in hist.iterrows()
        ]

        # --- Shariah Screening ---
        screening = shariah_screening(info, market_cap)

        # --- Simple Recommendation Logic ---
        recommendation = "BUY" if screening["Shariah Compliant"] and (hist["Close"].iloc[-1] > hist["Close"].mean()) else "HOLD/AVOID"

        return {
            "company": {
                "name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "summary": info.get("longBusinessSummary", "N/A"),
                "marketCap": market_cap,
            },
            "financials": financials,
            "prices": prices,
            "shariah_screening": screening,
            "recommendation": recommendation,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
