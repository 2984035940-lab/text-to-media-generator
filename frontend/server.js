const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API proxy endpoints
app.post('/api/generate-video', async (req, res) => {
    try {
        const axios = require('axios');
        const response = await axios.post(`${API_BASE_URL}/api/generate-video`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/generate-image', async (req, res) => {
    try {
        const axios = require('axios');
        const response = await axios.post(`${API_BASE_URL}/api/generate-image`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/tasks/:taskId', async (req, res) => {
    try {
        const axios = require('axios');
        const response = await axios.get(`${API_BASE_URL}/api/tasks/${req.params.taskId}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/generations/:generationId', async (req, res) => {
    try {
        const axios = require('axios');
        const response = await axios.get(`${API_BASE_URL}/api/generations/${req.params.generationId}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Frontend server running on port ${PORT}`);
    console.log(`API Base URL: ${API_BASE_URL}`);
});
