from dataclasses import dataclass

@dataclass
class RiskResult:
    score: int
    status: str
    reasons: list[str]


def calculate_risk(worker: dict, environment: dict | None = None) -> RiskResult:
    """Simple explainable rule-based risk engine for the MVP/demo.

    This is deliberately not presented as a clinically or mine-safety certified
    model. Thresholds are demo values and should be replaced/validated for any
    real deployment.
    """
    environment = environment or {}
    score = 0
    reasons: list[str] = []

    if worker.get("sos"):
        score += 45
        reasons.append("SOS activated")

    if worker.get("fall_detected"):
        score += 30
        reasons.append("Fall detected")

    if worker.get("movement") is False:
        score += 15
        reasons.append("No movement detected")

    hr = worker.get("heart_rate")
    if isinstance(hr, (int, float)) and (hr < 45 or hr > 130):
        score += 10
        reasons.append("Abnormal heart-rate reading")

    gas = environment.get("gas")
    if isinstance(gas, (int, float)):
        if gas >= 800:
            score += 25
            reasons.append("High gas indication")
        elif gas >= 500:
            score += 12
            reasons.append("Elevated gas indication")

    temp = environment.get("temperature")
    if isinstance(temp, (int, float)):
        if temp >= 45:
            score += 20
            reasons.append("High temperature")
        elif temp >= 38:
            score += 8
            reasons.append("Elevated temperature")

    score = min(score, 100)
    if score >= 65:
        status = "CRITICAL"
    elif score >= 30:
        status = "WARNING"
    else:
        status = "SAFE"

    if not reasons:
        reasons.append("No abnormal condition detected")

    return RiskResult(score=score, status=status, reasons=reasons)
