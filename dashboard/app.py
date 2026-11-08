"""KRITIS Detection Lab - web GUI.

Shows the simulated plant (read over Modbus), runs the lab attack scenarios
against the simulator, and lists the Suricata alerts from eve.json.
LAB USE ONLY: the scenarios only ever target TARGET (the simulator container).
"""
import json
import os
import time
from datetime import datetime

from flask import Flask, jsonify
from pymodbus.client import ModbusTcpClient

TARGET = os.getenv("TARGET", "plc-sim")
EVE_LOG = os.getenv("EVE_LOG", "/logs/eve.json")

app = Flask(__name__, static_folder="static", static_url_path="")

SIGNATURES = {
    9000001: "T0846 Remote System Discovery",
    9000002: "T0836 Modify Parameter",
    9000003: "T0855 Unauthorized Command Message",
}

SCENARIOS = {
    "scan": {
        "title": "Register scan",
        "description": "Reads registers from several unit IDs in a short burst.",
        "technique": "T0846 Remote System Discovery",
        "sid": 9000001,
    },
    "write": {
        "title": "Setpoint change",
        "description": "Writes 95 to the chlorine dosing setpoint (normal value is 20).",
        "technique": "T0836 Modify Parameter",
        "sid": 9000002,
    },
    "flood": {
        "title": "Write flood",
        "description": "Sends 60 write commands to the inlet valve in a few seconds.",
        "technique": "T0855 Unauthorized Command Message",
        "sid": 9000003,
    },
}

last_run = {}  # scenario id -> epoch seconds


def client():
    c = ModbusTcpClient(TARGET, port=502, timeout=3)
    c.connect()
    return c


def run_scan():
    c = client()
    for unit in range(1, 6):
        for addr in (0, 10, 20):
            c.read_holding_registers(addr, 4, slave=unit)
    c.close()


def run_write():
    c = client()
    c.write_register(3, 95, slave=1)
    c.close()


def run_flood():
    c = client()
    for i in range(60):
        c.write_register(2, i % 100, slave=1)
    c.close()


def run_restore():
    c = client()
    c.write_register(2, 40, slave=1)
    c.write_register(3, 20, slave=1)
    c.close()


RUNNERS = {"scan": run_scan, "write": run_write, "flood": run_flood, "restore": run_restore}


def read_alerts(limit=200):
    """Return the newest alerts from Suricata's eve.json (newest first)."""
    if not os.path.exists(EVE_LOG):
        return []
    size = os.path.getsize(EVE_LOG)
    with open(EVE_LOG, "rb") as f:
        f.seek(max(0, size - 600_000))
        lines = f.read().decode("utf-8", "ignore").splitlines()
    alerts = []
    for line in reversed(lines):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("event_type") != "alert":
            continue
        a = e["alert"]
        try:
            epoch = datetime.strptime(e["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
        except (KeyError, ValueError):
            continue
        alerts.append({
            "time": epoch,
            "sid": a.get("signature_id"),
            "signature": a.get("signature"),
            "technique": SIGNATURES.get(a.get("signature_id"), ""),
            "src": e.get("src_ip"),
            "dest": f'{e.get("dest_ip")}:{e.get("dest_port")}',
        })
        if len(alerts) >= limit:
            break
    return alerts


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/state")
def state():
    try:
        c = client()
        r = c.read_holding_registers(0, 4, slave=1)
        c.close()
        if r.isError():
            raise RuntimeError("Modbus error")
        level, pump, valve, chlorine = r.registers
        return jsonify(ok=True, level=level, pump=pump, valve=valve, chlorine=chlorine)
    except Exception:
        return jsonify(ok=False)


@app.get("/api/alerts")
def alerts():
    return jsonify(alerts=read_alerts(60), log_found=os.path.exists(EVE_LOG))


@app.get("/api/scenarios")
def scenarios():
    now = time.time()
    all_alerts = read_alerts(200)
    out = []
    for sid, s in SCENARIOS.items():
        t = last_run.get(sid)
        detected = bool(t) and any(
            a["sid"] == s["sid"] and a["time"] >= t - 1 for a in all_alerts
        )
        out.append({"id": sid, **s, "last_run": t, "detected": detected})
    return jsonify(now=now, scenarios=out)


@app.post("/api/run/<name>")
def run(name):
    if name not in RUNNERS:
        return jsonify(ok=False, error="unknown scenario"), 404
    try:
        RUNNERS[name]()
    except Exception as exc:
        return jsonify(ok=False, error=str(exc)), 502
    if name in SCENARIOS:
        last_run[name] = time.time()
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
