# 🐣 OpenClaw Pet - Kullanıcı Senaryosu

## Senaryo 1: İlk Açılış (Yeni Kullanıcı)

### Adım 1: Botu Açma
**Kullanıcı:** Telegram'da OpenClaw botuna tıklar

**Bot Yanıtı:**
```
🐣 Welcome to OpenClaw Pet!

Your coding companion is waiting for you.
Tap the menu button below to meet your pet!

[🐣 Open Pet] ← Menu Button
```

### Adım 2: Menü Butonuna Tıklama
**Kullanıcı:** "🐣 Open Pet" butonuna tıklar

**Açılan Ekran:**
- Tam ekran Web App açılır
- Arka planda mor/mavi gradient
- Ortada BÜYÜK bir 🥚 yumurta
- Altında yazı: "📱 Shake phone or tap egg to hatch!"
- Ekranda parçacık animasyonları

### Adım 3: Yumurtaya Dokunma/Sallama
**Kullanıcı:** Telefonu sallar veya yumurtaya 5 kez dokunur

**Animasyon:**
1. Dokunuş 1-2: Yumurta hafif sallanır
2. Dokunuş 3-4: Çatlaklar (🐣) görünür
3. Dokunuş 5: YUMURTA KIRILIR! 💥
   - Kırılma animasyonu
   - Ses efekti (cırtlak)
   - Titreşim
   - 🤖 Baby Bot belirir!

**Popup:**
```
🎉 It's a Baby Bot!
Your pet has hatched! Take good care of it!
[OK]
```

### Adım 4: Pet ile Etkileşim
**Ekran Değişimi:**
- Üstte: "⭐ Level 1 - Baby Bot"
- Ortada: 🤖 (animasyonlu, zıplayan)
- Altında 3 stat bar:
  - 🍕 Hunger: ██████░░░░ 60%
  - 😊 Happy: ██████░░░░ 60%
  - ⚡ Energy: ██████████ 100%
- Altta 3 buton: [🍕 Feed] [🎮 Play] [💻 Code]

---

## Senaryo 2: Günlük Kullanım

### Adım 1: Kontrol
**Kullanıcı:** Botu açar, menüden Pet'e tıklar

**Durum Kontrolü:**
- Pet'in açlık seviyesi düşmüş ( zaman geçtiği için)
- Hunger: ███░░░░░░░ 30% (kırmızı renk)

### Adım 2: Besleme
**Kullanıcı:** 🍕 Feed butonuna basar

**Sonuç:**
- Animasyon: Pet yemeği yer (ağız hareketi)
- Hunger: 30% → 50% (yeşil artış)
- XP: +5 puan
- Ses: "Chomp" efekti

### Adım 3: Oyun
**Kullanıcı:** 🎮 Play butonuna basar

**Sonuç:**
- Pet mutlu dans eder
- Happy: 60% → 75%
- Energy: 100% → 90% (yoruldu)
- XP: +10 puan
- Ses: Neşeli melodi

### Adım 4: Kod Yazma
**Kullanıcı:** 💻 Code butonuna basar (Gerçekten kod yazdığını simüle eder)

**Sonuç:**
- Pet gururlu bakar
- XP: +15 puan (en çok bundan kazanır)
- Energy: 90% → 85%
- Seviye atlama kontrolü yapılır

---

## Senaryo 3: Seviye Atlama (Evolution)

### Koşul: XP 100 oldu
**Sistem:** Otomatik kontrol

### Adım 1: Seviye Atlama
**Ekran:**
- Flash efekti
- Pet büyür
- "✨ LEVEL UP!" yazısı belirir

### Adım 2: Evrim (Belirli Seviyelerde)
**Level 5:** 🤖 Baby Bot → 💻 Teen Coder
**Level 10:** 💻 Teen Coder → 🦖 Senior Dev
**Level 20:** 🦖 Senior Dev → 👑 10x Legend

**Her Evrimde:**
- Büyük patlama animasyonu
- Yeni görünüm
- Yeni animasyonlar
- Özel ses efekti
- Achievement popup

---

## Senaryo 4: Streak (Seri)

### Günlük Giriş
**Kullanıcı:** Her gün botu açar

**Ödül:**
- Gün 1: "Welcome back!"
- Gün 2: "🔥 2 Day Streak!"
- Gün 7: "🔥🔥 7 Day Streak! Bonus XP!"
- Gün 30: "🔥🔥🔥 30 Day Streak! LEGENDARY!"

---

## Senaryo 5: Uyarılar (Düşük Stat)

### Açlık Uyarısı
**Koşul:** Hunger < 20%

**Ekran:**
- Pet üzgün gözükür
- Kırmızı uyarı: "⚠️ Your pet is hungry!"
- Titreşim

### Enerji Uyarısı
**Koşul:** Energy < 10%

**Ekran:**
- Pet yorgun yatar
- "😴 Your pet needs sleep!"

---

## Teknik Akış

```
Kullanıcı Tıklar → Telegram WebApp Açar → 
Yumurta Göster → Sallama/Dokunma Algıla →
Kırılma Animasyonu → Pet Belirir →
Stat Barları Göster → Butonları Aktif Et →
Kullanıcı Etkileşim → Stat Güncelle →
XP Kontrol Et → Seviye Atlama? →
Evrim Kontrol Et → Animasyon Göster
```

## Önemli Kurallar

1. **İlk Açılış:** MUTLAKA yumurta göster
2. **Hatching:** 5 dokunuş veya shake ZORUNLU
3. **Ses:** Her aksiyonda farklı ses
4. **Titreşim:** Telegram haptic + telefon vibrate
5. **Animasyon:** Hiçbir şey aniden olmamalı (0.3s transition)
6. **Kaydetme:** Her aksiyonda otomatik save

---

## Renkler

- Yumurta: 🟡 Sarı (#FFE4B5)
- Baby Bot: 🔵 Turkuaz (#4ECDC4)
- Teen Coder: 🟣 Mor (#667EEA)
- Senior Dev: 🟢 Yeşil (#45B7D1)
- Legend: 🟡 Altın (#FFD700)
- Background: Mor/Mavi Gradient

## Sesler

- Dokunma: Kısa "bip"
- Kırılma: "Crack" + yükselen ton
- Feed: "Chomp chomp"
- Play: Neşeli melodi
- Code: "Typewriter" + success
- Evolution: Fanfare + confetti

