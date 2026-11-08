"""Scenario 3: repeated writes in a short time. LAB USE ONLY."""
import os
from pymodbus.client import ModbusTcpClient

target = os.getenv("TARGET", "plc-sim")
client = ModbusTcpClient(target, port=502)
client.connect()
for i in range(60):
    client.write_register(2, i % 100, slave=1)
print("Sent 60 write requests")
client.close()
