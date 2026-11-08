# Monitoring

Suricata runs inside the PLC container's network namespace and writes `eve.json` to `../logs/`.

Next steps: ship `eve.json` to Wazuh or Elastic, and add Zeek with the Modbus analyzer.
