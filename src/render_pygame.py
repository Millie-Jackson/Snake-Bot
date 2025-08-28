"""
src/render_pygame.py
"""


import pygame
from .config import CELL, GRID_W, GRID_H, BG, GRID, SNAKE, HEAD, FOOD, TEXT


def draw_grid(surface):
    for x in range(GRID_W):
        pygame.draw.line(surface, GRID, (x*CELL, 0), (x*CELL, GRID_H*CELL), 1)
    for y in range(GRID_H):
        pygame.draw.line(surface, GRID, (0, y*CELL), (GRID_W*CELL, y*CELL), 1)

def draw_all(surface, game, font, score):
    surface.fill(BG)
    draw_grid(surface)
    # snake
    for (x, y) in list(game.snake)[:-1]:
        pygame.draw.rect(surface, SNAKE, pygame.Rect(x*CELL, y*CELL, CELL, CELL), border_radius=5)
    hx, hy = game.head
    pygame.draw.rect(surface, HEAD, pygame.Rect(hx*CELL, hy*CELL, CELL, CELL), border_radius=6)
    # food
    if game.food:
        fx, fy = game.food
        pygame.draw.rect(surface, FOOD, pygame.Rect(fx*CELL+3, fy*CELL+3, CELL-6, CELL-6), border_radius=6)
    hud = font.render(f"Score: {score}", True, TEXT)
    surface.blit(hud, (8, 8))
