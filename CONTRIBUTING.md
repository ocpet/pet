# Contributing to Clawpet

Thanks for the interest! This is a small project with a clear scope, but contributions are welcome.

## Quick start

```bash
git clone https://github.com/ocpet/pet.git
cd pet
pip3 install pillow                  # for the share-card PNG
python3 server.py                    # listens on $PET_PORT (default 8080)
cloudflared tunnel --url http://localhost:8080  # for Telegram WebApp HTTPS
```

Then register a Mini App in BotFather pointing at the tunnel URL and open `t.me/<your-bot>/<your-app>` in Telegram.

## What we welcome

- **Bug fixes** — broken stat math, race conditions, font/emoji issues, mobile layout glitches
- **New languages** — add a block to `i18n.js` UI map + per-species personality dialogue. Currently TR/EN/FR/DE; Russian, Spanish, Portuguese, Korean are obvious next picks
- **Per-species dialogue lines** — more variety in `i18n.js` and `server.py` (PLAYDATE_LINES / AMBIENT_LINES)
- **Performance** — server uses single-threaded `http.server`; multi-threading + LRU cache for friend graphs would help
- **Documentation** — README clarifications, deploy guides for non-Oracle hosts, screenshots in different languages

## What we will probably push back on

- **Token / wallet / NFT integrations** — Clawpet is intentionally non-crypto. Drama as a viral mechanic is fine; wallet onboarding is not.
- **iOS / Android native apps** — the Telegram-only constraint is the entire pitch. A separate native app is a different product.
- **Heavy framework adoption** — backend should stay close to stdlib + Pillow; frontend should stay vanilla JS. The 700-LoC discipline is a feature.

## Code style

- **Python:** PEP 8, no formatter required, comments only for non-obvious things
- **JS:** vanilla, no transpilation, single file unless there's a strong reason
- **i18n:** all user-visible strings must route through `i18n.js` UI map or per-species dialogue tables
- **Storage:** JSON file per user. If you need a database, talk to us first

## Testing

There's no formal test suite. Before submitting a PR:

1. Run the backend locally
2. Open the Mini App through a real Telegram client (iOS or Android — desktop Telegram has different `DeviceMotion` behavior)
3. Walk through: hatch → name → feed → play → sleep → memorial (use file edit to fast-forward `lastFed` if you want to test mortality without waiting 7 days)
4. Test in at least 2 languages
5. Verify share card PNG renders correctly: `curl http://localhost:8080/card/<userId>.png?lang=en > out.png`

## PR conventions

- One concern per PR
- Conventional commits not required, but write commit messages that explain *why* the change is needed
- Update README / CHANGELOG if user-facing
- Don't include screenshots in the repo unless they're under 200 KB

## Reporting bugs

Open an issue with:
- Telegram client (iOS / Android / Desktop), version
- Pet state (species, level, streak) if relevant
- What you expected vs. what happened
- Console errors from `tg.WebApp` or browser devtools, if visible

## Licensing

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
