from fastapi import FastAPI
from analysis import analyze_company

app = FastAPI()

def fetch_company_data(ticker: str) -> dict:
    # Placeholder fetcher (replace with Yahoo Finance, FMP, etc.)
    return {
        "profile": {"description": "Sample company description with financial services."},
        "financials": {
            "totalDebt": 5_000_000_000,
            "marketCap": 50_000_000_000,
            "cash": 10_000_000_000,
            "interestIncome": 200_000_000,
            "revenue": 20_000_000_000,
        },
        "technicals": {"trend": "bullish"},
        "fundamentals": {"pe_ratio": 20},
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(ticker: str):
    data = fetch_company_data(ticker)
    return analyze_company(ticker, data)
