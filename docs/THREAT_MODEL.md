# Threat model (simplified)

**Assets:** PLC (tank level, pump, valve, chlorine dosing), engineering workstation, monitoring.

**Assumptions:** Modbus/TCP has no authentication or encryption. Anyone with network access can read and write.

**Threats:**
1. Reconnaissance of devices and registers
2. Unauthorized modification of process parameters
3. Command flooding / denial of service
4. Replay of captured commands

**Mitigations:** segmentation (IT/OT), allow-listed Modbus clients, function-code filtering, IDS monitoring, alert triage playbooks.
