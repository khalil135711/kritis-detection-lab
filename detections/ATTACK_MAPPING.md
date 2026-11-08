# Detection to MITRE ATT&CK for ICS mapping

| Detection | Technique | Data source | Status |
|-----------|-----------|-------------|--------|
| Suricata 9000001 read burst | T0846 Remote System Discovery | Network traffic | done |
| Suricata 9000002 single register write | T0836 Modify Parameter | Network traffic | done |
| Suricata 9000003 write flood | T0855 Unauthorized Command Message | Network traffic | done |
| Sigma modbus_unauthorized_write | T0836 | Suricata eve.json | draft |
