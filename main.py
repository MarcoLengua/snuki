"""
SNUKI - keyboard prototype / hardware runner

Player 1: Q W E D  -> 0 / 1 / 2 / 3 steps
Player 2: I O P Ü  -> 0 / 1 / 2 / 3 steps

Run with keyboard (default):   python main.py
Run with real sensors (on Pi): python main.py --hardware
"""

import sys
import pygame
import config
from game_state import RaceState
from input_handler import KeyboardInputProvider
from renderer import draw_banner, draw_track, draw_horse, draw_hud, draw_win_screen, HorseAnimator


def make_input_provider():
    if "--hardware" in sys.argv:
        from input_handler import SensorInputProvider
        print("Starte mit Sensor-Input (MCP23017)...")
        return SensorInputProvider()
    print("Starte mit Tastatur-Input.")
    return KeyboardInputProvider()


def main():
    pygame.init()
    pygame.display.set_caption("SNUKI")
    screen = pygame.display.set_mode((config.SCREEN_W, config.SCREEN_H))
    clock = pygame.time.Clock()

    font_label = pygame.font.SysFont("arial", 22, bold=True)
    font_small = pygame.font.SysFont("arial", 18)
    font_big = pygame.font.SysFont("arial", 48, bold=True)

    num_players = len(config.PLAYER_NAMES)
    race = RaceState(num_players)
    input_provider = make_input_provider()

    # smoothed on-screen fraction per horse, separate from the logical
    # position so a jump from e.g. 2 to 5 steps glides instead of teleporting
    display_fraction = [0.0] * num_players
    target_fraction = [0.0] * num_players
    animators = [HorseAnimator() for _ in range(num_players)]

    running = True
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    race.reset()
                    display_fraction = [0.0] * num_players
                    target_fraction = [0.0] * num_players
                    animators = [HorseAnimator() for _ in range(num_players)]
                elif event.key == pygame.K_SPACE and race.finished:
                    race.reset()
                    display_fraction = [0.0] * num_players
                    target_fraction = [0.0] * num_players
                    animators = [HorseAnimator() for _ in range(num_players)]

        if not race.finished:
            triggers = input_provider.poll(events)
            for player_index, steps in triggers:
                race.apply_trigger(player_index, steps)

        for i in range(num_players):
            target_fraction[i] = race.progress_fraction(i)

        # smooth toward target
        smoothing = min(dt / max(config.STEP_ANIM_SECONDS, 0.001), 1.0)
        for i in range(num_players):
            display_fraction[i] += (target_fraction[i] - display_fraction[i]) * smoothing

        moving_epsilon = 0.001
        for i in range(num_players):
            moving = abs(target_fraction[i] - display_fraction[i]) > moving_epsilon
            animators[i].update(dt, moving)

        screen.fill(config.BG_COLOR)
        draw_banner(screen)
        draw_track(screen, num_players, font_label)
        for i in range(num_players):
            draw_horse(screen, i, display_fraction[i], animators[i])
        draw_hud(screen, race, font_small)

        if race.finished:
            draw_win_screen(screen, race.winner_name(), race.winner, font_big, font_small)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
