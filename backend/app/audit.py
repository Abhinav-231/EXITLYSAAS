"""Append-only, hash-chained audit log (in memory for the demo).

Each entry stores the hash of the previous one, so editing history breaks the chain.
"""
import csv
import hashlib
import io
import json
from datetime import datetime, timezone


class AuditLog:
    def __init__(self) -> None:
        self._entries: list[dict] = []

    def append(self, exit_id: str, person_id: str, app_id: str, action: str, outcome: str) -> dict:
        prev = self._entries[-1]["hash"] if self._entries else "GENESIS"
        body = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "exit_id": exit_id, "person_id": person_id,
            "app_id": app_id, "action": action, "outcome": outcome, "prev_hash": prev,
        }
        body["hash"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        self._entries.append(body)
        return body

    def entries(self) -> list[dict]:
        return list(self._entries)

    def verify(self) -> bool:
        prev = "GENESIS"
        for e in self._entries:
            body = {k: v for k, v in e.items() if k != "hash"}
            if body["prev_hash"] != prev:
                return False
            if hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() != e["hash"]:
                return False
            prev = e["hash"]
        return True

    def to_csv(self) -> str:
        buf = io.StringIO()
        fields = ["timestamp", "exit_id", "person_id", "app_id", "action", "outcome", "prev_hash", "hash"]
        w = csv.DictWriter(buf, fieldnames=fields)
        w.writeheader()
        w.writerows(self._entries)
        return buf.getvalue()
