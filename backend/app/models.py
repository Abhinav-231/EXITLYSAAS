from datetime import date
from enum import Enum

from pydantic import BaseModel


class Sensitivity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class App(BaseModel):
    id: str
    name: str
    sensitivity: Sensitivity
    api_revocable: bool  # True if the vendor exposes an admin API we can call
    seat_cost_monthly: float


class Person(BaseModel):
    id: str
    name: str
    email: str
    active: bool = True


class Grant(BaseModel):
    person_id: str
    app_id: str
    role: str  # "member" | "admin" | "owner"
    last_active: date | None = None


class Step(BaseModel):
    app_id: str
    app_name: str
    action: str  # "revoke_via_api" | "manual_checklist"
    requires_approval: bool
    instructions: str


class ExitPlan(BaseModel):
    exit_id: str
    person_id: str
    risk_score: int
    risk_level: str
    monthly_savings: float
    steps: list[Step]
