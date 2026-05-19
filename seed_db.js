const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        await mongoose.connect('mongodb://localhost:27017/get_smth', {
            serverSelectionTimeoutMS: 5000
        });
        console.log('✓ Connected to MongoDB');
    } catch (error) {
        console.error('✗ Failed to connect:', error.message);
        process.exit(1);
    }
};

// Define schemas inline
const OrderSchema = new mongoose.Schema({
    orderId: String,
    userId: String,
    status: String,
    createdAt: Date
}, { collection: 'orders' });

const ProductSchema = new mongoose.Schema({
    name: String,
    price: Number,
    imageUrl: String
}, { collection: 'products' });

const Order = mongoose.model('Order', OrderSchema);
const Product = mongoose.model('Product', ProductSchema);

const seedData = async () => {
    try {
        // Clear existing data
        await Order.deleteMany({});
        await Product.deleteMany({});
        
        // Insert sample orders
        const orders = [
            { orderId: 'KSP-883921', userId: 'user123', status: 'Shipped', createdAt: new Date(2026, 4, 15) },
            { orderId: 'KSP-883922', userId: 'user123', status: 'Delivered', createdAt: new Date(2026, 4, 10) },
            { orderId: 'KSP-883923', userId: 'user123', status: 'Processing', createdAt: new Date(2026, 4, 18) }
        ];
        await Order.insertMany(orders);
        console.log('✓ Inserted sample orders');
        
        // Insert sample products
        const products = [
            { name: 'Wireless Headphones', price: 129.99 },
            { name: 'Running Shoes', price: 89.99 },
            { name: 'Smart Watch', price: 199.99 }
        ];
        await Product.insertMany(products);
        console.log('✓ Inserted sample products');
        
        mongoose.disconnect();
        console.log('✓ Database seeded successfully');
    } catch (error) {
        console.error('✗ Seeding error:', error.message);
        process.exit(1);
    }
};

connectDB().then(() => seedData());
