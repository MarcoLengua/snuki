"""
Run this ON THE RASPBERRY PI to confirm the MCP23017 boards answer on
the I2C bus, using the same library the real game will use (so a
success here means the game's SensorInputProvider will find them too).

    python i2c_scan.py

Expected output once wired correctly:
    0x20: OK
    0x21: OK
    0x22: OK   (once you've wired the 3rd board)
"""

import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

ADDRESSES = [0x20, 0x21, 0x22]

i2c = busio.I2C(board.SCL, board.SDA)

for addr in ADDRESSES:
    try:
        mcp = MCP23017(i2c, address=addr)
        # touch a register to force real communication, not just an ack
        _ = mcp.gpio
        print(f"0x{addr:02X}: OK")
    except Exception as e:
        print(f"0x{addr:02X}: NOT FOUND ({e})")
