"""
src/app/py

Gradio-based viewer that renders each frame to a PIL image.
This runs in a browser on Hugging Face Spaces (no desktop window).
"""


from typing import Tuple
import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .config import CELL, GRID_W, GRID_H, BG, GRID, SNAKE, HEAD, FOOD, DIRS, FPS
from .engine import SnakeGame
from .ai import choose_move


W, H = GRID_W*CELL, GRID_H*CELL


def _rgb(arr3):
    return tuple(int(x) for x in arr3)

def render_frame(game: SnakeGame) -> Image.Image:
    im = Image.new("RGB", (W, H), _rgb(BG))
    draw = ImageDraw.Draw(im)

    # grid
    for x in range(GRID_W):
        draw.line([(x*CELL, 0), (x*CELL, H)], fill=_rgb(GRID))
    for y in range(GRID_H):
        draw.line([(0, y*CELL), (W, y*CELL)], fill=_rgb(GRID))

    # snake body
    for (x, y) in list(game.snake)[:-1]:
        draw.rounded_rectangle([x*CELL, y*CELL, x*CELL+CELL, y*CELL+CELL], radius=5, fill=_rgb(SNAKE))
    # head
    hx, hy = game.head
    draw.rounded_rectangle([hx*CELL, hy*CELL, hx*CELL+CELL, hy*CELL+CELL], radius=6, fill=_rgb(HEAD))

    # food
    if game.food:
        fx, fy = game.food
        pad = 3
        draw.rounded_rectangle([fx*CELL+pad, fy*CELL+pad, fx*CELL+CELL-pad, fy*CELL+CELL-pad], radius=6, fill=_rgb(FOOD))

    # HUD
    draw.text((8, 8), f"Score: {game.score}", fill=(220,220,230))
    return im

def tick(state: Tuple[SnakeGame, bool]):
    game, alive = state
    if not alive or not game.alive:
        return render_frame(game), (game, False)

    # AI move
    mv = choose_move(game)
    if mv is not None:
        game.set_dir(*mv)
    res = game.step()

    return render_frame(game), (game, res.alive)

def new_game():
    g = SnakeGame()
    return render_frame(g), (g, True)

with gr.Blocks(title="Snake-Bot") as demo:
    gr.Markdown("# 🐍 Snake-Bot\nAI plays Snake autonomously (BFS + safe fallback).")
    img = gr.Image(type="pil", interactive=False, label="Live View").style(height=H)
    state = gr.State()

    with gr.Row():
        start = gr.Button("Start / Reset", variant="primary")
    timer = gr.Timer(interval=1.0/ FPS, active=True)

    start.click(fn=new_game, outputs=[img, state])
    timer.tick(fn=tick, inputs=state, outputs=[img, state])


if __name__ == "__main__":
    demo.launch()
