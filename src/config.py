"""
src/config.py

Grid + visual config kept here to reuse in Pygame + Gradio renderers.
"""
 

CELL = 24
GRID_W, GRID_H = 24, 18 # logical grid size
FPS = 14

# RGB tuples for Pygame; also reused by PIL
BG = (18, 18, 24)
GRID = (32, 32, 40)
SNAKE = (64, 200, 130)
HEAD = (80, 230, 160)
FOOD = (240, 90, 90)
TEXT = (200, 200, 210)

DIRS = {
    "UP":    (0, -1),
    "DOWN":  (0,  1),
    "LEFT":  (-1, 0),
    "RIGHT": (1,  0),
}
