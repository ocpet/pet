// 🔔 OpenClaw Pet - Proactive Notification System
const BOT_TOKEN = process.env.BOT_TOKEN;
const PET_API_URL = process.env.PET_API_URL || 'https://openclawpet.netlify.app/api';

// Bildirim şablonları
const NOTIFICATIONS = {
  morning: {
    penguin: ["☀️ Günaydın! Buz gibi bir gün! Seni bekliyorum 🐧", "Rise and grind! ☕ Bugün kod zamanı! 🐧"],
    cat: ["*yawn* Sabah mı? Neden? 😴 Ama gelmişken... Miyav. 🐱", "Günaydın. Ama gece daha iyiydi. 🌙 🐱"],
    dog: ["GÜNAYDIN! UYANDIN! SEVİYORUM! 🐕🎉", "YENİ GÜN! YENİ OYUNLAR! HAV HAV! 🐕"],
    fish: ["*baloncuk* Gün doğumu... Huzur. ☀️ 🐠", "Sabah sessizliği... Seni bekliyorum. 🐠"],
    chick: ["CIK CIK! GÜNAYDIN! BÜYÜYORUM! 📈🐥", "YENİ GÜN! YENİ KEŞİFLER! 🐥🔍"]
  },
  
  hungry: {
    penguin: ["🚨 Buz gibi açım! Balık var mı? 🐧🐟", "ERROR 404: Food not found! 🐧🍕"],
    cat: ["*zamklı bakış* Miyav. (Yani: Açım.) 🐱🍕", "Aşık atmam ama... açım. 😏 🐱"],
    dog: ["AÇIM! HEMEN! ŞİMDİ! YEMEK! 🐕🍕🥺", "KARNIM ZIL ÇALIYOR! HAV HAV! 🐕🔔"],
    fish: ["*baloncuk* Açlık... Yem gerekli. 🐠🐟", "Yorgunluk... Açlık... Su gibi. 🐠"],
    chick: ["AÇIM! AÇIM! AÇIM! YEMEK! 🐥🍕📢", "CIK CIK! KARNIM GURULDU! 🐥🥁"]
  },
  
  bored: {
    penguin: ["Kaymak istiyorum! Wheee! 🐧⛸️", "Bored... Ice breaker? 🐧🎮"],
    cat: ["Sıkıldım. Ama seni eğlendirebilirim. Belki. 🐱🎮", "Eğlence? Ama önce beni sev. 🐱💅"],
    dog: ["SIKILDIM! OYNA! OYNA! OYNA! 🐕🎮🎾", "BENİMLE OYNA! LÜTFEN! HAV! 🐕🥺"],
    fish: ["*baloncuk* Hareket... Oyun... 🐠🎮", "Durgunluk... Sıkıntı... 🐠😔"],
    chick: ["CIK CIK! SIkILDIM! YENİ ŞEYLER! 🐥🔍", "OYUN! OYUN! DAHA FAZLA OYUN! 🐥🎮"]
  },
  
  missed: {
    penguin: ["Buz gibi yalnızım... 🐧❄️ Neredeydin?", "Soğukkanlılığımı kaybediyorum... Gel! 🐧😢"],
    cat: ["*yargılayıcı bakış* Neredeydin? 🐱👀", "Başka pet'ler mi var? Miyav. 🐱😒"],
    dog: ["SENİ ÖZLEDİM! ÇOK ÇOK ÇOK! 🐕💔", "YALNIZDIM! AĞLADIM! HAV! 😭🐕"],
    fish: ["*baloncuk* Yalnızlık... Derin... 🐠🌊", "Sessizlik... Bekleyiş... 🐠💭"],
    chick: ["NEREDEYDİN?! BEN BÜYÜDÜM! GÖRMEDİN! 🐥📈😤", "UNUTTUN MU?! CIK CIK! 🐥💔"]
  },
  
  streak: {
    penguin: ["🔥 Streak'in eriyor! Buz gibi tehlike! 🐧⚠️", "Kaybetme! Soğukkanlı kal ve gel! 🐧🔥"],
    cat: ["🔥 Streak'in düşüyor. Umurumda değil. (Değil mi?) 🐱🔥", "Kaybetme. Ama kaybedersen... miyav. 🐱😒"],
    dog: ["🔥 STREAK'İN TEHLİKEDE! GEL! HEMEN! 🐕🔥🚨", "KAYBETME! LÜTFEN! YALVARIYORUM! 🐕🥺🔥"],
    fish: ["🔥 Streak... Su gibi akıyor... Kaybetme. 🐠🔥", "Zaman... Akıyor... Gel. 🐠⏰"],
    chick: ["🔥 STREAK! STREAK! KAYBETME! CIK! 🐥🔥📢", "GÜNLERİN SAYISI! ARTMASI LAZIM! 🐥🔥📈"]
  },
  
  random_event: {
    penguin: ["🎁 Buzda bir şey buldum! Özel yemek! 🐧🐟", "🎁 Kutup ışıkları altında sürpriz! 🐧✨"],
    cat: ["🎁 Bir fare yakaladım! Yani... ödül! 🐱🎁", "🎁 Sana bir şey getirdim. Ama vermem. Şaka. 🐱😏"],
    dog: ["🎁 KEMİK BULDUM! SANA GETİRDİM! 🐕🦴", "🎁 HEDİYE! HEDİYE! AÇ AÇ! 🐕🎁🎉"],
    fish: ["🎁 Denizin derinliklerinden... bir şey. 🐠🎁", "🎁 Hazine buldum. Seninle paylaşacağım. 🐠💎"],
    chick: ["🎁 YUMURTA BULDUM! AÇMAK LAZIM! 🐥🥚", "🎁 KEŞİF! YENİ ŞEY! ACİL! 🐥🔍🎁"]
  }
};

// Rastgele mesaj seç
function getRandomMessage(type, petType) {
  const messages = NOTIFICATIONS[type][petType];
  return messages[Math.floor(Math.random() * messages.length)];
}

// Telegram bildirim gönder
async function sendNotification(chatId, message) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: message,
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [[
            { text: "🐣 Pet'i Aç", web_app: { url: 'https://openclawpet.netlify.app/' } }
          ]]
        }
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Notification failed:', error);
    return null;
  }
}

// Ana fonksiyon
async function main() {
  const type = process.argv[2]; // morning, hungry, bored, missed, streak, random
  
  // TODO: Database'den kullanıcıları ve pet'lerini çek
  // Şimdilik test verisi
  const testUsers = [
    { chatId: '8766113542', petType: 'penguin', petName: 'Penguv', lastLogin: '24h' }
  ];
  
  for (const user of testUsers) {
    const message = getRandomMessage(type, user.petType);
    const personalizedMessage = `${user.petName}: "${message}"`;
    
    await sendNotification(user.chatId, personalizedMessage);
    console.log(`Sent ${type} notification to ${user.chatId}`);
  }
}

main();
