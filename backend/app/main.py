"""Exitly demo API.

All "revocations" are SIMULATED against sample data. No real vendor API is called yet.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from .audit import AuditLog
from .models import ExitPlan
from .planner import build_plan
from .sample_data import APPS, GRANTS, PEOPLE

app = FastAPI(title="Exitly (demo)", version="0.1.0")
audit = AuditLog()
plans: dict[str, ExitPlan] = {}


@app.get("/health")
def health():
    return {"status": "ok", "mode": "demo (simulated revocations)"}


@app.get("/people")
def people():
    return list(PEOPLE.values())


@app.get("/people/{person_id}/access")
def access(person_id: str):
    if person_id not in PEOPLE:
        raise HTTPException(404, "Unknown person")
    return [
        {"app": APPS[g.app_id].name, "role": g.role, "last_active": g.last_active}
        for g in GRANTS if g.person_id == person_id
    ]


@app.post("/exits/{person_id}", response_model=ExitPlan)
def start_exit(person_id: str):
    """Plan a departure: list every app, set a risk score, mark steps needing admin approval."""
    if person_id not in PEOPLE:
        raise HTTPException(404, "Unknown person")
    plan = build_plan(person_id, GRANTS, APPS)
    plans[plan.exit_id] = plan
    return plan


@app.post("/exits/{exit_id}/execute")
def execute_exit(exit_id: str, approve_sensitive: bool = False):
    """Run the plan (simulated). Steps needing approval are held unless approve_sensitive=true."""
    plan = plans.get(exit_id)
    if not plan:
        raise HTTPException(404, "Unknown exit")
    results = []
    for s in plan.steps:
        if s.action == "manual_checklist":
            outcome = "listed_for_manual_removal"
        elif s.requires_approval and not approve_sensitive:
            outcome = "held_for_admin_approval"
        else:
            outcome = "revoked_simulated"
        audit.append(exit_id, plan.person_id, s.app_id, s.action, outcome)
        results.append({"app": s.app_name, "outcome": outcome})
    return {"exit_id": exit_id, "results": results}


@app.get("/audit")
def audit_log():
    return {"chain_valid": audit.verify(), "entries": audit.entries()}


@app.get("/audit/export.csv", response_class=PlainTextResponse)
def audit_export():
    return audit.to_csv()


@app.get("/savings")
def savings():
    """Seat cost of everything granted to each person (what an exit would free up)."""
    return {
        PEOPLE[pid].name: round(sum(APPS[g.app_id].seat_cost_monthly for g in GRANTS if g.person_id == pid), 2)
        for pid in PEOPLE
    }


# Serve the simple frontend at "/" (mounted last so API routes win).
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
