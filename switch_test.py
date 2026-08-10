"""
Run this ON THE RASPBERRY PI to test a single microswitch wired to
pin GPA0 of the MCP23017 at address 0x20 (Spieler 1's board).

Wiring for this test:
    switch COM -> GND
    switch NO  -> MCP23017 GPA0

    python switch_test.py

Press the switch — you should see "GEDRÜCKT" print each time.
Change PIN below to test a different pin.
"""

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

ADDRESS = 0x20
PIN = 0  # GPA0

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=ADDRESS)

switch = mcp.get_pin(PIN)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

print(f"Teste Pin {PIN} auf Board 0x{ADDRESS:02X}. Drück den Taster (Strg+C zum Beenden).")

last_state = switch.value  # True = nicht gedrückt (Pull-Up), False = gedrückt
while True:
    state = switch.value
    if state != last_state:
        if not state:
            print("GEDRÜCKT")
        else:
            print("losgelassen")
        last_state = state
    time.sleep(0.02)
