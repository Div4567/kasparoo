const fs = require('fs');
const p = '/home/anjishnu-nandi/Documents/GitHub/get_smth/backend/index.js';
let it = fs.readFileSync(p, 'utf8');

it = it.replace("res.status(500).json({ error: 'Server Error' });", "console.error('Order fetch error:', error); res.status(500).json({ error: 'Server Error', details: error.message });");

it = it.replace("res.status(500).json({ error: 'Failed to communicate with AI Service.' });", "console.error('Chat service error:', error); res.status(500).json({ error: 'Failed to communicate with external chat service.', details: error.message });");

fs.writeFileSync(p, it);
