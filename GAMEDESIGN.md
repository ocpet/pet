# 🎮 OpenClaw Pet - Game Design Document

## 1. OYUN KONSEPTİ

**Tür:** Virtual Pet / Tamagotchi
**Platform:** Telegram Mini App
**Hedef Kitle:** Yazılımcılar, OpenClaw kullanıcıları
**Oynanış Süresi:** Günlük 2-3 dakika, uzun vadeli (aylarca)

## 2. ÇEKİRDEK DÖNGÜ (Core Loop)

```
Günlük Giriş → Pet'i Kontrol Et → Etkileşim (Feed/Play/Code) 
→ XP Kazan → Seviye Atlama → Evrim → Tekrar Et
```

## 3. OYUN DURUMLARI (Game States)

### State 1: EGG (Yumurta)
- **Süre:** İlk açılışta sabit
- **Etkileşim:** Shake veya 5x tap
- **Görsel:** 🥚 + sallanma animasyonu
- **Ses:** Tap sesi (her dokunuşta)
- **Geçiş:** 5. dokunuşta State 2'ye

### State 2: BABY (Bebek)
- **Seviye:** 1-4
- **Görsel:** 🤖
- **İhtiyaçlar:** Sık beslenme, sık oyun
- **Özellik:** Çabuk açlık, çabuk mutsuzluk
- **Ses:** Cırtlak bebek sesleri

### State 3: TEEN (Genç)
- **Seviye:** 5-9
- **Görsel:** 💻
- **İhtiyaçlar:** Kod yazma (daha fazla XP)
- **Özellik:** Daha az bakım, daha hızlı büyüme
- **Ses:** Enerjik genç sesleri

### State 4: ADULT (Yetişkin)
- **Seviye:** 10-19
- **Görsel:** 🦖
- **İhtiyaçlar:** Dengeli bakım
- **Özellik:** Streak bonusları, daily challenges
- **Ses:** Olgun, gururlu sesler

### State 5: LEGEND (Efsane)
- **Seviye:** 20+
- **Görsel:** 👑
- **İhtiyaçlar:** Minimum bakım, prestige sistemi
- **Özellik:** Liderboard, özel yetenekler
- **Ses:** Epik, efsanevi sesler

## 4. İSTATİSTİKLER (Stats)

### Primary Stats (0-100)
- **Hunger (Açlık):** 0 = aç, 100 = tok
  - Düşüş: Her dakika -0.5
  - Artış: Feed +20
  - Risk: <20 = üzgün pet, <10 = zarar görür

- **Happiness (Mutluluk):** 0 = depresif, 100 = çok mutlu
  - Düşüş: Her dakika -0.3
  - Artış: Play +15
  - Bonus: Streak varsa daha yavaş düşer

- **Energy (Enerji):** 0 = bitkin, 100 = dinç
  - Düşüş: Her aksiyonda -5
  - Artış: Zamanla +1/dk (uyku modu)
  - Kısıtlama: <20 = aksiyon yarı etkili

### Secondary Stats
- **XP (Deneyim):** 0-100 arası
  - Feed: +5 XP
  - Play: +10 XP
  - Code: +15 XP
  - 100 XP = Level Up

- **Level (Seviye):** 1-20+ arası
  - Her level = daha güçlü pet
  - Her 5 level = Evrim (yeni görünüm)

- **Streak (Seri):** Kaç gün üst üste giriş
  - Bonus: Her gün +%10 XP multiplier
  - Risk: Kaçırırsa streak reset

## 5. ETKİLEŞİM SİSTEMİ

### Feed (Besle) 🍕
- **Cooldown:** 30 saniye
- **Efekt:** Hunger +20, XP +5
- **Animasyon:** Pet yemeği yer (ağız aç-kapa)
- **Ses:** "Nom nom" sesi
- **Limit:** 100'e ulaşınca "I'm full!"

### Play (Oyna) 🎮
- **Cooldown:** 1 dakika
- **Efekt:** Happy +15, Energy -10, XP +10
- **Animasyon:** Pet zıplar, dans eder
- **Ses:** Neşeli melodi
- **Minigame:** Basit tap-the-dot oyunu (opsiyonel)

### Code (Kod Yaz) 💻
- **Cooldown:** 2 dakika
- **Efekt:** XP +15, Energy -5, Hunger -5
- **Animasyon:** Pet klavyede yazar, ekran parlar
- **Ses:** Typewriter + success chime
- **Bonus:** Streak varsa +50% XP

### Sleep (Uyku) 😴 (Pasif)
- **Otomatik:** Gece 23:00-08:00 arası
- **Efekt:** Energy +50/saat, Hunger -10/saat
- **Görsel:** Pet uyur, zzz animasyonu

## 6. GÜNLÜK DÖNGÜ (Daily Cycle)

### Morning (08:00-12:00)
- Pet uyanır
- +20 Energy bonus
- "Good morning!" mesajı

### Day (12:00-18:00)
- Normal aktivite
- +10% XP bonus (çalışma saatleri)

### Evening (18:00-23:00)
- Yüksek mutluluk dönemi
- +20% Play etkisi

### Night (23:00-08:00)
- Sleep mode aktif
- Auto-save
- Streak kontrolü (bugün girdi mi?)

## 7. SEVİYE ATLAMA SİSTEMİ

### Level Up (Her 100 XP)
- Flash efekti
- "Level X!" yazısı
- Pet büyür (scale up animasyon)
- Yeni özellik açılır (belirli levellerde)

### Evolution (Her 5 Level)
- **Level 5:** Baby → Teen
- **Level 10:** Teen → Adult
- **Level 20:** Adult → Legend

**Evrim Animasyonu:**
1. Ekran beyazlaşır
2. Pet parlar
3. Yeni görünüm belirir
4. Konfeti yağmuru
5. "Evolved to [STAGE]!" popup

## 8. STREAK SİSTEMİ

### Giriş Takibi
- Her gün giriş = +1 streak
- Kaçırırsa = reset
- Bonuslar:
  - 3 gün: +10% XP
  - 7 gün: +25% XP, özel badge
  - 14 gün: +50% XP, özel animasyon
  - 30 gün: +100% XP, LEGENDARY badge

### Streak Koruma
- 1x "Freeze" hakkı (haftada 1)
- Premium özellik: Auto-freeze

## 9. UI/UX TASARIMI

### Ana Ekran Layout
```
┌─────────────────────┐
│ 🔥 Streak: 5 Days   │  ← Header
├─────────────────────┤
│                     │
│    [PET GÖRSEL]     │  ← Center (büyük)
│    (animasyonlu)    │
│                     │
├─────────────────────┤
│ ⭐ Level 5 - Teen   │  ← Level badge
├─────────────────────┤
│ XP: ████████░░ 80%  │  ← XP bar
├─────────────────────┤
│ 🍕 ██████░░░░ 60%   │  ← Stats
│ 😊 ████████░░ 80%   │
│ ⚡ █████████░ 90%   │
├─────────────────────┤
│ [🍕] [🎮] [💻]     │  ← Buttons
└─────────────────────┘
```

### Renk Paleti
- Background: Gradient (Mor → Mavi)
- Pet Area: Yarı saydam beyaz (glassmorphism)
- Hunger: Kırmızı (#ff6b6b)
- Happy: Yeşil (#4ecdc4)
- Energy: Mavi (#45b7d1)
- XP: Mor (#f093fb)

### Animasyonlar
- Tüm geçişler: 0.3s ease
- Pet bounce: 2s infinite
- Stat değişimi: 0.5s smooth
- Button press: 0.1s scale

## 10. SES TASARIMI

### Sesler Listesi
1. **tap.mp3** - Yumurtaya dokunma (kısa "bip")
2. **crack.mp3** - Yumurta kırılma (cırtlak)
3. **hatch.mp3** - Pet çıkma (fanfare)
4. **feed.mp3** - Yemek yeme ("nom")
5. **play.mp3** - Oyun (neşeli melodi)
6. **code.mp3** - Kod yazma (typewriter)
7. **levelup.mp3** - Seviye atlama (success)
8. **evolve.mp3** - Evrim (epic)
9. **alert.mp3** - Uyarı (düşük stat)
10. **streak.mp3** - Streak bonus (özel)

## 11. KAYDETME SİSTEMİ

### LocalStorage (Client-side)
```javascript
{
  "pet": {
    "stage": 2,
    "level": 7,
    "xp": 45,
    "hunger": 60,
    "happy": 80,
    "energy": 90,
    "streak": 5,
    "lastLogin": "2026-04-28T12:00:00Z",
    "hatched": true
  }
}
```

### Senkronizasyon
- Her aksiyonda auto-save
- Login/out'ta sync
- Telegram CloudStorage (opsiyonel)

## 12. GELİŞTİRME AŞAMALARI

### Phase 1: MVP (Minimum Viable Product)
- [x] Yumurta + kırılma
- [x] Baby Bot görseli
- [x] 3 buton (Feed/Play/Code)
- [x] 3 stat bar
- [x] Basit animasyonlar

### Phase 2: Core Mechanics
- [ ] Seviye atlama
- [ ] Evrim sistemi
- [ ] Streak tracking
- [ ] Zaman-based decay
- [ ] Ses efektleri

### Phase 3: Polish
- [ ] Tüm evrim görseleri
- [ ] Minigames
- [ ] Liderboard
- [ ] Badges/achievements
- [ ] Customization

### Phase 4: Social
- [ ] Arkadaş ekleme
- [ ] Pet vs Pet
- [ ] Paylaşma
- [ ] Community events

---

**Bu document'e göre adım adım geliştireceğim!** 🚀
