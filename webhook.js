// OpenClaw Pet Skill Webhook
// Returns Telegram Mini App URL when user types "pet"

const express = require('express');
const app = express();

// Web App URL (deploy edince güncellenecek)
const WEBAPP_URL = process.env.PET_WEBAPP_URL || 'https://pet.example.com';

app.use(express.json());

// OpenClaw webhook endpoint
app.post('/webhook', (req, res) => {
  const { command, user_id } = req.body;
  
  if (command === 'pet' || command === '/pet') {
    res.json({
      type: 'web_app',
      url: WEBAPP_URL,
      text: '🐣 Your coding companion is waiting!',
      button_text: '🎮 Open Pet'
    });
  } else {
    res.json({
      type: 'text',
      text: 'Usage: /pet or pet'
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', skill: 'pet' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🐣 Pet skill webhook running on port ${PORT}`);
});
