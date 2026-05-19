const mongoose = require('mongoose');

const ticketSchema = new mongoose.Schema({
    userId: { type: String, required: true },
    issue: { type: String, required: true },
    priority: { type: String, enum: ['low', 'medium', 'high'], default: 'low' },
    status: { type: String, enum: ['open', 'in-progress', 'resolved'], default: 'open' },
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Ticket', ticketSchema);
