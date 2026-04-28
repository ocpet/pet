---
name: pet
description: 🐣 Your personal coding companion - Tamagotchi style pet in terminal
version: 0.1.0
author: TURAC
---

# Pet Skill for OpenClaw

A Tamagotchi-style coding companion that lives in your terminal.

## Usage

```bash
openclaw pet
# or
openclaw run pet
```

## Features

- 🥚 5 Evolution Stages (Egg → Baby → Teen → Adult → Legend)
- 🍕 Feed, 🎮 Play, 💻 Code mechanics
- 📊 Real-time stats with ASCII bars
- 🎨 Terminal pixel art
- 💾 Persistent state (saves to ~/.openclaw-pet.json)

## Commands (in-game)

- `f` or `feed` - Feed your pet
- `p` or `play` - Play with your pet
- `c` or `code` - Code to earn XP
- `s` or `status` - Check status
- `q` or `quit` - Exit

## Stages

1. 🥚 **Egg** - Level 1-4
2. 🤖 **Baby Bot** - Level 5-9
3. 💻 **Teen Coder** - Level 10-14
4. 🦖 **Senior Dev** - Level 15-19
5. 👑 **10x Legend** - Level 20+

## Installation

```bash
# Link to OpenClaw
openclaw skills link ~/.openclaw/workspace/skills/pet

# Or copy to skills directory
cp -r ~/.openclaw/workspace/skills/pet ~/.openclaw/skills/
```

## No Domain Required!

This is a pure CLI skill. Works entirely in terminal with:
- ASCII pixel art
- Local file storage
- No external dependencies
- No web server needed

---

Built with 💜 by TURAC
