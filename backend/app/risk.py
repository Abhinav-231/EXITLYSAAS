from .models import App, Grant, Sensitivity

SENSITIVITY_WEIGHT = {Sensitivity.low: 5, Sensitivity.medium: 15, Sensitivity.high: 30}
ROLE_MULTIPLIER = {"member": 1.0, "admin": 1.5, "owner": 1.75}


def risk_score(grants: list[Grant], apps: dict[str, App]) -> int:
    """0-100 score: what could this person still reach if nothing is revoked?"""
    total = 0.0
    for g in grants:
        app = apps[g.app_id]
        total += SENSITIVITY_WEIGHT[app.sensitivity] * ROLE_MULTIPLIER.get(g.role, 1.0)
    return min(100, round(total))


def risk_level(score: int) -> str:
    if score >= 70:
        return "critical"
    if score >= 40:
        return "high"
    if score >= 20:
        return "medium"
    return "low"
