"""
Tiny helper: press any key and see what pygame constant/name it reports.
Useful mainly for the Ü key (and any other non-US-layout key) since
pygame keycodes don't always match what's printed on your keycap.

Run:  python key_probe.py
Press keys, watch the console. ESC to quit.
"""

import pygame

pygame.init()
pygame.display.set_mode((400, 120))
pygame.display.set_caption("Key probe — press keys, check the console")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            name = pygame.key.name(event.key)
            print(f"key={event.key}  pygame.K_{name.upper()}  unicode={event.unicode!r}")

pygame.quit()
