const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const axios = require('axios');
const connectDB = require('./db');
const Order = require('./models/Order');
const Ticket = require('./models/Ticket');
const Product = require('./models/Product');

dotenv.config();
connectDB();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'Backend API Gateway' });
});

// Fetch Products from MongoDB
app.get('/api/products', async (req, res) => {
    try {
        const products = await Product.find().limit(2);
        res.json(products);
    } catch (error) {
        console.error("Error fetching products:", error);
        console.error('Order fetch error:', error); res.status(500).json({ error: 'Server Error', details: error.message });
    }
});

// Fetch Orders for user
app.get('/api/orders/:userId', async (req, res) => {
    try {
        const orders = await Order.find({ userId: req.params.userId }).sort({ createdAt: -1 });
        res.json(orders);
    } catch (error) {
        res.status(500).json({ error: 'Server Error' });
    }
});


// --- Active Order Management Endpoints ---

// Cancel Order
app.put('/api/orders/:orderId/cancel', async (req, res) => {
    try {
        const order = await Order.findOneAndUpdate(
            { orderId: req.params.orderId },
            { status: 'Cancelled' },
            { new: true }
        );
        if (!order) return res.status(404).json({ error: 'Order not found' });
        res.json({ message: 'Order successfully cancelled', order });
    } catch (error) {
        res.status(500).json({ error: 'Server Error' });
    }
});

// Create Order (AI or User generated)
app.post('/api/orders', async (req, res) => {
    try {
        const { orderId, userId, products, total } = req.body;
        const newOrder = await Order.create({ orderId, userId, products, total, status: 'Processing' });
        res.status(201).json({ message: 'Order successfully created', order: newOrder });
    } catch (error) {
        res.status(500).json({ error: 'Server Error' });
    }
});

// Check for Replacements
app.get('/api/orders/:orderId/replacements', async (req, res) => {
    try {
        const order = await Order.findOne({ orderId: req.params.orderId });
        if (!order) return res.status(404).json({ error: 'Order not found' });
        
        // Simple mock returning alternative products
        const replacements = await Product.find().limit(3);
        res.json({ message: 'Available replacements found', replacements });
    } catch (error) {
        res.status(500).json({ error: 'Server Error' });
    }
});

// Create Escaltion Ticket
app.post('/api/tickets', async (req, res) => {
    try {
        const { userId, issue, priority } = req.body;
        const ticket = await Ticket.create({ userId, issue, priority });
        res.status(201).json(ticket);
    } catch (error) {
        res.status(500).json({ error: 'Server Error' });
    }
});

// Chat endpoint bridging to external chat service
app.post('/api/chat', async (req, res) => {
    try {
        const { message, userId, history } = req.body;
        
        // Send query to the external chat service
        const aiResponse = await axios.post(`${AI_SERVICE_URL}/chat`, {
            query: message,
            user_id: userId,
            history: history
        });

        res.json({
            reply: aiResponse.data.reply,
            intent: aiResponse.data.intent,
            escalate: aiResponse.data.escalate
        });
    } catch (error) {
        console.error("Chat service error:", error.message);
        console.error('Chat service error:', error); res.status(500).json({ error: 'Failed to communicate with external chat service.', details: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Backend API Gateway running on port ${PORT}`);
});
