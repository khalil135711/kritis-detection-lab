# KRITIS Detection Lab

A small, fully local lab that simulates a **water treatment plant (OT/ICS)** and shows how a
SOC / Blue Team can **detect attacks on Modbus/TCP**. Built as a portfolio project for
critical infrastructure (KRITIS) and NIS2 contexts.

> **Scope:** Everything runs locally in Docker on an isolated network. The attack scripts only
> target the simulator in this repo. Never run them against systems you do not own.

## Architecture

```
 browser ──▶ dashboard (GUI, :8080) ──Modbus/TCP 502──▶ plc-sim (fake water plant)
                  │  ▲                                      ▲
                  │  └──── reads logs/eve.json              │ shared network namespace
                  │                                    suricata (IDS) ──▶ logs/eve.json
                  └── runs the attack scenarios (lab only)
```

## Quick start

```bash
docker compose up --build -d
```

Open **http://localhost:8080**. You will see the plant live, can run the three attack
scenarios with one click, and watch the Suricata alerts and ATT&CK techniques appear.
Each scenario shows whether its expected rule fired.

CLI alternative (no GUI):

```bash
docker compose run --rm attacker python scan.py
docker compose run --rm attacker python unauthorized_write.py
python3 monitoring/alert_viewer.py logs/eve.json
```

## Scenarios

| # | Scenario | Script | Detection | ATT&CK for ICS |
|---|----------|--------|-----------|----------------|
| 1 | Modbus device/register scanning | `attacks/scan.py` | Suricata sid 9000001 | T0846 Remote System Discovery |
| 2 | Unauthorized register write (setpoint change) | `attacks/unauthorized_write.py` | Suricata sid 9000002, Sigma rule | T0836 Modify Parameter |
| 3 | Write flood / replay | `attacks/write_flood.py` | Suricata sid 9000003 (threshold) | T0855 Unauthorized Command Message |

## Repo layout

- `ot-sim/` – Python Modbus/TCP simulator (tank level, pump, valve)
- `dashboard/` – web GUI (Flask): live plant view, scenario buttons, alert feed
- `monitoring/` – Suricata config notes, alert viewer
- `detections/` – Suricata and Sigma rules, ATT&CK mapping
- `attacks/` – scripted attack scenarios
- `reports/` – incident report template + example (KRITIS/NIS2 style)
- `docs/` – threat model, NIS2 / KRITIS notes, roadmap

## Roadmap

- [ ] Add Wazuh or Elastic as SIEM and ship `eve.json`
- [ ] Add Zeek with the Modbus analyzer
- [ ] Add OpenPLC as a second, more realistic target
- [ ] Add replay scenario and more ATT&CK for ICS techniques
- [ ] Add a screenshot or demo GIF of the GUI at the top of this README

## License

MIT
