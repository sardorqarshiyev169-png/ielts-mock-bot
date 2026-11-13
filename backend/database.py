import sqlite3
import json
import logging
from contextlib import contextmanager
from pathlib import Path
from .config import DB_PATH

logger = logging.getLogger(__name__)

@contextmanager
def get_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initializes tables and indexes synchronously"""
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                target_band REAL DEFAULT 7.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                time_limit_minutes INTEGER DEFAULT 60,
                difficulty TEXT DEFAULT 'Medium',
                description TEXT,
                is_published INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                section_number INTEGER NOT NULL,
                title TEXT,
                passage_text TEXT,
                audio_file TEXT,
                instructions TEXT,
                FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER NOT NULL,
                question_number INTEGER NOT NULL,
                question_type TEXT NOT NULL,
                prompt TEXT NOT NULL,
                options_json TEXT,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS test_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tg_id INTEGER,
                test_id INTEGER NOT NULL,
                section_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                band_score REAL NOT NULL,
                user_answers_json TEXT,
                time_spent_seconds INTEGER,
                feedback_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
            )
        """)

        logger.info("Database initialized successfully at %s", DB_PATH)

def get_or_create_user(tg_id: int, username: str = "", full_name: str = "") -> dict:
    with get_db() as db:
        cursor = db.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        
        db.execute(
            "INSERT INTO users (tg_id, username, full_name) VALUES (?, ?, ?)",
            (tg_id, username or "", full_name or "Candidate")
        )
        cursor = db.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        return dict(cursor.fetchone())

def list_tests(test_type: str = None) -> list:
    with get_db() as db:
        query = "SELECT * FROM tests WHERE is_published = 1"
        params = []
        if test_type and test_type != "all":
            query += " AND type = ?"
            params.append(test_type)
        query += " ORDER BY id DESC"
        
        cursor = db.execute(query, params)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            t = dict(r)
            q_cur = db.execute(
                "SELECT COUNT(*) FROM questions q JOIN sections s ON q.section_id = s.id WHERE s.test_id = ?",
                (t["id"],)
            )
            t["question_count"] = q_cur.fetchone()[0]
            results.append(t)
        return results

def get_test_details(test_id: int) -> dict:
    with get_db() as db:
        cursor = db.execute("SELECT * FROM tests WHERE id = ?", (test_id,))
        test_row = cursor.fetchone()
        if not test_row:
            return None
        test = dict(test_row)

        cursor = db.execute("SELECT * FROM sections WHERE test_id = ? ORDER BY section_number ASC", (test_id,))
        sections_rows = cursor.fetchall()
        test["sections"] = []
        for s in sections_rows:
            sec = dict(s)
            q_cursor = db.execute(
                "SELECT * FROM questions WHERE section_id = ? ORDER BY question_number ASC",
                (sec["id"],)
            )
            questions = []
            for q in q_cursor.fetchall():
                qd = dict(q)
                if qd.get("options_json"):
                    try:
                        qd["options"] = json.loads(qd["options_json"])
                    except Exception:
                        qd["options"] = []
                else:
                    qd["options"] = []
                questions.append(qd)
            sec["questions"] = questions
            test["sections"].append(sec)

        return test

def save_attempt(user_id: int, tg_id: int, test_id: int, section_type: str, 
                 score: int, max_score: int, band_score: float, 
                 user_answers: dict, time_spent: int, feedback: dict) -> int:
    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO test_attempts 
            (user_id, tg_id, test_id, section_type, score, max_score, band_score, user_answers_json, time_spent_seconds, feedback_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            tg_id,
            test_id,
            section_type,
            score,
            max_score,
            band_score,
            json.dumps(user_answers),
            time_spent,
            json.dumps(feedback)
        ))
        return cursor.lastrowid

def get_user_attempts(tg_id: int) -> list:
    with get_db() as db:
        cursor = db.execute("""
            SELECT a.*, t.title as test_title 
            FROM test_attempts a 
            LEFT JOIN tests t ON a.test_id = t.id 
            WHERE a.tg_id = ? 
            ORDER BY a.created_at DESC LIMIT 20
        """, (tg_id,))
        return [dict(r) for r in cursor.fetchall()]
