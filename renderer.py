"""
All drawing lives here. Horses are simple shapes (no external image
assets needed to get started) — swap in sprite images later by editing
draw_horse() only.
"""

import pygame
import config


def lane_rect(player_index):
    top = config.TRACK_TOP + player_index * (config.LANE_HEIGHT + 20)
    left = config.TRACK_MARGIN_LEFT
    width = config.SCREEN_W - config.TRACK_MARGIN_LEFT - config.TRACK_MARGIN_RIGHT
    return pygame.Rect(left, top, width, config.LANE_HEIGHT)


def draw_track(screen, num_players, font_label):
    for i in range(num_players):
        rect = lane_rect(i)
        pygame.draw.rect(screen, config.TRACK_COLOR, rect, border_radius=10)
        pygame.draw.rect(screen, config.LINE_COLOR, rect, width=2, border_radius=10)

        # finish line
        finish_x = rect.right - 6
        pygame.draw.line(
            screen, config.FINISH_COLOR,
            (finish_x, rect.top), (finish_x, rect.bottom), 4
        )

        # player label
        label = font_label.render(config.PLAYER_NAMES[i], True, config.TEXT_COLOR)
        screen.blit(label, (20, rect.centery - label.get_height() // 2))


def draw_horse(screen, player_index, fraction, font_small):
    rect = lane_rect(player_index)
    usable_w = rect.width - 60
    x = rect.left + 30 + usable_w * fraction
    y = rect.centery

    color = config.PLAYER_COLORS[player_index]

    # simple horse silhouette: body + neck/head + legs, good enough to
    # read at a glance and easy to replace with a sprite later
    body = pygame.Rect(0, 0, 54, 28)
    body.center = (x, y)
    pygame.draw.ellipse(screen, color, body)

    neck_points = [
        (body.right - 10, body.top + 4),
        (body.right + 16, body.top - 18),
        (body.right + 24, body.top - 6),
        (body.right + 6, body.top + 10),
    ]
    pygame.draw.polygon(screen, color, neck_points)

    head = pygame.Rect(0, 0, 16, 12)
    head.center = (body.right + 22, body.top - 14)
    pygame.draw.ellipse(screen, color, head)

    leg_y0 = body.bottom - 4
    for lx in (body.left + 10, body.left + 34, body.right - 20, body.right - 4):
        pygame.draw.line(screen, color, (lx, leg_y0), (lx, leg_y0 + 16), 5)


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
