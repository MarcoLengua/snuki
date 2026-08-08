"""
Race state: how far along the track each horse is, and win detection.
Pure game logic, no pygame/drawing here — keeps it easy to unit test
and easy to reuse once the real sensors drive it instead of the keyboard.
"""

from config import PLAYER_NAMES, TRACK_LENGTH


class RaceState:
    def __init__(self, num_players=None):
        self.num_players = num_players or len(PLAYER_NAMES)
        self.positions = [0] * self.num_players
        self.finished = False
        self.winner = None

    def apply_trigger(self, player_index, steps):
        """Advance a horse. Ignored once the race is over."""
        if self.finished:
            return
        if not (0 <= player_index < self.num_players):
            return
        self.positions[player_index] += steps
        if self.positions[player_index] >= TRACK_LENGTH:
            self.positions[player_index] = TRACK_LENGTH
            self.finished = True
            self.winner = player_index

    def progress_fraction(self, player_index):
        """0.0 .. 1.0 how far that horse is along the track."""
        return min(self.positions[player_index] / TRACK_LENGTH, 1.0)

    def reset(self):
        self.positions = [0] * self.num_players
        self.finished = False
        self.winner = None

    def winner_name(self):
        if self.winner is None:
            return None
        return PLAYER_NAMES[self.winner]
