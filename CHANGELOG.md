# Changelog

All notable changes to Clawpet will be documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Russian (`ru`) i18n bundle
- Couple / jealousy mechanic (auto-generated romance + drama events between friend pets)
- Group raid (5+ pets vs. boss event, posts progress to the group chat)
- Telegram sticker pack (5 species × 5 expressions)
- Pet "tweet": daily auto-generated diary entry shareable as image
- HMAC validation of `initData` (security hardening before public scale)
- og:image meta tag on Mini App index for shared-link card preview

## [0.2.0] — 2026-04-29

### Added
- **Social layer:** visit links, befriend (bidirectional), 24h-cooldown playdates with auto-generated dialogue
- **Pet-to-pet ambient interactions:** server-side cron-like events (35% probability per friend, 6h cooldown) that spawn dialogue when both pets have friends
- **Pet diary:** last 3 dialogue lines shown on the pet screen
- **Permanent mortality:** 7 days no feed → dead, archived to `memorial/`
- **Sad mode:** 3 days neglect → grayscale + per-species sad dialogue
- **Streak counter:** consecutive-day login tracking, milestone bubbles at 3 / 7 / 30 days
- **Memorial page + reincarnation:** dead pet has a shareable read-only page; user can opt to start a new pet of the same species (+ "II") losing all level / friends / bond
- **i18n (TR/EN/FR/DE):** 4-language UI + per-species personality dialogue (~120 hand-written lines)
- **Pet card PNG:** server-rendered 1080×1350 share card via Pillow (with SVG fallback if Pillow is unavailable). Cross-platform font handling (Apple Color Emoji on macOS, NotoColorEmoji bitmap on Linux with auto-scale)
- **Cross-runtime skill metadata:** single `SKILL.md` works in both OpenClaw and Hermes Agent runtimes
- **Resume:** Mini App detects existing pets on load and skips egg screen
- **iOS shake-to-hatch permission flow:** explicit DeviceMotion request button for iOS 13+
- **Public landing site** (`ocpet.github.io/pet`) with `/alternatives/tamagotchi`, `/use-cases/group-chat`, `/blog/best-telegram-mini-apps-2026`

### Changed
- Backend `ROOT` resolves from script path or `PET_ROOT` env var (was hardcoded `~/.openclaw/...`)
- Pet `type` is now stored as species string (`fish`, `cat`, etc.), not an emoji char. Migration script applied to existing data on the production VM.
- Stat-bar background color fix (was rendering as solid black due to RGBA fill on RGB image)
- Card text labels (`days`, `friends`, `IN MEMORIAM`, `Rest in peace`) now localize via `?lang=` query param on `/card/<userId>.png`
- Pet-screen layout compacted to fit Telegram WebView viewport without scrolling on iPhone

### Fixed
- Resume flow correctly handles legacy pets stored with emoji-as-type
- Emoji rendering on Linux uses `NotoColorEmoji` (bitmap, fixed 109px) and scales down via LANCZOS for inline icons
- DuckDNS auto-update cron prevents IP hijacking by external squatters

## [0.1.0] — 2026-04-26

### Added
- Initial Telegram Mini App with shake-to-hatch (5 species: penguin, cat, dog, fish, chick)
- Care loop: feed, play, sleep, with hunger / happy / energy stats
- Per-user JSON storage
- OpenClaw skill metadata (`SKILL.md` with `metadata.openclaw` block)

[Unreleased]: https://github.com/ocpet/pet/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/ocpet/pet/releases/tag/v0.2.0
[0.1.0]: https://github.com/ocpet/pet/releases/tag/v0.1.0
