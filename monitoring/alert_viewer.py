"""Print Suricata alerts from eve.json in a compact form.
Usage: python3 monitoring/alert_viewer.py logs/eve.json
"""
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "logs/eve.json"
with open(path) as f:
    for line in f:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("event_type") == "alert":
            a = e["alert"]
            print(f'{e["timestamp"]}  sid={a["signature_id"]}  {a["signature"]}  '
                  f'{e.get("src_ip")} -> {e.get("dest_ip")}:{e.get("dest_port")}')
