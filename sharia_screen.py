from typing import Dict
import math

BUSINESS_KEYWORDS = [
    "bank", "finance", "insurance", "gambl", "casino", "alcohol", "brewery",
    "tobacco", "pork", "porn", "adult", "defense", "weapon", "movie", "film"
]

def business_activity_screen(profile: Dict, revenue_breakdown: Dict | None = None) -> dict:
    reasons = []
    name = profile.get("companyName") or profile.get("longName") or profile.get("shortName", "")
    summary = profile.get("description", "") or profile.get("industry", "") or ""
    lower = (str(name) + " " + str(summary)).lower()
    flagged = [kw for kw in BUSINESS_KEYWORDS if kw in lower]

    if revenue_breakdown:
        for k, pct in revenue_breakdown.items():
            if pct > 0.05:
                reasons.append(f"Revenue from prohibited activity '{k}' = {pct:.2%}")
    else:
        if flagged:
            reasons.append(f"Business keywords flagged: {flagged}")

    return {"pass": len(reasons) == 0, "reasons": reasons, "flagged_keywords": flagged}

def financial_ratio_screen(financials: dict, avg_market_cap: float) -> dict:
    td = float(financials.get("totalDebt", 0) or 0)
    cash = float(financials.get("cashAndShortTermInvestments", 0) or 0)
    ar = float(financials.get("accountsReceivable", 0) or 0)
    interest = float(financials.get("interestIncome", 0) or 0)
    revenue = float(financials.get("revenue", 1) or 1)

    out = {}
    out["debt_ratio"] = td / avg_market_cap if avg_market_cap else math.inf
    out["cash_ratio"] = cash / avg_market_cap if avg_market_cap else math.inf
    out["receivables_ratio"] = ar / avg_market_cap if avg_market_cap else math.inf
    out["interest_income_ratio"] = interest / revenue if revenue else 0

    thresholds = {"debt": 0.33, "cash": 0.33, "receivables": 0.33, "interest_income": 0.05}
    out["pass"] = all([
        out["debt_ratio"] <= thresholds["debt"],
        out["cash_ratio"] <= thresholds["cash"],
        out["receivables_ratio"] <= thresholds["receivables"],
        out["interest_income_ratio"] <= thresholds["interest_income"]
    ])
    out["thresholds"] = thresholds
    return out
