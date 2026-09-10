from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
from datetime import datetime, timezone

from database import (
    init_db, upsert_worker, add_environment, add_alert, set_rover,
    list_workers, list_alerts, latest_environment, get_rover,
    acknowledge_alert, utc_now,
)
from risk_engine import calculate_risk

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
CORS(app)
init_db()


def evaluate_and_store(worker: dict, environment: dict | None = None):
    result = calculate_risk(worker, environment)
    worker = dict(worker)
    worker["status"] = result.status
    worker["updated_at"] = utc_now()
    upsert_worker(worker)

    if result.status in {"WARNING", "CRITICAL"}:
        alert_type = "MAN_DOWN" if worker.get("fall_detected") else "HAZARD"
        if worker.get("sos"):
            alert_type = "SOS"
        add_alert({
            "worker_id": worker.get("worker_id"),
            "alert_type": alert_type,
            "risk_score": result.score,
            "status": result.status,
            "location": worker.get("zone"),
            "message": "; ".join(result.reasons),
        })
    return result


@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "Jeevan Setu backend", "time": utc_now()})


@app.get("/api/workers")
def workers():
    return jsonify(list_workers())


@app.get("/api/alerts")
def alerts():
    return jsonify(list_alerts())


@app.get("/api/environment")
def environment():
    return jsonify(latest_environment())


@app.get("/api/rover")
def rover():
    return jsonify(get_rover())


@app.post("/api/worker/update")
def worker_update():
    payload = request.get_json(silent=True) or {}
    if not payload.get("worker_id"):
        return jsonify({"error": "worker_id is required"}), 400

    env = payload.get("environment") or latest_environment()
    if env:
        add_environment(env)
    result = evaluate_and_store(payload, env)
    return jsonify({"worker": payload, "risk": result.__dict__})


@app.post("/api/rover/update")
def rover_update():
    payload = request.get_json(silent=True) or {}
    payload.setdefault("rover_id", "R01")
    payload["updated_at"] = utc_now()
    set_rover(payload)
    if any(k in payload for k in ("gas", "temperature", "humidity")):
        add_environment({
            "gas": payload.get("gas"),
            "temperature": payload.get("temperature"),
            "humidity": payload.get("humidity"),
            "zone": payload.get("target_zone", "UNKNOWN"),
        })
    return jsonify(get_rover())


@app.post("/api/rover/deploy")
def rover_deploy():
    payload = request.get_json(silent=True) or {}
    zone = payload.get("target_zone", "UNKNOWN")
    rover = get_rover()
    rover.update({"status": "DEPLOYED", "target_zone": zone, "camera_online": True, "updated_at": utc_now()})
    set_rover(rover)
    return jsonify(rover)


@app.post("/api/rover/reset")
def rover_reset():
    rover = get_rover()
    rover.update({"status": "READY", "target_zone": None, "camera_online": True, "updated_at": utc_now()})
    set_rover(rover)
    return jsonify(rover)


@app.post("/api/alerts/<int:alert_id>/acknowledge")
def acknowledge(alert_id: int):
    if not acknowledge_alert(alert_id):
        return jsonify({"error": "alert not found"}), 404
    return jsonify({"ok": True, "alert_id": alert_id})


@app.post("/api/demo/reset")
def demo_reset():
    # Rebuild a clean demonstration state with 3 workers and a ready rover.
    from database import get_conn
    with get_conn() as conn:
        conn.execute("DELETE FROM workers")
        conn.execute("DELETE FROM environment")
        conn.execute("DELETE FROM alerts")
        conn.execute("DELETE FROM rover")
    for worker in [
        {"worker_id": "W01", "name": "Worker 01", "zone": "N1", "status": "SAFE", "heart_rate": 78, "movement": True, "sos": False, "fall_detected": False},
        {"worker_id": "W02", "name": "Worker 02", "zone": "N3", "status": "SAFE", "heart_rate": 82, "movement": True, "sos": False, "fall_detected": False},
        {"worker_id": "W03", "name": "Worker 03", "zone": "N4", "status": "SAFE", "heart_rate": 80, "movement": True, "sos": False, "fall_detected": False},
    ]:
        upsert_worker(worker)
    add_environment({"gas": 180, "temperature": 31, "humidity": 65, "zone": "N3"})
    set_rover({"rover_id": "R01", "status": "READY", "target_zone": None, "camera_online": True, "gas": 180, "temperature": 31, "humidity": 65, "obstacle": False})
    return jsonify({"ok": True})


@app.post("/api/demo/emergency")
def demo_emergency():
    # One-click scenario for internal hackathon demo.
    worker = {
        "worker_id": "W03", "name": "Worker 03", "zone": "N4",
        "heart_rate": 86, "movement": False, "sos": True,
        "fall_detected": True,
    }
    env = {"gas": 860, "temperature": 42, "humidity": 74, "zone": "N4"}
    result = evaluate_and_store(worker, env)
    rover = get_rover()
    rover.update({"status": "DEPLOYED", "target_zone": "N4", "camera_online": True,
                  "gas": 860, "temperature": 42, "humidity": 74, "updated_at": utc_now()})
    set_rover(rover)
    return jsonify({"worker": worker, "risk": result.__dict__, "rover": rover})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
