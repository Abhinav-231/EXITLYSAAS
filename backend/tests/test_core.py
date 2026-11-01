from fastapi.testclient import TestClient

from app.audit import AuditLog
from app.main import app
from app.risk import risk_level

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_plan_risk_and_savings():
    plan = client.post("/exits/p1").json()
    assert plan["risk_level"] in {"high", "critical"}
    assert plan["monthly_savings"] > 0
    assert len(plan["steps"]) == 3


def test_manual_checklist_for_apps_without_api():
    plan = client.post("/exits/p2").json()
    assert plan["steps"][0]["action"] == "manual_checklist"


def test_sensitive_steps_held_until_approved():
    plan = client.post("/exits/p1").json()
    held = client.post(f"/exits/{plan['exit_id']}/execute").json()["results"]
    assert any(r["outcome"] == "held_for_admin_approval" for r in held)
    plan2 = client.post("/exits/p1").json()
    done = client.post(f"/exits/{plan2['exit_id']}/execute?approve_sensitive=true").json()["results"]
    assert all(r["outcome"] == "revoked_simulated" for r in done)


def test_audit_chain_detects_tampering():
    log = AuditLog()
    log.append("e1", "p1", "slack", "revoke_via_api", "revoked_simulated")
    log.append("e1", "p1", "github", "revoke_via_api", "revoked_simulated")
    assert log.verify()
    log._entries[0]["outcome"] = "edited"
    assert not log.verify()


def test_risk_levels():
    assert risk_level(5) == "low" and risk_level(85) == "critical"


def test_frontend_served():
    r = client.get("/")
    assert r.status_code == 200 and "Exitly" in r.text
