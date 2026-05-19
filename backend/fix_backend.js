const fs = require('fs');
const p = '/home/anjishnu-nandi/Documents/GitHub/get_smth/backend/index.js';
let it = fs.readFileSync(p, 'utf8');

const productsEndpoint = `
// Fetch Products (Mock)
app.get('/api/products', (req, res) => {
    res.json([
        { _id: 'p1', name: 'Wireless Headphones', price: 129.99 },
        { _id: 'p2', name: 'Running Shoes', price: 89.99 }
    ]);
});

// Fetch Orders for user
`;

it = it.replace('// Fetch Orders for user', productsEndpoint.trim() + '\n\n// Fetch Orders for user');
fs.writeFileSync(p, it);
