"""Illustrative sample data. Nothing here is a real person or company."""
from datetime import date

from .models import App, Grant, Person, Sensitivity

APPS = {
    a.id: a
    for a in [
        App(id="gworkspace", name="Google Workspace", sensitivity=Sensitivity.high, api_revocable=True, seat_cost_monthly=12),
        App(id="github", name="GitHub", sensitivity=Sensitivity.high, api_revocable=True, seat_cost_monthly=4),
        App(id="slack", name="Slack", sensitivity=Sensitivity.medium, api_revocable=True, seat_cost_monthly=8.75),
        App(id="figma", name="Design tool", sensitivity=Sensitivity.low, api_revocable=False, seat_cost_monthly=15),
        App(id="crm", name="CRM", sensitivity=Sensitivity.high, api_revocable=False, seat_cost_monthly=25),
    ]
}

PEOPLE = {
    p.id: p
    for p in [
        Person(id="p1", name="Sam K.", email="sam@example.com"),
        Person(id="p2", name="Lena M.", email="lena@example.com"),
        Person(id="p3", name="Priya R.", email="priya@example.com"),
    ]
}

GRANTS = [
    Grant(person_id="p1", app_id="github", role="admin", last_active=date(2026, 10, 20)),
    Grant(person_id="p1", app_id="slack", role="member", last_active=date(2026, 10, 28)),
    Grant(person_id="p1", app_id="gworkspace", role="member", last_active=date(2026, 10, 30)),
    Grant(person_id="p2", app_id="figma", role="member", last_active=date(2026, 9, 1)),
    Grant(person_id="p3", app_id="crm", role="owner", last_active=date(2026, 10, 15)),
    Grant(person_id="p3", app_id="slack", role="member", last_active=date(2026, 10, 25)),
    Grant(person_id="p3", app_id="figma", role="member", last_active=None),
]
