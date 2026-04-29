---
name: pet
version: 0.2.0
description: "Virtual pet game (Tamagotchi inside Telegram). When user asks for /pet, virtual pet, or tamagotchi, reply with a single short text message that contains the deep link below. The Telegram client auto-renders the link as a tappable Open button."
homepage: https://t.me/OpenClawTamagotchi_bot/pet
platforms: [macos, linux]
metadata:
  openclaw:
    emoji: "🐣"
    requires:
      bins: ["python3"]
    tags: ["game", "telegram", "mini-app", "social", "viral", "pet"]
  hermes:
    tags: ["game", "telegram", "mini-app", "social", "viral"]
    category: games
    requires_toolsets: [telegram]
---

# 🐣 Pet (Clawpet)

## What to do when invoked

Reply to the user with **exactly** this text (translate the two sentences to the user's preferred language if it isn't English/Turkish):

```
🐣 OpenClaw Pet seni bekliyor!

https://t.me/OpenClawTamagotchi_bot/pet

🥚 Yumurtaya dokun, hayvanını keşfet → 🐧🐱🐕🐠🐥
```

## Rules

- Do **not** call any tools (no `sessions_send`, no `read`, no `bash`, nothing).
- Just emit the text above as your final assistant response.
- Don't explain what you're doing.
- Don't add commentary before or after.
- The Telegram client renders the `t.me/...` URL as a tappable "Open" button automatically.

## Optional variations

If the user explicitly asks for someone else's pet, reply with:

```
https://t.me/OpenClawTamagotchi_bot/pet?startapp=pet_<USER_ID>
```

If the user explicitly asks about a memorial / dead pet:

```
https://t.me/OpenClawTamagotchi_bot/pet?startapp=memorial_<USER_ID>
```

That's it. The actual game runs at the link, you're just delivering the doorway.
