from screening.shariah import shariah_compliance_check

def analyze_company(ticker: str, data: dict) -> dict:
    """
    Main decision engine combining fundamentals, technicals, and shariah screening.
    """
    financials = data.get("financials", {})
    business_summary = data.get("profile", {}).get("description", "")

    shariah_result = shariah_compliance_check(financials, business_summary)

    analysis = {
        "ticker": ticker,
        "shariah": shariah_result,
        "technicals": data.get("technicals", {}),
        "fundamentals": data.get("fundamentals", {}),
    }

    if not shariah_result["status"]:
        analysis["recommendation"] = "Avoid (Non-compliant)"
    else:
        analysis["recommendation"] = "Consider Buy (Compliant)"

    return analysis
