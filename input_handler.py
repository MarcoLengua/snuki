"""
Input abstraction.

The game loop only ever asks an "input provider" for a list of
(player_index, steps) events per frame. Today that's the keyboard.
Later, on the Raspberry Pi, it'll be a provider that reads the three
MCP23017 I/O expanders over I2C and translates a triggered microswitch
into the exact same kind of event — nothing in game_state.py or
renderer.py has to change.
"""

import pygame
from config import KEY_MAPS


class InputProvider:
    """Base interface. Subclasses implement poll()."""

    def poll(self, events):
        """
        events: the list of pygame events collected this frame.
        Returns: list of (player_index, steps) tuples triggered this frame.
        """
        raise NotImplementedError


class KeyboardInputProvider(InputProvider):
    """Maps keydown events to (player_index, steps) using config.KEY_MAPS."""

    def __init__(self, key_maps=None):
        self.key_maps = key_maps if key_maps is not None else KEY_MAPS

    def poll(self, events):
        triggers = []
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            for player_index, mapping in enumerate(self.key_maps):
                if event.key in mapping:
                    steps = mapping[event.key]
                    triggers.append((player_index, steps))
        return triggers


class SensorInputProvider(InputProvider):
    """
    Placeholder for the real hardware.

    Planned implementation (once the MCP23017 boards are wired up):

        import board, busio
        from adafruit_mcp230xx.mcp23017 import MCP23017

        i2c = busio.I2C(board.SCL, board.SDA)
        mcp_per_player = [
            MCP23017(i2c, address=0x20),  # player 0
            MCP23017(i2c, address=0x21),  # player 1
            MCP23017(i2c, address=0x22),  # player 2
        ]
        # each MCP pin -> steps, via the same hole layout as the
        # cardboard template (green=0, blue=1, gelb=2, rot=3)

    poll() would read each MCP's GPIO register once per frame (or react
    to its INT pin), debounce, and emit the same (player_index, steps)
    tuples the keyboard provider emits today.
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "SensorInputProvider is a stub for the hardware build. "
            "Use KeyboardInputProvider until the Pi + MCP23017 wiring is ready."
        )

    def poll(self, events):
        raise NotImplementedError
