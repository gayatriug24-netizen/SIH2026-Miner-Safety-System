import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "data" / "jeevan_setu.db"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS workers (
            worker_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            zone TEXT NOT NULL,
            status TEXT NOT NULL,
            heart_rate REAL,
            movement INTEGER,
            sos INTEGER,
            fall_detected INTEGER,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS environment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gas REAL,
            temperature REAL,
            humidity REAL,
            zone TEXT,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT,
            alert_type TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            status TEXT NOT NULL,
            location TEXT,
            message TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rover (
            rover_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            target_zone TEXT,
            camera_online INTEGER NOT NULL,
            gas REAL,
            temperature REAL,
            humidity REAL,
            obstacle INTEGER,
            updated_at TEXT NOT NULL
        );
        """)


def upsert_worker(worker: dict):
    with get_conn() as conn:
        conn.execute("""
        INSERT INTO workers(worker_id, name, zone, status, heart_rate, movement, sos,
                            fall_detected, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(worker_id) DO UPDATE SET
            name=excluded.name,
            zone=excluded.zone,
            status=excluded.status,
            heart_rate=excluded.heart_rate,
            movement=excluded.movement,
            sos=excluded.sos,
            fall_detected=excluded.fall_detected,
            updated_at=excluded.updated_at
        """, (
            worker["worker_id"], worker.get("name", worker["worker_id"]),
            worker.get("zone", "UNKNOWN"), worker.get("status", "SAFE"),
            worker.get("heart_rate"), int(bool(worker.get("movement", True))),
            int(bool(worker.get("sos", False))), int(bool(worker.get("fall_detected", False))),
            worker.get("updated_at", utc_now())
        ))


def add_environment(env: dict):
    with get_conn() as conn:
        conn.execute("""
        INSERT INTO environment(gas, temperature, humidity, zone, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """, (env.get("gas"), env.get("temperature"), env.get("humidity"),
              env.get("zone", "UNKNOWN"), env.get("updated_at", utc_now())))


def add_alert(alert: dict):
    with get_conn() as conn:
        conn.execute("""
        INSERT INTO alerts(worker_id, alert_type, risk_score, status, location,
                           message, acknowledged, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        """, (alert.get("worker_id"), alert["alert_type"], alert["risk_score"],
              alert["status"], alert.get("location"), alert["message"],
              alert.get("created_at", utc_now())))


def set_rover(rover: dict):
    with get_conn() as conn:
        conn.execute("""
        INSERT INTO rover(rover_id, status, target_zone, camera_online, gas,
                          temperature, humidity, obstacle, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(rover_id) DO UPDATE SET
            status=excluded.status,
            target_zone=excluded.target_zone,
            camera_online=excluded.camera_online,
            gas=excluded.gas,
            temperature=excluded.temperature,
            humidity=excluded.humidity,
            obstacle=excluded.obstacle,
            updated_at=excluded.updated_at
        """, (rover["rover_id"], rover.get("status", "READY"), rover.get("target_zone"),
              int(bool(rover.get("camera_online", True))), rover.get("gas"),
              rover.get("temperature"), rover.get("humidity"),
              int(bool(rover.get("obstacle", False))), rover.get("updated_at", utc_now())))


def list_workers():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM workers ORDER BY worker_id")]


def list_alerts(limit=25):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,))]


def latest_environment():
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM environment ORDER BY id DESC LIMIT 1").fetchone()
        return dict(row) if row else {}


def get_rover():
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM rover WHERE rover_id='R01'").fetchone()
        return dict(row) if row else {"rover_id": "R01", "status": "READY", "camera_online": 1}


def acknowledge_alert(alert_id: int):
    with get_conn() as conn:
        cur = conn.execute("UPDATE alerts SET acknowledged=1 WHERE id=?", (alert_id,))
        return cur.rowcount > 0
