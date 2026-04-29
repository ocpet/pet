#!/usr/bin/env python3
"""
OpenClaw Pet — Python backend.

Endpoints:
  GET  /                   → index.html
  POST /api/pet            → action dispatcher

Actions:
  create   {type, name}              → spawn new pet
  feed / play / sleep                → mutate own pet
  visit    {targetUserId}            → read another user's pet (read-only)
  befriend {targetUserId}            → add bidirectional friendship + bond bonus
  playdate {targetUserId}            → 24h-gated joint playdate, boosts both
  friends                            → list current user's friends with minimal pet info
"""
import http.server
import socketserver
import json
import os
import io
import random
from datetime import datetime, timedelta

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PORT = int(os.environ.get('PET_PORT', '8080'))
ROOT = os.environ.get('PET_ROOT') or os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(ROOT, "users")
MEMORIAL_DIR = os.path.join(ROOT, "memorial")
os.makedirs(USERS_DIR, exist_ok=True)
os.makedirs(MEMORIAL_DIR, exist_ok=True)

EMOJI = {'penguin': '🐧', 'cat': '🐱', 'dog': '🐕', 'fish': '🐠', 'chick': '🐥'}
SAD_DAYS = 3
DEATH_DAYS = 7

PLAYDATE_LINES = {
    'tr': [
        "{a}: {b} ile koşturduk, harikaydı!",
        "{a}: {b} bana yeni bir oyun öğretti 🎉",
        "{a}: havlama dur {b} 😤",
        "{a}: {b} ile uyukladık, tatlı rüyalar",
        "{a}: {b} hep benim mamamı çalıyor!",
        "{a}: {b} en iyi arkadaşım 💕",
    ],
    'en': [
        "{a}: ran around with {b}, amazing!",
        "{a}: {b} taught me a new game 🎉",
        "{a}: stop barking {b} 😤",
        "{a}: napped with {b}, sweet dreams",
        "{a}: {b} keeps stealing my food!",
        "{a}: {b} is my best friend 💕",
    ],
    'fr': [
        "{a}: j'ai couru avec {b}, génial !",
        "{a}: {b} m'a appris un nouveau jeu 🎉",
        "{a}: arrête d'aboyer {b} 😤",
        "{a}: sieste avec {b}, doux rêves",
        "{a}: {b} vole toujours ma nourriture !",
        "{a}: {b} est mon meilleur ami 💕",
    ],
    'de': [
        "{a}: bin mit {b} gerannt, großartig!",
        "{a}: {b} hat mir ein neues Spiel beigebracht 🎉",
        "{a}: hör auf zu bellen {b} 😤",
        "{a}: mit {b} geschlafen, süße Träume",
        "{a}: {b} klaut immer mein Futter!",
        "{a}: {b} ist mein bester Freund 💕",
    ],
}

AMBIENT_LINES = {
    'tr': [
        "{a}: {b} bana mama gönderdi 🍖",
        "{a}: {b} pencereden baktı, gülümsedik",
        "{a}: rüyamda {b} ile koştuk",
        "{a}: {b} özledim ama söylemem",
        "{b}: {a}, sen iyi misin?",
        "{a}: {b} ile sessizce oturduk",
    ],
    'en': [
        "{a}: {b} sent me food 🍖",
        "{a}: {b} looked through the window, we smiled",
        "{a}: dreamed of running with {b}",
        "{a}: missed {b} but won't say it",
        "{b}: {a}, are you alright?",
        "{a}: sat quietly with {b}",
    ],
    'fr': [
        "{a}: {b} m'a envoyé de la nourriture 🍖",
        "{a}: {b} a regardé par la fenêtre, on a souri",
        "{a}: j'ai rêvé de courir avec {b}",
        "{a}: {b} me manquait mais je ne le dirai pas",
        "{b}: {a}, tu vas bien ?",
        "{a}: assis tranquillement avec {b}",
    ],
    'de': [
        "{a}: {b} hat mir Futter geschickt 🍖",
        "{a}: {b} schaute durchs Fenster, wir lächelten",
        "{a}: träumte vom Laufen mit {b}",
        "{a}: vermisste {b}, aber ich sag's nicht",
        "{b}: {a}, geht's dir gut?",
        "{a}: still mit {b} gesessen",
    ],
}


def user_path(user_id):
    return os.path.join(USERS_DIR, f"{user_id}.json")


def load_pet(user_id):
    p = user_path(user_id)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        pet = json.load(f)
    pet.setdefault('friends', [])
    pet.setdefault('bond', {})
    pet.setdefault('lastPlaydate', {})
    pet.setdefault('dialogues', [])
    pet.setdefault('status', 'alive')
    pet.setdefault('streak', 0)
    pet.setdefault('lastActiveDate', None)
    apply_decay(pet)
    return pet


def apply_decay(pet):
    """Mutates pet in place: decay stats + update status based on elapsed time."""
    if pet.get('status') == 'dead':
        return
    anchor = pet.get('lastFed') or pet.get('lastPlayed') or pet.get('created')
    if not anchor:
        return
    try:
        elapsed = datetime.now() - datetime.fromisoformat(anchor)
    except Exception:
        return
    days = elapsed.total_seconds() / 86400
    decayed_hunger = max(0, pet.get('hunger', 50) - int(days * 8))
    decayed_happy = max(0, pet.get('happy', 50) - int(days * 6))
    pet['hunger'] = decayed_hunger
    pet['happy'] = decayed_happy
    if days >= DEATH_DAYS or decayed_hunger <= 0:
        pet['status'] = 'dead'
        pet.setdefault('diedAt', datetime.now().isoformat())
    elif days >= SAD_DAYS:
        pet['status'] = 'sad'
    else:
        pet['status'] = 'alive'


def touch_streak(pet):
    today = datetime.now().date()
    last = pet.get('lastActiveDate')
    if last == today.isoformat():
        return
    yesterday = (today - timedelta(days=1)).isoformat()
    pet['streak'] = pet.get('streak', 0) + 1 if last == yesterday else 1
    pet['lastActiveDate'] = today.isoformat()


def archive_memorial(pet):
    """Move dead pet record to memorial dir."""
    uid = str(pet['userId'])
    with open(os.path.join(MEMORIAL_DIR, f"{uid}.json"), 'w') as f:
        json.dump(pet, f, indent=2, ensure_ascii=False)


CARD_LABELS = {
    'tr': {'days': 'gün', 'friends': 'arkadaş', 'memoriam': 'IN MEMORIAM', 'rip': 'Sevgili dostumuz huzur içinde uyusun'},
    'en': {'days': 'days', 'friends': 'friends', 'memoriam': 'IN MEMORIAM', 'rip': 'Rest in peace, dear friend'},
    'fr': {'days': 'jours', 'friends': 'amis', 'memoriam': 'IN MEMORIAM', 'rip': 'Repose en paix, cher ami'},
    'de': {'days': 'Tage', 'friends': 'Freunde', 'memoriam': 'IN MEMORIAM', 'rip': 'Ruhe in Frieden, lieber Freund'},
}


def render_card(pet, lang='tr'):
    """Render shareable PNG card. Returns bytes or None if PIL unavailable."""
    if not HAS_PIL:
        return None
    L = CARD_LABELS.get(lang, CARD_LABELS['tr'])
    W, H = 1080, 1350
    is_dead = pet.get('status') == 'dead'
    bg_top = (15, 23, 42) if is_dead else (102, 126, 234)
    bg_bot = (51, 65, 85) if is_dead else (118, 64, 162)
    img = Image.new('RGB', (W, H), bg_top)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(bg_top[0] * (1 - t) + bg_bot[0] * t)
        g = int(bg_top[1] * (1 - t) + bg_bot[1] * t)
        b = int(bg_top[2] * (1 - t) + bg_bot[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    d = ImageDraw.Draw(img)

    def first_font(paths, size):
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
        return ImageFont.load_default()

    EMOJI_FONTS = [
        "/System/Library/Fonts/Apple Color Emoji.ttc",
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "/usr/share/fonts/noto-cjk/NotoColorEmoji.ttf",
    ]
    TEXT_FONTS = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    # NotoColorEmoji is a bitmap font that only accepts size 109 — render at 109 then resize via different approach
    emoji_font = None
    for p in EMOJI_FONTS:
        for sz in (240, 137, 109):
            try:
                emoji_font = ImageFont.truetype(p, sz)
                break
            except Exception:
                continue
        if emoji_font:
            break
    if emoji_font is None:
        emoji_font = ImageFont.load_default()
    big_font = first_font(TEXT_FONTS, 96)
    med_font = first_font(TEXT_FONTS, 48)
    sml_font = first_font(TEXT_FONTS, 36)

    # Inline emoji icon font (Noto bitmap is fixed-size, only 109 works on Linux; Apple's font
    # accepts arbitrary sizes). For Linux we render at native size then scale down.
    icon_font_native = None
    icon_native_size = 109
    for p in EMOJI_FONTS:
        # Try a small native size first (Apple), then fall back to Noto's fixed 109
        for sz in (48, 109):
            try:
                icon_font_native = ImageFont.truetype(p, sz)
                icon_native_size = sz
                break
            except Exception:
                continue
        if icon_font_native:
            break

    def paste_emoji(center_xy, char, target_size=56):
        """Render emoji char to a temp RGBA image and paste centered, scaled to target_size."""
        if not icon_font_native:
            d.text(center_xy, char, font=med_font, fill='white', anchor='mm')
            return
        if icon_native_size <= target_size + 8:
            # font is already at the right size, render directly
            try:
                d.text(center_xy, char, font=icon_font_native, fill='white', anchor='mm', embedded_color=True)
            except Exception:
                d.text(center_xy, char, font=icon_font_native, fill='white', anchor='mm')
            return
        # Render to temp RGBA at native size, scale down, paste with alpha
        tmp = Image.new('RGBA', (icon_native_size + 20, icon_native_size + 20), (0,0,0,0))
        td = ImageDraw.Draw(tmp)
        try:
            td.text((tmp.size[0]/2, tmp.size[1]/2), char, font=icon_font_native, anchor='mm', embedded_color=True)
        except Exception:
            td.text((tmp.size[0]/2, tmp.size[1]/2), char, font=icon_font_native, fill='white', anchor='mm')
        scaled = tmp.resize((target_size, target_size), Image.Resampling.LANCZOS)
        cx, cy = int(center_xy[0]), int(center_xy[1])
        img.paste(scaled, (cx - target_size//2, cy - target_size//2), scaled)

    def text_emoji(xy, content, font, fill='white', anchor='mm'):
        """Draw text that may contain emoji using embedded_color when supported."""
        try:
            d.text(xy, content, font=font, fill=fill, anchor=anchor, embedded_color=True)
        except Exception:
            d.text(xy, content, font=font, fill=fill, anchor=anchor)

    # Big main emoji also needs scaling on Linux when font is bitmap-only
    main_emoji_size = 280  # target render size
    def paste_main_emoji(center_xy, char):
        if not emoji_font:
            d.text(center_xy, char, font=big_font, fill='white', anchor='mm')
            return
        # If emoji_font's pixel size already matches roughly, draw direct
        try:
            ef_size = emoji_font.size
        except Exception:
            ef_size = 240
        if abs(ef_size - main_emoji_size) <= 24:
            text_emoji(center_xy, char, emoji_font, 'white')
            return
        tmp = Image.new('RGBA', (ef_size + 40, ef_size + 40), (0,0,0,0))
        td = ImageDraw.Draw(tmp)
        try:
            td.text((tmp.size[0]/2, tmp.size[1]/2), char, font=emoji_font, anchor='mm', embedded_color=True)
        except Exception:
            td.text((tmp.size[0]/2, tmp.size[1]/2), char, font=emoji_font, fill='white', anchor='mm')
        scaled = tmp.resize((main_emoji_size, main_emoji_size), Image.Resampling.LANCZOS)
        cx, cy = int(center_xy[0]), int(center_xy[1])
        img.paste(scaled, (cx - main_emoji_size//2, cy - main_emoji_size//2), scaled)

    emoji = '🪦' if is_dead else EMOJI.get(pet.get('type'), '🐾')
    name = pet.get('name', '?')
    if is_dead:
        d.text((W/2, 200), L['memoriam'], font=med_font, fill='white', anchor='mm')
    paste_main_emoji((W/2, 470), emoji)
    d.text((W/2, 720), name, font=big_font, fill='white', anchor='mm')

    if is_dead:
        died = (pet.get('diedAt') or '')[:10]
        born = (pet.get('created') or '')[:10]
        d.text((W/2, 840), f'{born} — {died}', font=med_font, fill='white', anchor='mm')
        d.text((W/2, 920), f'Level {pet.get("level",1)} · {len(pet.get("friends",[]))} {L["friends"]}', font=sml_font, fill=(220,220,220), anchor='mm')
        text_emoji((W/2, 1080), L['rip'] + ' 🕯', sml_font, (200,200,200))
    else:
        # "Level 28 · 🔥 38 days" — split so streak emoji uses emoji font
        level_txt = f'Level {pet.get("level",1)}'
        days_txt = f'{pet.get("streak",0)} {L["days"]}'
        d.text((W/2 - 200, 840), level_txt + ' ·', font=med_font, fill='white', anchor='mm')
        paste_emoji((W/2, 840), '🔥', target_size=52)
        d.text((W/2 + 200, 840), days_txt, font=med_font, fill='white', anchor='mm')
        # Stat bars
        stats = [('🍕', pet.get('hunger',0), (255,107,107)),
                 ('😊', pet.get('happy',0), (78,205,196)),
                 ('⚡', pet.get('energy',0), (69,183,209))]
        bar_x = 240; bar_w = 600; bar_h = 40; y = 950
        for icon, val, color in stats:
            paste_emoji((bar_x - 70, y + bar_h/2), icon, target_size=44)
            # RGB-only background (was alpha-broken in RGB mode → solid black)
            d.rectangle([bar_x, y, bar_x + bar_w, y + bar_h], fill=(40, 40, 70), outline=(255,255,255,200))
            d.rectangle([bar_x, y, bar_x + int(bar_w * val/100), y + bar_h], fill=color)
            d.text((bar_x + bar_w + 60, y + bar_h/2), str(val), font=med_font, fill='white', anchor='mm')
            y += 80

    # Footer: emoji + count + label split
    f_count = len(pet.get('friends', []))
    paste_emoji((W/2 - 110, H - 100), '🤝', target_size=40)
    d.text((W/2 + 20, H - 100), f'{f_count} {L["friends"]}', font=sml_font, fill='white', anchor='mm')
    d.text((W/2, H - 50), 't.me/OpenClawTamagotchi_bot/pet', font=sml_font, fill=(220,220,220), anchor='mm')

    out = io.BytesIO()
    img.save(out, format='PNG', optimize=True)
    return out.getvalue()


def render_card_svg(pet):
    is_dead = pet.get('status') == 'dead'
    emoji = '🪦' if is_dead else EMOJI.get(pet.get('type'), '🐾')
    bg = '#0f172a' if is_dead else '#667eea'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
<rect width="1080" height="1350" fill="{bg}"/>
<text x="540" y="500" font-size="240" text-anchor="middle">{emoji}</text>
<text x="540" y="720" font-size="96" font-weight="bold" fill="white" text-anchor="middle" font-family="Helvetica">{pet.get('name','?')}</text>
<text x="540" y="820" font-size="48" fill="white" text-anchor="middle" font-family="Helvetica">Level {pet.get('level',1)} · 🔥 {pet.get('streak',0)} gün</text>
<text x="540" y="1280" font-size="36" fill="#ddd" text-anchor="middle" font-family="Helvetica">t.me/OpenClawTamagotchi_bot/pet</text>
</svg>'''


def save_pet(user_id, pet):
    with open(user_path(user_id), 'w') as f:
        json.dump(pet, f, indent=2, ensure_ascii=False)


def public_view(pet):
    """Read-only projection used for visit/friends endpoints."""
    if not pet:
        return None
    return {
        'userId': pet.get('userId'),
        'type': pet.get('type'),
        'name': pet.get('name'),
        'emoji': EMOJI.get(pet.get('type'), '🐾'),
        'hunger': pet.get('hunger', 0),
        'happy': pet.get('happy', 0),
        'energy': pet.get('energy', 0),
        'level': pet.get('level', 1),
        'friendCount': len(pet.get('friends', [])),
        'recentDialogue': (pet.get('dialogues') or [None])[-1],
    }


def add_friendship(a_pet, b_pet):
    a_id, b_id = str(a_pet['userId']), str(b_pet['userId'])
    fresh = b_id not in a_pet['friends']
    if fresh:
        a_pet['friends'].append(b_id)
        if a_id not in b_pet['friends']:
            b_pet['friends'].append(a_id)
        a_pet['bond'][b_id] = a_pet['bond'].get(b_id, 0) + 10
        b_pet['bond'][a_id] = b_pet['bond'].get(a_id, 0) + 10
        a_pet['happy'] = min(100, a_pet.get('happy', 0) + 5)
        b_pet['happy'] = min(100, b_pet.get('happy', 0) + 5)
    return fresh


def _line_pool(pool, lang):
    return pool.get((lang or 'tr').lower(), pool['tr'])


def do_playdate(a_pet, b_pet, lang='tr'):
    a_id, b_id = str(a_pet['userId']), str(b_pet['userId'])
    last = a_pet['lastPlaydate'].get(b_id)
    if last:
        last_dt = datetime.fromisoformat(last)
        if datetime.now() - last_dt < timedelta(hours=24):
            return None  # cooldown
    now = datetime.now().isoformat()
    a_pet['lastPlaydate'][b_id] = now
    b_pet['lastPlaydate'][a_id] = now
    a_pet['bond'][b_id] = a_pet['bond'].get(b_id, 0) + 5
    b_pet['bond'][a_id] = b_pet['bond'].get(a_id, 0) + 5
    a_pet['happy'] = min(100, a_pet.get('happy', 0) + 15)
    b_pet['happy'] = min(100, b_pet.get('happy', 0) + 15)
    a_pet['energy'] = max(0, a_pet.get('energy', 0) - 10)
    b_pet['energy'] = max(0, b_pet.get('energy', 0) - 10)
    line = random.choice(_line_pool(PLAYDATE_LINES, lang)).format(a=a_pet['name'], b=b_pet['name'])
    a_pet['dialogues'] = (a_pet.get('dialogues', []) + [line])[-20:]
    b_pet['dialogues'] = (b_pet.get('dialogues', []) + [line])[-20:]
    return line


def maybe_ambient_event(pet, lang='tr'):
    """Triggered on pet load. If has friends and last event >6h ago, ~30% chance to spawn an event."""
    friends = pet.get('friends', [])
    if not friends:
        return None
    last = pet.get('lastAmbient')
    if last:
        try:
            if datetime.now() - datetime.fromisoformat(last) < timedelta(hours=6):
                return None
        except Exception:
            pass
    if random.random() > 0.35:
        return None
    fid = random.choice(friends)
    friend = load_pet(fid)
    if not friend or friend.get('status') == 'dead':
        return None
    line = random.choice(_line_pool(AMBIENT_LINES, lang)).format(a=pet['name'], b=friend['name'])
    pet['dialogues'] = (pet.get('dialogues', []) + [line])[-20:]
    friend['dialogues'] = (friend.get('dialogues', []) + [line])[-20:]
    pet['lastAmbient'] = datetime.now().isoformat()
    friend['lastAmbient'] = datetime.now().isoformat()
    pet['happy'] = min(100, pet.get('happy', 50) + 3)
    friend['happy'] = min(100, friend.get('happy', 50) + 3)
    save_pet(str(friend['userId']), friend)
    return line


class PetHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(ROOT, 'index.html'), 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.startswith('/card/'):
            raw = self.path.replace('/card/', '').replace('.png', '')
            uid = raw.split('?')[0]
            lang = 'tr'
            if '?' in raw:
                from urllib.parse import parse_qs
                qs = parse_qs(raw.split('?', 1)[1])
                lang = (qs.get('lang') or ['tr'])[0].lower()
            self.serve_card(uid, lang)
        else:
            super().do_GET()

    def serve_card(self, user_id, lang='tr'):
        pet = load_pet(user_id) or self._load_memorial(user_id)
        if not pet:
            self.send_response(404); self.end_headers(); return
        png = render_card(pet, lang)
        if png is None:
            # Fallback: SVG
            svg = render_card_svg(pet)
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()
            self.wfile.write(svg.encode('utf-8'))
            return
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(png)

    def _load_memorial(self, user_id):
        p = os.path.join(MEMORIAL_DIR, f"{user_id}.json")
        if not os.path.exists(p): return None
        with open(p) as f: return json.load(f)

    def _json(self, status, payload):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        if self.path != '/api/pet':
            self.send_response(404); self.end_headers(); return

        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length) or b'{}')
        user_id = str(data.get('userId', 'unknown'))
        action = data.get('action')
        target_id = str(data.get('targetUserId', '')) if data.get('targetUserId') else None
        lang = (data.get('lang') or 'tr').lower()

        pet = load_pet(user_id)
        # Ambient pet-to-pet on each action (if alive + has friends)
        if pet and pet.get('status') != 'dead' and action in ('feed', 'play', 'sleep', 'diary'):
            maybe_ambient_event(pet, lang)

        # If pet exists and is dead, only memorial/revive/visit/create allowed
        if pet and pet.get('status') == 'dead' and action not in ('memorial', 'revive', 'visit', 'create', 'friends'):
            return self._json(410, {'error': 'pet_dead', 'message': f'{pet.get("name")} öldü 🪦', 'pet': pet})

        if action == 'create':
            # If old pet existed and is dead, archive it first
            if pet and pet.get('status') == 'dead':
                archive_memorial(pet)
            pet_type = data.get('type', 'cat')
            pet = {
                'userId': user_id,
                'type': pet_type,
                'name': data.get('name', 'Pamuk'),
                'hunger': 50, 'happy': 50, 'energy': 100, 'level': 1,
                'status': 'alive', 'streak': 1,
                'lastActiveDate': datetime.now().date().isoformat(),
                'created': datetime.now().isoformat(),
                'lastFed': None, 'lastPlayed': None,
                'friends': [], 'bond': {}, 'lastPlaydate': {}, 'dialogues': [],
            }
            save_pet(user_id, pet)
            return self._json(200, pet)

        if action == 'feed' and pet:
            pet['hunger'] = min(100, pet['hunger'] + 25)
            pet['lastFed'] = datetime.now().isoformat()
            pet['status'] = 'alive'
            touch_streak(pet)
            save_pet(user_id, pet)
            return self._json(200, pet)

        if action == 'play' and pet:
            if pet['energy'] >= 10:
                pet['happy'] = min(100, pet['happy'] + 20)
                pet['energy'] = max(0, pet['energy'] - 10)
                pet['lastPlayed'] = datetime.now().isoformat()
                pet['status'] = 'alive'
                touch_streak(pet)
                save_pet(user_id, pet)
            return self._json(200, pet)

        if action == 'sleep' and pet:
            pet['energy'] = min(100, pet['energy'] + 30)
            touch_streak(pet)
            save_pet(user_id, pet)
            return self._json(200, pet)

        if action == 'memorial':
            # View memorial (own dead pet or via targetUserId)
            target = pet
            if target_id:
                target = load_pet(target_id) or self._load_memorial(target_id)
            if not target or target.get('status') != 'dead':
                return self._json(404, {'error': 'no_memorial'})
            return self._json(200, public_view(target) | {
                'status': 'dead',
                'diedAt': target.get('diedAt'),
                'created': target.get('created'),
                'cardUrl': f'/card/{target.get("userId")}.png',
            })

        if action == 'revive':
            # Forfeit feature: lose all friends, lose level, lose streak. Hard cost.
            if not pet:
                return self._json(404, {'error': 'no_pet'})
            archive_memorial(pet)
            pet = {
                'userId': user_id,
                'type': pet.get('type'),
                'name': pet.get('name') + ' II',
                'hunger': 50, 'happy': 50, 'energy': 100, 'level': 1,
                'status': 'alive', 'streak': 0,
                'lastActiveDate': datetime.now().date().isoformat(),
                'created': datetime.now().isoformat(),
                'lastFed': datetime.now().isoformat(),
                'friends': [], 'bond': {}, 'lastPlaydate': {}, 'dialogues': [],
                'reincarnatedFrom': pet.get('userId'),
            }
            save_pet(user_id, pet)
            return self._json(200, pet)

        if action == 'visit':
            if not target_id:
                return self._json(400, {'error': 'targetUserId required'})
            target = load_pet(target_id)
            if not target:
                return self._json(404, {'error': 'pet not found'})
            view = public_view(target)
            view['isFriend'] = pet is not None and target_id in pet.get('friends', [])
            view['bond'] = (pet or {}).get('bond', {}).get(target_id, 0)
            return self._json(200, view)

        if action == 'befriend':
            if not pet or not target_id:
                return self._json(400, {'error': 'need own pet and targetUserId'})
            target = load_pet(target_id)
            if not target:
                return self._json(404, {'error': 'pet not found'})
            fresh = add_friendship(pet, target)
            save_pet(user_id, pet); save_pet(target_id, target)
            return self._json(200, {'fresh': fresh, 'pet': pet, 'target': public_view(target)})

        if action == 'playdate':
            if not pet or not target_id:
                return self._json(400, {'error': 'need own pet and targetUserId'})
            target = load_pet(target_id)
            if not target:
                return self._json(404, {'error': 'pet not found'})
            if target_id not in pet.get('friends', []):
                return self._json(400, {'error': 'not friends yet'})
            line = do_playdate(pet, target, lang)
            if line is None:
                return self._json(429, {'error': 'cooldown', 'message': '24 saatte bir playdate'})
            save_pet(user_id, pet); save_pet(target_id, target)
            return self._json(200, {'dialogue': line, 'pet': pet, 'target': public_view(target)})

        if action == 'diary':
            if not pet:
                return self._json(404, {'error': 'no_pet'})
            save_pet(user_id, pet)  # persist any ambient mutation
            return self._json(200, {'lines': pet.get('dialogues', [])})

        if action == 'friends':
            friends = []
            for fid in (pet or {}).get('friends', []):
                fp = load_pet(fid)
                if fp:
                    v = public_view(fp)
                    v['bond'] = pet['bond'].get(fid, 0)
                    friends.append(v)
            return self._json(200, {'friends': friends})

        return self._json(400, {'error': f'unknown action: {action}'})


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PetHandler) as httpd:
        print(f"🐣 OpenClaw Pet server running at http://localhost:{PORT}")
        print(f"   cloudflared tunnel --url http://localhost:{PORT}")
        httpd.serve_forever()
