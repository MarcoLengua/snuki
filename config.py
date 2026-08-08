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
PLAYER_NAMES = ["Spieler 1", "Spieler 2"]
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
        pygame.K_q: 0,
        pygame.K_w: 1,
        pygame.K_e: 2,
        pygame.K_d: 3,
    },
    {  # Player 2 (index 1)
        pygame.K_i: 0,
        pygame.K_o: 1,
        pygame.K_p: 2,
        pygame.K_LEFTBRACKET: 3,  # physical "Ü" key on many layouts
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
SCREEN_W, SCREEN_H = 1000, 600
FPS = 60

TRACK_MARGIN_LEFT = 160
TRACK_MARGIN_RIGHT = 60
TRACK_TOP = 120
LANE_HEIGHT = 110

BG_COLOR = (250, 246, 230)
TRACK_COLOR = (222, 210, 180)
LINE_COLOR = (120, 110, 90)
TEXT_COLOR = (40, 35, 25)
FINISH_COLOR = (200, 40, 40)
