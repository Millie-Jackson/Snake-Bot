---
title: Snake-Bot
emoji: 🐍
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: src/app.py
pinned: false
license: mit
---

# Snake-Bot 🐍🤖

An AI-controlled Snake game built with Python + Pygame.  
The bot uses **Breadth-First Search (BFS)** pathfinding to plan collision-free routes to the food, and falls back to safe-move heuristics when no path is available.

## Features
- Grid-based Snake game in `pygame`
- AI agent that plays autonomously
- BFS pathfinding toward food
- Safe-move survival fallback
- Clean modular code for future upgrades (A*, RL, Gemini integration)

## Setup
```bash
conda env create -f environment.yml
conda activate snake-bot
python src/game.py
