"""
src/ai.py
"""


from collections import deque
from typing import Iterable, List, Optional, Tuple, Set
from .config import DIRS, GRID_W, GRID_H
from .engine import SnakeGame, Pos


def neighbors(x: int, y: int) -> Iterable[Pos]:
    for dx, dy in DIRS.values():
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
            yield (nx, ny)

def bfs_path(start: Pos, goal: Pos, blocked: Set[Pos]) -> Optional[List[Pos]]:
    q = deque([start])
    came = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = came[cur]
            return list(reversed(path))
        for nxt in neighbors(*cur):
            if nxt not in came and nxt not in blocked:
                came[nxt] = cur
                q.append(nxt)
    return None

def safe_moves(head: Pos, body: List[Pos]) -> List[Tuple[int,int]]:
    hx, hy = head
    body_set = set(body[:-1])  # tail cell frees next frame
    goods = []
    for dx, dy in DIRS.values():
        nx, ny = hx + dx, hy + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in body_set:
            goods.append((dx, dy))
    return goods

def choose_move(game: SnakeGame) -> Optional[Tuple[int,int]]:
    head = game.head
    food = game.food
    if food is None:
        # board filled – arbitrary
        return (0, 1)

    blocked = set(list(game.snake)[:-1])
    path = bfs_path(head, food, blocked)
    if path and len(path) >= 2:
        nx, ny = path[1]
        return (nx - head[0], ny - head[1])

    # Fallback: any safe move; tiny heuristic to keep space
    candidates = safe_moves(head, list(game.snake))
    if not candidates:
        return None
    # Prefer moves that increase Manhattan distance from walls slightly
    def score(mv):
        nx, ny = head[0] + mv[0], head[1] + mv[1]
        margin = min(nx, GRID_W-1-nx, ny, GRID_H-1-ny)
        return margin
    candidates.sort(key=score, reverse=True)
    return candidates[0]
