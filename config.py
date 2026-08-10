"""
Central configuration for SNUKI.

This is the only file you should need to touch to add the 3rd player
later, retune colors, or change the track length. Keyboard mappings here
are the "software-only" stand-in for the real cardboard sensors — later,
input_handler.py gets a SensorInputProvider that emits the exact same
(player_index, steps) events, so nothing else in the game needs to change.
"""

import pygame

# ---------------------------------------------------------------------
# Players
# ---------------------------------------------------------------------
# Add a 3rd entry here (and a key mapping below) when you're ready to
# test with three players. Everything else (rendering, race logic,
# win detection) already loops over however many players are defined.
PLAYER_NAMES = ["Valeria", "Adriana"]
PLAYER_COLORS = [
    (209, 53, 43),   # red
    (43, 61, 143),   # blue
    (43, 143, 74),   # green — reserved for player 3
]

# ---------------------------------------------------------------------
# Keyboard input (temporary stand-in for the real hole sensors)
# ---------------------------------------------------------------------
# Each player gets 4 keys mapped to the 4 possible outcomes: 0/1/2/3
# steps, exactly like the four hole colors on the cardboard board
# (green=0, blue=1, gelb=2, rot=3).
#
# Player 1: Q W E D  -> 0 1 2 3
# Player 2: I O P Ü  -> 0 1 2 3
#
# NOTE on the Ü key: pygame's keycodes are US-layout based, and there is
# no dedicated K_UE constant. On most systems the physical key where Ü
# sits (next to P) reports as pygame.K_LEFTBRACKET regardless of your
# configured keyboard layout. If that doesn't trigger for you, run
# key_probe.py (included) to see what keycode your key actually sends,
# and edit the mapping below.
KEY_MAPS = [
    {  # Player 1 (index 0)
        pygame.K_a: 0,
        pygame.K_s: 1,
        pygame.K_d: 2,
        pygame.K_f: 3,
    },
    {  # Player 2 (index 1)
        pygame.K_v: 0,
        pygame.K_b: 1,
        pygame.K_n: 2,
        pygame.K_m: 3,
    },
    # Player 3 (index 2) — uncomment and pick free keys when you add
    # a third player:
    # {
    #     pygame.K_KP7: 0,
    #     pygame.K_KP8: 1,
    #     pygame.K_KP9: 2,
    #     pygame.K_KP_PLUS: 3,
    # },
]

# ---------------------------------------------------------------------
# Race track
# ---------------------------------------------------------------------
TRACK_LENGTH = 20        # steps needed to win
STEP_ANIM_SECONDS = 0.35  # how long the horse takes to glide to its new spot

# ---------------------------------------------------------------------
# Window / layout
# ---------------------------------------------------------------------
SCREEN_W, SCREEN_H = 1000, 660
FPS = 60

TRACK_MARGIN_LEFT = 160
TRACK_MARGIN_RIGHT = 60
# Where the track starts vertically is now computed at runtime from the
# banner image's scaled height — see renderer.get_track_top().
LANE_HEIGHT = 110

BG_COLOR = (250, 246, 230)
TRACK_COLOR = (222, 210, 180)
LINE_COLOR = (120, 110, 90)
TEXT_COLOR = (40, 35, 25)
FINISH_COLOR = (200, 40, 40)

# ---------------------------------------------------------------------
# Hardware: MCP23017 boards + microswitches
# ---------------------------------------------------------------------
# One MCP23017 per player, addresses set via the A0/A1/A2 pins on the
# HW-839 boards (see hardware/README_HARDWARE.md).
MCP_ADDRESSES = [0x20, 0x21, 0x22]

# Which MCP23017 pin (0-15, i.e. GPA0..GPA7=0..7, GPB0..GPB7=8..15)
# corresponds to which hole, and how many steps that hole is worth.
# Same point values as the cardboard template: rot=3, gelb=2, blau=1.
# Pin numbers here are just an assignment order — wire them to whichever
# physical hole is convenient, then note it down here so it matches.
PLAYER_PIN_MAP = [
    # Player 1 (board 0x20)
    [
        (0, 3), (1, 3),                          # 2x rot
        (2, 2), (3, 2), (4, 2), (5, 2),           # 4x gelb
        (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1),  # 7x blau
    ],
    # Player 2 (board 0x21) — same pin layout, different board
    [
        (0, 3), (1, 3),
        (2, 2), (3, 2), (4, 2), (5, 2),
        (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1),
    ],
    # Player 3 (board 0x22) — uncomment once wired
    # [
    #     (0, 3), (1, 3),
    #     (2, 2), (3, 2), (4, 2), (5, 2),
    #     (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1),
    # ],
]

SWITCH_DEBOUNCE_SECONDS = 0.05

