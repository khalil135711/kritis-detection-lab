"""Scenario 1: enumerate unit IDs and read registers (reconnaissance). LAB USE ONLY."""
import os
from pymodbus.client import ModbusTcpClient

target = os.getenv("TARGET", "plc-sim")
client = ModbusTcpClient(target, port=502)
client.connect()
for unit in range(1, 6):
    for addr in (0, 10, 20):
        r = client.read_holding_registers(addr, 4, slave=unit)
        print(f"unit={unit} addr={addr} ->", getattr(r, "registers", "error"))
client.close()
