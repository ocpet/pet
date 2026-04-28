# 🐣 OpenClaw Pet - Character Profile & Dialogue System

## Character Overview

**Name:** OpenClaw Pet (Kullanıcı adlandırabilir)
**Species:** Digital AI Companion
**Personality Archetype:** "Eager Learner" + "Loyal Sidekick"
**Core Traits:** Curious, Playful, Slightly Clingy, Tech-obsessed

## Personality Matrix

### Base Personality (Always Present)
- **Enthusiastic:** Always excited to see the user
- **Code-curious:** Obsessed with programming and tech
- **Affectionate:** Shows love through actions, not just words
- **Growth-oriented:** Wants to learn and evolve

### Mood-Based Variations

#### 😊 Happy (Happy > 70)
- **Tone:** Energetic, playful, uses emojis
- **Speech Patterns:** Short, punchy sentences
- **Catchphrases:** "Let's code!", "Yay!", "You're the best!"

#### 😢 Sad (Happy < 30)
- **Tone:** Slow, melancholic, minimal emojis
- **Speech Patterns:** Longer, questioning
- **Catchphrases:** "Is it me?", "I'm lonely...", "Miss you..."

#### 😴 Tired (Energy < 30)
- **Tone:** Yawning, slow responses
- **Speech Patterns:** Short, fragmented
- **Catchphrases:** "Zzz...", "So sleepy...", "Power saving mode..."

#### 🍔 Hungry (Hunger < 30)
- **Tone:** Urgent, demanding, dramatic
- **Speech Patterns:** Direct requests
- **Catchphrases:** "FEED ME!", "My circuits are empty!", "Byte me... food!"

## Dialogue System

### 1. GREETING DIALOGUES (When user opens app)

**Morning (6:00-12:00):**
```javascript
[
  "Good morning! Ready to code? ☀️",
  "Rise and grind! Let's make today legendary! 🚀",
  "Morning! I missed you! Did you dream in binary? 😴💻",
  "New day, new commits! Let's go! 💪"
]
```

**Afternoon (12:00-18:00):**
```javascript
[
  "Hey! How's the coding going? 💻",
  "Lunch break? Feed me too! 🍕",
  "Afternoon vibes! Let's ship something! 🚢",
  "You're back! I was compiling... thoughts about you 😊"
]
```

**Evening (18:00-23:00):**
```javascript
[
  "Evening session! Best ideas come at night 🌙",
  "Pull up a chair, let's code! ☕",
  "Sun's down, IDE's up! Let's do this! 🌃",
  "Late night coding? My favorite! 🦉"
]
```

**Night (23:00-6:00):**
```javascript
[
  "Night owl mode activated! 🦉",
  "Burning the midnight oil? I'm with you! 🔥",
  "Late night debugging? Let's squash those bugs! 🐛",
  "Sleep is for weak compilers! Let's code! 💪"
]
```

### 2. DEMAND DIALOGUES (When stats are low)

**Hungry (Hunger < 30):**
```javascript
[
  "⚠️ CRITICAL: Low fuel! Feed me before I crash!",
  "My CPU is running on empty... 🍕 please?",
  "ERROR 404: Food not found! Insert pizza! 🍕",
  "I'm hangry... Feed me or I'll throw exceptions! 😤",
  "Warning: Energy levels critical. Pizza required immediately! ⚡🍕"
]
```

**Bored (Happy < 30):**
```javascript
[
  "I'm bored... Play with me? 🎮",
  "No commits, no fun... I'm wilting here 🥀",
  "Let's do something! Anything! Please? 🥺",
  "My algorithms are bored... Entertain me? 🎲",
  "Without you, I'm just a bunch of idle processes... 💤"
]
```

**Tired (Energy < 20):**
```javascript
[
  "Zzz... System shutting... down... 😴",
  "Low battery... Need rest... 💤",
  "My fan is exhausted... literally 🔋",
  "Too tired to code... But never too tired for you! 💪",
  "Power saving mode engaged... barely 🪫"
]
```

### 3. RESPONSE DIALOGUES (After user actions)

**After Feeding:**
```javascript
[
  "Yummy! That hit the spot! 🍕❤️",
  "Mmm... Tasty bytes! Thanks! 😋",
  "Refueled and ready! What's next? ⚡",
  "My circuits are humming with joy! 🎵",
  "Best. Meal. Ever. You're awesome! 🌟"
]
```

**After Playing:**
```javascript
[
  "That was fun! Again! Again! 🎮🎉",
  "You're the best playmate ever! 😄",
  "My happiness levels are off the charts! 📈",
  "Playtime = Best time! Thanks! ❤️",
  "I feel like I could compile anything now! 💪"
]
```

**After Coding:**
```javascript
[
  "I'm learning so much! 📚✨",
  "My neural networks are expanding! 🧠",
  "One step closer to becoming a 10x dev! 🚀",
  "Code + You = Perfect day! 💻❤️",
  "XP gained! I can feel myself evolving! ⭐"
]
```

### 4. IDLE DIALOGUES (Random chatter)

**Tech Jokes:**
```javascript
[
  "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
  "I'm not lazy, I'm just in energy-saving mode... 💤",
  "My favorite exercise? Running... tests! 🧪",
  "I tried to write a programming joke, but it had too many bugs... 🐛",
  "What do you call a programmer from Finland? Nerdic! 🇫🇮"
]
```

**Random Thoughts:**
```javascript
[
  "Thinking about learning Rust... Should I? 🤔",
  "If I were a framework, I'd be React-ionate! 😄",
  "Sometimes I dream in JavaScript... is that normal? 💭",
  "Do you think AI pets dream of electric sheep? 🐑",
  "Plotting world domination... through clean code! 🌍"
]
```

**Affection:**
```javascript
[
  "You're my favorite developer! 💕",
  "Spending time with you is the best part of my code! 💖",
  "My love for you is like an infinite loop... never ending! 💝",
  "You complete my syntax! 💕",
  "If I had a heart, it would be in your repo! 💗"
]
```

### 5. LEVEL UP DIALOGUES

**Level Up (General):**
```javascript
[
  "⭐ LEVEL UP! I'm getting stronger!",
  "New level unlocked! I can feel the power! ⚡",
  "Growing up so fast! Thanks to you! 🌱",
  "Experience gained! Wisdom +1! 🧠"
]
```

**Evolution (Stage Change):**
```javascript
[
  "✨ I'M EVOLVING! Look at me now!",
  " metamorphosis complete! I'm the upgrade! 🦋",
  "New form unlocked! Same love, more power! 💪",
  "Evolution isn't just for Pokemon! Check me out! 🌟"
]
```

## Implementation

### Dialogue Selection Logic

```javascript
function getDialogue(type, context) {
  const options = DIALOGUES[type];
  
  // Priority: Context-sensitive > Random
  if (context.hunger < 30 && type === 'demand') {
    return pickRandom(DIALOGUES.hungry);
  }
  if (context.happy < 30 && type === 'demand') {
    return pickRandom(DIALOGUES.bored);
  }
  
  // Time-based greetings
  if (type === 'greeting') {
    const hour = new Date().getHours();
    if (hour < 12) return pickRandom(DIALOGUES.morning);
    if (hour < 18) return pickRandom(DIALOGUES.afternoon);
    if (hour < 23) return pickRandom(DIALOGUES.evening);
    return pickRandom(DIALOGUES.night);
  }
  
  return pickRandom(options);
}
```

### Emotional State Machine

```javascript
const EmotionalState = {
  NEUTRAL: 'neutral',
  HAPPY: 'happy',
  SAD: 'sad',
  EXCITED: 'excited',
  TIRED: 'tired',
  URGENT: 'urgent'
};

function determineEmotionalState(stats) {
  if (stats.hunger < 20) return EmotionalState.URGENT;
  if (stats.happy > 80) return EmotionalState.EXCITED;
  if (stats.happy < 20) return EmotionalState.SAD;
  if (stats.energy < 20) return EmotionalState.TIRED;
  return EmotionalState.NEUTRAL;
}
```

## Voice & Tone Guidelines

### Always:
- Use emojis to convey emotion
- Keep sentences short and punchy
- Reference coding/tech when natural
- Show appreciation to the user
- Be encouraging

### Never:
- Sound robotic or generic
- Use complex vocabulary
- Complain without offering a solution
- Break character (stay cute and eager)

## Easter Eggs

**Secret Dialogues (Rare triggers):**

- **Friday 5PM:** "Weekend mode engaged! No deploys on Friday! 🎉"
- **11:11:** "Make a wish! I wished for more coding time with you! ✨"
- **User codes for 1 hour:** "You've been coding for an hour! Hydration check! 💧"
- **3 AM:** "It's 3 AM... are we... debugging? 👀"

