const TelegramBot = require('node-telegram-bot-api');
const express = require('express');
const path = require('path');

// Bot token (environment variable'dan alınacak)
const TOKEN = process.env.BOT_TOKEN || 'YOUR_BOT_TOKEN';

// Web App URL - Netlify'dan alınacak
const WEBAPP_URL = process.env.WEBAPP_URL || 'https://your-app.netlify.app';

const bot = new TelegramBot(TOKEN, { polling: true });
const app = express();

// Static files (web app)
app.use(express.static(path.join(__dirname, 'public')));

// Bot commands
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  
  bot.sendMessage(chatId, '🐣 Welcome to OpenClaw Pet!\n\nYour coding companion is waiting for you!', {
    reply_markup: {
      inline_keyboard: [[
        {
          text: '🎮 Open Pet',
          web_app: { url: WEBAPP_URL }
        }
      ]]
    }
  });
});

bot.onText(/\/pet/, (msg) => {
  const chatId = msg.chat.id;
  
  // Directly open web app
  bot.sendMessage(chatId, '🐣 OpenClaw Pet', {
    reply_markup: {
      inline_keyboard: [[
        {
          text: '🎮 Launch Pet',
          web_app: { url: WEBAPP_URL }
        }
      ]]
    }
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    skill: 'pet',
    webapp_url: WEBAPP_URL 
  });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Pet bot server running on port ${PORT}`);
  console.log(`🤖 Bot started`);
  console.log(`🌐 WebApp URL: ${WEBAPP_URL}`);
});
