"""
Sound effects.

- galop.mp3 plays for up to 2 seconds whenever a horse takes a step
  (i.e. right when a trigger is applied), on its own dedicated channel
  per player so two horses moving at once don't cut each other's sound off.
- final.mp3 plays once, on a separate channel, the moment a horse
  crosses the finish line.

Drop your own galop.mp3 / final.mp3 into assets/ — this module fails
gracefully (prints a warning, game keeps running silently) if the
files are missing or no audio device is available, e.g. when testing
on a machine/VM without sound.
"""

import os
import pygame
import config

_ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
_GALOP_PATH = os.path.join(_ASSET_DIR, "galop.mp3")
_FINAL_PATH = os.path.join(_ASSET_DIR, "final.mp3")

GALOP_DURATION_MS = 2000

# Reserve one mixer channel per possible player for the galop sound,
# and one extra channel (right after) for the finish sound so it never
# gets stolen by a galop retrigger.
_MAX_PLAYERS = 4
_FINAL_CHANNEL_ID = _MAX_PLAYERS

_mixer_ready = False
_galop_sound = None
_final_sound = None
_warned = set()


def _warn_once(key, message):
    if key not in _warned:
        print(f"[audio] {message}")
        _warned.add(key)


def init():
    """Call once after pygame.init(). Safe to call multiple times."""
    global _mixer_ready
    if _mixer_ready:
        return
    try:
        pygame.mixer.init()
        pygame.mixer.set_num_channels(max(8, _MAX_PLAYERS + 1))
        _mixer_ready = True
    except pygame.error as e:
        _warn_once("mixer_init", f"Kein Audio verfügbar, Spiel läuft stumm ({e})")


def _load(path, cache_attr):
    global _galop_sound, _final_sound
    if not _mixer_ready:
        return None
    current = globals()[cache_attr]
    if current is not None:
        return current
    if not os.path.isfile(path):
        _warn_once(path, f"Sounddatei fehlt: {path} — lege sie in assets/ ab.")
        return None
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error as e:
        _warn_once(path, f"Konnte {path} nicht laden ({e})")
        return None
    globals()[cache_attr] = sound
    return sound


def get_galop_sound():
    return _load(_GALOP_PATH, "_galop_sound")


def get_final_sound():
    return _load(_FINAL_PATH, "_final_sound")


def play_galop(player_index):
    """Plays galop.mp3 for up to GALOP_DURATION_MS on this player's
    dedicated channel. Re-triggering (another step before the 2s are up)
    just restarts it, which is the desired 'still galloping' feel."""
    if not _mixer_ready:
        return
    sound = get_galop_sound()
    if sound is None:
        return
    channel_id = player_index % _MAX_PLAYERS
    pygame.mixer.Channel(channel_id).play(sound, maxtime=GALOP_DURATION_MS)


def play_final():
    """Plays final.mp3 once, stopping any galop sounds first so it's
    clearly audible."""
    if not _mixer_ready:
        return
    sound = get_final_sound()
    if sound is None:
        return
    for i in range(_MAX_PLAYERS):
        pygame.mixer.Channel(i).stop()
    pygame.mixer.Channel(_FINAL_CHANNEL_ID).play(sound)
