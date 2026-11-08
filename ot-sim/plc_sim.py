"""Tiny simulated water plant exposed via Modbus/TCP (port 502).

Holding registers:
  0 = tank level (0-100 %)
  1 = pump setpoint (0 = off, 1 = on)
  2 = inlet valve position (0-100 %)
  3 = chlorine dosing setpoint (0-100)
"""
import threading
import time

from pymodbus.datastore import (ModbusSequentialDataBlock, ModbusServerContext,
                                ModbusSlaveContext)
from pymodbus.server import StartTcpServer

store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [50, 1, 40, 20] + [0] * 96))
context = ModbusServerContext(slaves=store, single=True)


def process_loop():
    """Very simple physics: tank fills with valve, drains with pump."""
    while True:
        level, pump, valve, _ = store.getValues(3, 0, count=4)
        level += (valve // 20) - (3 if pump else 0)
        level = max(0, min(100, level))
        store.setValues(3, 0, [level])
        time.sleep(2)


if __name__ == "__main__":
    threading.Thread(target=process_loop, daemon=True).start()
    print("PLC simulator listening on 0.0.0.0:502")
    StartTcpServer(context=context, address=("0.0.0.0", 502))
