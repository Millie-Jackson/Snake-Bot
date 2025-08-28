"""
src/game.py
"""


import pygame, sys
from .config import GRID_W, GRID_H, CELL, FPS, DIRS
from .engine import SnakeGame
from .ai import choose_move
from .render_pygame import draw_all


AI_AUTOPLAY = True


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_W*CELL, GRID_H*CELL))
    pygame.display.set_caption("Snake-Bot")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    game = SnakeGame()
    running = True

    while running and game.alive:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if not AI_AUTOPLAY and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:    game.set_dir(*DIRS["UP"])
                if e.key == pygame.K_DOWN:  game.set_dir(*DIRS["DOWN"])
                if e.key == pygame.K_LEFT:  game.set_dir(*DIRS["LEFT"])
                if e.key == pygame.K_RIGHT: game.set_dir(*DIRS["RIGHT"])

        if AI_AUTOPLAY:
            mv = choose_move(game)
            if mv is None:
                break
            game.set_dir(*mv)

        result = game.step()
        draw_all(screen, game, font, result.score)
        pygame.display.flip()
        clock.tick(FPS)

    # quick exit screen
    pygame.time.wait(800)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
