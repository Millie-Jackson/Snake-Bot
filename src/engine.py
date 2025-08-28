"""
src/engine.py
"""


from collections import deque
import random
from dataclasses import dataclass
from typing import Deque, List, Optional, Tuple
from .config import GRID_W, GRID_H


Pos = Tuple[int, int]


def in_bounds(x: int, y: int) -> bool:
    return 0 <= x < GRID_W and 0 <= y < GRID_H


@dataclass
class StepResult:
    alive: bool
    ate: bool
    score: int


class SnakeGame:
    """
    Pure game logic (no rendering). Works for Pygame and Gradio.
    """
    
    def __init__(self, init_len: int = 4):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake: Deque[Pos] = deque([(cx - i, cy) for i in range(init_len)])  # head is last
        self.dir: Pos = (1, 0)
        self.score = 0
        self.food: Optional[Pos] = self._spawn_food()
        self.alive = True
        self.frame = 0

    def _spawn_food(self) -> Optional[Pos]:
        all_cells = {(x, y) for x in range(GRID_W) for y in range(GRID_H)}
        free = list(all_cells - set(self.snake))
        return random.choice(free) if free else None

    @property
    def head(self) -> Pos:
        return self.snake[-1]

    def set_dir(self, dx: int, dy: int) -> None:
        # prevent 180° turns
        if (dx, dy) == (-self.dir[0], -self.dir[1]):
            return
        self.dir = (dx, dy)

    def step(self) -> StepResult:
        if not self.alive:
            return StepResult(False, False, self.score)

        self.frame += 1
        hx, hy = self.head
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        # collisions
        if not in_bounds(nx, ny) or (nx, ny) in self.snake:
            self.alive = False
            return StepResult(False, False, self.score)

        self.snake.append((nx, ny))

        ate = False
        if self.food and (nx, ny) == self.food:
            self.score += 1
            ate = True
            self.food = self._spawn_food()
        else:
            self.snake.popleft()  # move tail

        return StepResult(True, ate, self.score)
