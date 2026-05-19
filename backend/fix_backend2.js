const fs = require('fs');
const p = '/home/anjishnu-nandi/Documents/GitHub/get_smth/backend/index.js';
let it = fs.readFileSync(p, 'utf8');

it = it.replace("const Ticket = require('./models/Ticket');", "const Ticket = require('./models/Ticket');\nconst Product = require('./models/Product');");

it = it.replace(/\/\/ Fetch Products \(Mock\).*?\/\/ Fetch Orders for user/s, `// Fetch Products from MongoDB
app.get('/api/products', async (req, res) => {
    try {
        const products = await Product.find().limit(2);
        res.json(products);
    } catch (error) {
        console.error("Error fetching products:", error);
        res.status(500).json({ error: 'Server Error' });
    }
});`);

fs.writeFileSync(p, it);
