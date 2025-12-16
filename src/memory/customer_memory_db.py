import sqlite3
import os
from datetime import datetime


class CustomerMemoryDB:
    """
    Stores and retrieves customer communication preferences
    learned from feedback and previous interactions.

    Fields stored:
        - customer_id
        - preferred_tone
        - preferred_language
        - last_feedback
        - revision_count
        - updated_at
    """

    def __init__(self, db_path="customer_memory.db"):
        self.db_path = db_path
        self._ensure_db()

    # --------------------------------------------------------
    # DB Initialization
    # --------------------------------------------------------
    def _ensure_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS customer_memory (
                customer_id TEXT PRIMARY KEY,
                preferred_tone TEXT,
                preferred_language TEXT,
                last_feedback TEXT,
                revision_count INTEGER DEFAULT 0,
                updated_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    # --------------------------------------------------------
    # Save or update memory
    # --------------------------------------------------------
    def save_tone(
        self,
        customer_id,
        preferred_tone=None,
        preferred_language=None,
        feedback=None
    ):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # load existing
        existing = self.load_tone(customer_id)

        revision_count = (existing.get("revision_count", 0) if existing else 0)

        if feedback:
            revision_count += 1

        cur.execute("""
            INSERT INTO customer_memory (
                customer_id, preferred_tone, preferred_language,
                last_feedback, revision_count, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(customer_id)
            DO UPDATE SET
                preferred_tone=COALESCE(excluded.preferred_tone, customer_memory.preferred_tone),
                preferred_language=COALESCE(excluded.preferred_language, customer_memory.preferred_language),
                last_feedback=COALESCE(excluded.last_feedback, customer_memory.last_feedback),
                revision_count=?,
                updated_at=excluded.updated_at
        """, (
            customer_id,
            preferred_tone,
            preferred_language,
            feedback,
            revision_count,
            datetime.utcnow().isoformat(),
            revision_count
        ))

        conn.commit()
        conn.close()

    # --------------------------------------------------------
    # Load memory
    # --------------------------------------------------------
    def load_tone(self, customer_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            SELECT preferred_tone, preferred_language, last_feedback, revision_count
            FROM customer_memory
            WHERE customer_id = ?
        """, (customer_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            return {}

        return {
            "preferred_tone": row[0],
            "preferred_language": row[1],
            "last_feedback": row[2],
            "revision_count": row[3]
        }

    # --------------------------------------------------------
    # Delete memory for testing
    # --------------------------------------------------------
    def delete_memory(self, customer_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM customer_memory WHERE customer_id = ?", (customer_id,))
        conn.commit()
        conn.close()

    # --------------------------------------------------------
    # Clear all memory
    # --------------------------------------------------------
    def clear_all(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM customer_memory")
        conn.commit()
        conn.close()
