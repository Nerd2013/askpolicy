import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/askpolicy.db")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                explanation_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
        
def store_interaction(*, question, answer, explanation):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
        "explanation": explanation,
    }

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO interactions (timestamp, question, answer, explanation_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                record["timestamp"],
                record["question"],
                record["answer"],
                json.dumps(record["explanation"]),
            ),
        )
        conn.commit()