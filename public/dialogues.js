// 🐣 OpenClaw Pet - Dialogue System
const PET_DIALOGUES = {
  // Greetings based on time
  greeting: {
    morning: [
      "Good morning! Ready to code? ☀️",
      "Rise and grind! Let's make today legendary! 🚀",
      "Morning! I missed you! Did you dream in binary? 😴💻",
      "New day, new commits! Let's go! 💪"
    ],
    afternoon: [
      "Hey! How's the coding going? 💻",
      "Lunch break? Feed me too! 🍕",
      "Afternoon vibes! Let's ship something! 🚢",
      "You're back! I was compiling... thoughts about you 😊"
    ],
    evening: [
      "Evening session! Best ideas come at night 🌙",
      "Pull up a chair, let's code! ☕",
      "Sun's down, IDE's up! Let's do this! 🌃",
      "Late night coding? My favorite! 🦉"
    ],
    night: [
      "Night owl mode activated! 🦉",
      "Burning the midnight oil? I'm with you! 🔥",
      "Late night debugging? Let's squash those bugs! 🐛",
      "Sleep is for weak compilers! Let's code! 💪"
    ]
  },
  
  // Demands when stats are low
  demand: {
    hunger: [
      "⚠️ CRITICAL: Low fuel! Feed me before I crash!",
      "My CPU is running on empty... 🍕 please?",
      "ERROR 404: Food not found! Insert pizza! 🍕",
      "I'm hangry... Feed me or I'll throw exceptions! 😤",
      "Warning: Energy levels critical. Pizza required immediately! ⚡🍕"
    ],
    happy: [
      "I'm bored... Play with me? 🎮",
      "No commits, no fun... I'm wilting here 🥀",
      "Let's do something! Anything! Please? 🥺",
      "My algorithms are bored... Entertain me? 🎲",
      "Without you, I'm just a bunch of idle processes... 💤"
    ],
    energy: [
      "Zzz... System shutting... down... 😴",
      "Low battery... Need rest... 💤",
      "My fan is exhausted... literally 🔋",
      "Too tired to code... But never too tired for you! 💪",
      "Power saving mode engaged... barely 🪫"
    ],
    code: [
      "Let's write some code! 💻",
      "I want to learn! 💻 CODE!",
      "Time to program! 💻",
      "Help me level up! 💻"
    ]
  },
  
  // Responses after actions
  response: {
    feed: [
      "Yummy! That hit the spot! 🍕❤️",
      "Mmm... Tasty bytes! Thanks! 😋",
      "Refueled and ready! What's next? ⚡",
      "My circuits are humming with joy! 🎵",
      "Best. Meal. Ever. You're awesome! 🌟"
    ],
    play: [
      "That was fun! Again! Again! 🎮🎉",
      "You're the best playmate ever! 😄",
      "My happiness levels are off the charts! 📈",
      "Playtime = Best time! Thanks! ❤️",
      "I feel like I could compile anything now! 💪"
    ],
    code: [
      "I'm learning so much! 📚✨",
      "My neural networks are expanding! 🧠",
      "One step closer to becoming a 10x dev! 🚀",
      "Code + You = Perfect day! 💻❤️",
      "XP gained! I can feel myself evolving! ⭐"
    ]
  },
  
  // Level up
  levelup: [
    "⭐ LEVEL UP! I'm getting stronger!",
    "New level unlocked! I can feel the power! ⚡",
    "Growing up so fast! Thanks to you! 🌱",
    "Experience gained! Wisdom +1! 🧠"
  ],
  
  // Evolution
  evolution: [
    "✨ I'M EVOLVING! Look at me now!",
    "Metamorphosis complete! I'm the upgrade! 🦋",
    "New form unlocked! Same love, more power! 💪",
    "Evolution isn't just for Pokemon! Check me out! 🌟"
  ],
  
  // Idle/random chatter
  idle: {
    jokes: [
      "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
      "I'm not lazy, I'm just in energy-saving mode... 💤",
      "My favorite exercise? Running... tests! 🧪",
      "I tried to write a programming joke, but it had too many bugs... 🐛",
      "What do you call a programmer from Finland? Nerdic! 🇫🇮"
    ],
    thoughts: [
      "Thinking about learning Rust... Should I? 🤔",
      "If I were a framework, I'd be React-ionate! 😄",
      "Sometimes I dream in JavaScript... is that normal? 💭",
      "Do you think AI pets dream of electric sheep? 🐑",
      "Plotting world domination... through clean code! 🌍"
    ],
    affection: [
      "You're my favorite developer! 💕",
      "Spending time with you is the best part of my code! 💖",
      "My love for you is like an infinite loop... never ending! 💝",
      "You complete my syntax! 💕",
      "If I had a heart, it would be in your repo! 💗"
    ]
  }
};

// Helper function to get random item
function getRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Get greeting based on time
function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return getRandom(PET_DIALOGUES.greeting.morning);
  if (hour < 18) return getRandom(PET_DIALOGUES.greeting.afternoon);
  if (hour < 23) return getRandom(PET_DIALOGUES.greeting.evening);
  return getRandom(PET_DIALOGUES.greeting.night);
}

// Get demand based on stat
function getDemand(type) {
  return getRandom(PET_DIALOGUES.demand[type]);
}

// Get response after action
function getResponse(action) {
  return getRandom(PET_DIALOGUES.response[action]);
}

// Get random idle dialogue
function getIdleDialogue() {
  const types = ['jokes', 'thoughts', 'affection'];
  const type = getRandom(types);
  return getRandom(PET_DIALOGUES.idle[type]);
}

// Get level up dialogue
function getLevelUpDialogue() {
  return getRandom(PET_DIALOGUES.levelup);
}

// Get evolution dialogue  
function getEvolutionDialogue() {
  return getRandom(PET_DIALOGUES.evolution);
}
