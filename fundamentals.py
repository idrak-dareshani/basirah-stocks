def compute_fundamentals_score(financial_statements: list) -> float:
    score = 50.0
    try:
        latest = financial_statements[0]
        prior = financial_statements[1]
        rev_growth = (float(latest.get("revenue", 0)) / max(1.0, float(prior.get("revenue", 1))) - 1) * 100
        score += min(20, max(-20, rev_growth / 5))
    except Exception:
        pass
    return max(0, min(100, score))
