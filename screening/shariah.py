from typing import Dict

def shariah_compliance_check(financials: Dict, business_summary: str) -> Dict:
    """
    Perform Shariah screening based on financial ratios and business activities.
    """
    compliance = {"status": True, "issues": []}

    # Business screen
    haram_keywords = [
        "bank", "gambling", "casino", "alcohol", "brewery",
        "wine", "pork", "lottery", "insurance", "entertainment"
    ]

    if any(word in business_summary.lower() for word in haram_keywords):
        compliance["status"] = False
        compliance["issues"].append("Non-compliant business activity detected")

    # Financial ratios
    try:
        debt_ratio = financials.get("totalDebt", 0) / financials.get("marketCap", 1)
        cash_ratio = financials.get("cash", 0) / financials.get("marketCap", 1)
        interest_ratio = financials.get("interestIncome", 0) / max(financials.get("revenue", 1), 1)

        if debt_ratio > 0.33:
            compliance["status"] = False
            compliance["issues"].append(f"Debt ratio too high: {debt_ratio:.2f}")

        if cash_ratio > 0.33:
            compliance["status"] = False
            compliance["issues"].append(f"Cash ratio too high: {cash_ratio:.2f}")

        if interest_ratio > 0.05:
            compliance["status"] = False
            compliance["issues"].append(f"Interest income too high: {interest_ratio:.2f}")

    except Exception as e:
        compliance["status"] = False
        compliance["issues"].append(f"Error in calculation: {str(e)}")

    return compliance
