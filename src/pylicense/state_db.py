from __future__ import annotations

import sqlite3
from pathlib import Path

from . import models


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS trial_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    started_on TEXT NOT NULL,
    hwid TEXT NOT NULL,
    duration_days INTEGER NOT NULL
)
"""


def ensure_trial_schema(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute(SCHEMA_SQL)
        connection.commit()


def load_trial_state(db_path: Path) -> models.TrialState | None:
    if not db_path.exists():
        return None

    ensure_trial_schema(db_path)
    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT started_on, hwid, duration_days FROM trial_state WHERE id = 1"
        ).fetchone()

    if row is None:
        return None

    return models.TrialState(
        started_on=str(row[0]),
        hwid=str(row[1]),
        duration_days=int(row[2]),
    )


def save_trial_state(db_path: Path, state: models.TrialState) -> None:
    ensure_trial_schema(db_path)
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            INSERT INTO trial_state (id, started_on, hwid, duration_days)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                started_on = excluded.started_on,
                hwid = excluded.hwid,
                duration_days = excluded.duration_days
            """,
            (state.started_on, state.hwid, state.duration_days),
        )
        connection.commit()
