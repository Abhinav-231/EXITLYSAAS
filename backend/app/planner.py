import uuid

from .models import App, ExitPlan, Grant, Step
from .risk import risk_level, risk_score


def build_plan(person_id: str, grants: list[Grant], apps: dict[str, App]) -> ExitPlan:
    mine = [g for g in grants if g.person_id == person_id]
    steps: list[Step] = []
    for g in mine:
        app = apps[g.app_id]
        if app.api_revocable:
            steps.append(Step(
                app_id=app.id, app_name=app.name, action="revoke_via_api",
                requires_approval=g.role in ("admin", "owner"),
                instructions=f"Suspend the user in {app.name} through its admin API.",
            ))
        else:
            steps.append(Step(
                app_id=app.id, app_name=app.name, action="manual_checklist",
                requires_approval=False,
                instructions=f"{app.name} has no usable admin API on this plan. Remove the user in its admin console and tick this off.",
            ))
    score = risk_score(mine, apps)
    return ExitPlan(
        exit_id=str(uuid.uuid4())[:8], person_id=person_id,
        risk_score=score, risk_level=risk_level(score),
        monthly_savings=round(sum(apps[g.app_id].seat_cost_monthly for g in mine), 2),
        steps=steps,
    )
