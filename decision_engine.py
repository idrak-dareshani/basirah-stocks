def decide(sharia_pass: bool, fin_score: float, tech_score: float, fund_score: float) -> dict:
    if not sharia_pass:
        return {
            "recommendation": "Avoid (Non-Shariah compliant)",
            "score": 0,
            "confidence": 1.0,
            "reason": "Failed Shariah screening."
        }

    overall = 0.4 * fund_score + 0.3 * fin_score + 0.2 * tech_score + 0.1 * 50
    if overall >= 70:
        rec = "Buy"
    elif overall >= 40:
        rec = "Hold"
    else:
        rec = "Avoid"

    confidence = min(0.99, 0.4 + (abs(overall - 50) / 100))
    return {"recommendation": rec, "score": overall, "confidence": confidence}
