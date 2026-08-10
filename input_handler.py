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
    Reads the real cardboard-hole microswitches via the 3 MCP23017
    boards (one per player). Same output shape as KeyboardInputProvider:
    poll() returns a list of (player_index, steps) tuples.

    Must run on the Raspberry Pi with I2C enabled and the boards wired
    per hardware/README_HARDWARE.md. The adafruit libraries are only
    imported here (not at module load time), so this file still imports
    fine on a regular PC where those libraries aren't installed.
    """

    def __init__(self, mcp_addresses=None, pin_maps=None,
                 debounce_seconds=None):
        import board
        import busio
        import digitalio
        from adafruit_mcp230xx.mcp23017 import MCP23017
        import config
        import time

        self._digitalio = digitalio
        self._time = time

        mcp_addresses = mcp_addresses or config.MCP_ADDRESSES
        pin_maps = pin_maps or config.PLAYER_PIN_MAP
        self.debounce_seconds = (
            debounce_seconds if debounce_seconds is not None
            else config.SWITCH_DEBOUNCE_SECONDS
        )

        i2c = busio.I2C(board.SCL, board.SDA)

        # one MCP23017 per player that actually has a pin map configured
        self.boards = []
        self.pin_objects = []   # per player: list of (digital_pin, steps)
        self.last_state = []    # per player: list of last-read bool
        self.last_trigger_time = []  # per player: list of last-trigger timestamps

        for player_index, pin_map in enumerate(pin_maps):
            addr = mcp_addresses[player_index]
            mcp = MCP23017(i2c, address=addr)
            self.boards.append(mcp)

            pins_for_player = []
            states_for_player = []
            times_for_player = []
            for pin_number, steps in pin_map:
                p = mcp.get_pin(pin_number)
                p.direction = digitalio.Direction.INPUT
                p.pull = digitalio.Pull.UP
                pins_for_player.append((p, steps))
                states_for_player.append(True)  # True = not pressed (pull-up)
                times_for_player.append(0.0)

            self.pin_objects.append(pins_for_player)
            self.last_state.append(states_for_player)
            self.last_trigger_time.append(times_for_player)

    def poll(self, events):
        """
        Ignores the pygame `events` argument (kept for interface
        compatibility with KeyboardInputProvider) and instead reads the
        current state of every configured switch.
        """
        triggers = []
        now = self._time.monotonic()

        for player_index, pins_for_player in enumerate(self.pin_objects):
            for i, (pin_obj, steps) in enumerate(pins_for_player):
                state = pin_obj.value  # True = released, False = pressed
                was_pressed = not self.last_state[player_index][i]
                is_pressed = not state

                if is_pressed and not was_pressed:
                    # rising edge into "pressed" — debounce
                    last_t = self.last_trigger_time[player_index][i]
                    if now - last_t >= self.debounce_seconds:
                        triggers.append((player_index, steps))
                        self.last_trigger_time[player_index][i] = now

                self.last_state[player_index][i] = state

        return triggers
