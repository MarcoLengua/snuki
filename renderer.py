"""
All drawing lives here.

- Horses: assets/horse_run.png, a 6-frame running sprite sheet.
  HorseAnimator cycles through the frames while a horse is moving.
- Banner: assets/banner.jpg (the DOM Hamburg photo), scaled to the
  window width and shown above the track.
- Track: styled to read as an actual racetrack — dirt lanes, a grass
  margin, white rail dividers between lanes, and a checkered finish line.
"""

import os
import pygame
import config

_ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
_SPRITE_PATH = os.path.join(_ASSET_DIR, "horse_run.png")
_BANNER_PATH = os.path.join(_ASSET_DIR, "banner.jpg")

_SPRITE_FRAME_COUNT = 6
_SPRITE_SCALE = 2.2       # 60x33 source frames -> ~132x73 on screen
_ANIM_FPS = 12             # how fast the legs cycle while moving

_horse_frames = None   # lazy-loaded list[pygame.Surface]
_banner_surface = None  # lazy-loaded pygame.Surface
_banner_height = 130    # updated once the real banner is loaded and scaled

GRASS_COLOR = (86, 138, 72)
DIRT_COLOR = (176, 137, 92)
DIRT_LINE_COLOR = (140, 105, 68)
RAIL_COLOR = (245, 245, 240)
RAIL_POST_COLOR = (90, 65, 40)


def get_horse_frames():
    """
    Loads and slices the sprite sheet once (needs a pygame display /
    video mode to already be initialised, so we can't do this at
    import time). The source sprite faces left; we flip it so the
    horses run rightward, matching the track direction.
    """
    global _horse_frames
    if _horse_frames is not None:
        return _horse_frames

    sheet = pygame.image.load(_SPRITE_PATH).convert_alpha()
    sheet_w, sheet_h = sheet.get_size()
    frame_w = sheet_w // _SPRITE_FRAME_COUNT
    frame_h = sheet_h

    frames = []
    for i in range(_SPRITE_FRAME_COUNT):
        frame = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h)).copy()
        frame = pygame.transform.flip(frame, True, False)  # face right
        scaled = pygame.transform.scale(
            frame, (int(frame_w * _SPRITE_SCALE), int(frame_h * _SPRITE_SCALE))
        )
        frames.append(scaled)

    _horse_frames = frames
    return _horse_frames


def get_banner():
    """Loads + scales the DOM Hamburg banner to the window width once."""
    global _banner_surface, _banner_height
    if _banner_surface is not None:
        return _banner_surface

    img = pygame.image.load(_BANNER_PATH).convert()
    w, h = img.get_size()
    target_w = config.SCREEN_W
    scale = target_w / w
    target_h = max(1, int(h * scale))
    _banner_surface = pygame.transform.smoothscale(img, (target_w, target_h))
    _banner_height = target_h
    return _banner_surface


def get_track_top():
    """Where the racetrack starts, i.e. just below the banner."""
    get_banner()
    return _banner_height + 18


class HorseAnimator:
    """Per-horse animation state: which frame to show right now."""

    def __init__(self):
        self.frame_index = 0
        self.timer = 0.0

    def update(self, dt, moving):
        if not moving:
            self.frame_index = 0  # standing frame while idle
            self.timer = 0.0
            return
        self.timer += dt
        frame_duration = 1.0 / _ANIM_FPS
        while self.timer >= frame_duration:
            self.timer -= frame_duration
            self.frame_index = (self.frame_index + 1) % _SPRITE_FRAME_COUNT


def lane_rect(player_index):
    top = get_track_top() + player_index * (config.LANE_HEIGHT + 20)
    left = config.TRACK_MARGIN_LEFT
    width = config.SCREEN_W - config.TRACK_MARGIN_LEFT - config.TRACK_MARGIN_RIGHT
    return pygame.Rect(left, top, width, config.LANE_HEIGHT)


def draw_banner(screen):
    banner = get_banner()
    screen.blit(banner, (0, 0))
    # thin dark frame line under the banner to separate it from the track
    pygame.draw.line(screen, (30, 25, 20), (0, _banner_height), (config.SCREEN_W, _banner_height), 2)


def _draw_checkered_finish(screen, rect, square=8):
    """A black/white checkerboard strip at the right end of a lane."""
    strip_w = square * 2
    x0 = rect.right - strip_w
    cols = 2
    rows = max(1, rect.height // square)
    for row in range(rows):
        for col in range(cols):
            color = (20, 20, 20) if (row + col) % 2 == 0 else (245, 245, 245)
            r = pygame.Rect(x0 + col * square, rect.top + row * square, square, square)
            r = r.clip(rect)
            if r.width > 0 and r.height > 0:
                pygame.draw.rect(screen, color, r)


def draw_track(screen, num_players, font_label):
    if num_players == 0:
        return

    first = lane_rect(0)
    last = lane_rect(num_players - 1)
    enclosure = pygame.Rect(
        first.left - 26, first.top - 22,
        first.width + 52, (last.bottom - first.top) + 44
    )

    # grass margin behind everything
    pygame.draw.rect(screen, GRASS_COLOR, enclosure, border_radius=16)

    # outer rail (wood post look): dark border + inner white rail line
    pygame.draw.rect(screen, RAIL_POST_COLOR, enclosure, width=6, border_radius=16)
    inner = enclosure.inflate(-10, -10)
    pygame.draw.rect(screen, RAIL_COLOR, inner, width=3, border_radius=12)

    for i in range(num_players):
        rect = lane_rect(i)

        # dirt lane surface
        pygame.draw.rect(screen, DIRT_COLOR, rect)
        # a few horizontal "raked dirt" texture lines
        for ty in range(rect.top + 14, rect.bottom - 6, 16):
            pygame.draw.line(screen, DIRT_LINE_COLOR, (rect.left + 8, ty), (rect.right - 8, ty), 1)

        # white rail dividing this lane from the next one
        if i > 0:
            pygame.draw.line(screen, RAIL_COLOR, (rect.left - 13, rect.top), (rect.right + 13, rect.top), 3)
            for px in range(rect.left, rect.right, 60):
                pygame.draw.line(screen, RAIL_POST_COLOR, (px, rect.top - 3), (px, rect.top + 3), 2)

        # checkered finish line
        _draw_checkered_finish(screen, rect)

        # starting gate posts at the left edge
        for gx in (rect.left + 4, rect.left + 12):
            pygame.draw.line(screen, RAIL_POST_COLOR, (gx, rect.top + 4), (gx, rect.bottom - 4), 3)

        # player label, on the grass to the left of the lane
        label = font_label.render(config.PLAYER_NAMES[i], True, (255, 255, 255))
        shadow = font_label.render(config.PLAYER_NAMES[i], True, (0, 0, 0))
        label_pos = (enclosure.left + 12, rect.centery - label.get_height() // 2)
        screen.blit(shadow, (label_pos[0] + 1, label_pos[1] + 1))
        screen.blit(label, label_pos)


def draw_horse(screen, player_index, fraction, animator):
    """Draws the sprite-based horse plus a small colored flag so
    players stay easy to tell apart (the sprite itself is the same
    horse for everyone)."""
    rect = lane_rect(player_index)
    usable_w = rect.width - 90
    x = rect.left + 30 + usable_w * fraction
    y = rect.bottom - 12  # feet roughly on the "ground" line of the lane

    frames = get_horse_frames()
    frame = frames[animator.frame_index]
    frame_rect = frame.get_rect(midbottom=(x, y))

    # soft shadow under the horse for a bit of depth
    shadow = pygame.Surface((frame_rect.width * 0.7, 14), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 70), shadow.get_rect())
    screen.blit(shadow, shadow.get_rect(center=(frame_rect.centerx, frame_rect.bottom - 4)))

    screen.blit(frame, frame_rect)

    # player-colour flag above the horse
    color = config.PLAYER_COLORS[player_index]
    flag_x = frame_rect.centerx
    flag_top = frame_rect.top - 22
    pygame.draw.line(screen, (70, 60, 50), (flag_x, flag_top), (flag_x, frame_rect.top - 2), 2)
    pygame.draw.polygon(
        screen, color,
        [(flag_x, flag_top), (flag_x + 16, flag_top + 5), (flag_x, flag_top + 10)]
    )


def draw_hud(screen, race_state, font_small):
    y = config.SCREEN_H - 40
    parts = []
    for i, pos in enumerate(race_state.positions):
        parts.append(f"{config.PLAYER_NAMES[i]}: {pos}/{config.TRACK_LENGTH}")
    text = "   |   ".join(parts)
    label = font_small.render(text, True, config.TEXT_COLOR)
    screen.blit(label, (config.TRACK_MARGIN_LEFT, y))

    hint = "R = Neustart   |   ESC = Beenden"
    hint_label = font_small.render(hint, True, (140, 130, 110))
    screen.blit(hint_label, (config.TRACK_MARGIN_LEFT, y + 22))


def draw_win_screen(screen, winner_name, winner_index, font_big, font_small):
    overlay = pygame.Surface((config.SCREEN_W, config.SCREEN_H), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 210))
    screen.blit(overlay, (0, 0))

    color = config.PLAYER_COLORS[winner_index]
    title = font_big.render(f"{winner_name} gewinnt!", True, color)
    title_rect = title.get_rect(center=(config.SCREEN_W // 2, config.SCREEN_H // 2 - 20))
    screen.blit(title, title_rect)

    hint = font_small.render("Leertaste oder R für ein neues Rennen", True, config.TEXT_COLOR)
    hint_rect = hint.get_rect(center=(config.SCREEN_W // 2, config.SCREEN_H // 2 + 40))
    screen.blit(hint, hint_rect)
