// src/stocks-app/server.js
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql2/promise');
const cors = require('cors'); // Import the cors package

const app = express();
const port = 5005;

app.use(bodyParser.json());
// Use the cors middleware with specific origin and methods
app.use(cors({
  origin: 'http://localhost:3000',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Handle preflight requests
app.options('*', cors());

const db = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'root1234',
  database: 'stock_pred'
});

app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }
  const hashedPassword = await bcrypt.hash(password, 10);
  try {
    const [rows] = await db.query('INSERT INTO users (email, password) VALUES (?, ?)', [email, hashedPassword]);
    res.status(201).send('User registered successfully');
  } catch (error) {
    res.status(400).json({ message: 'Error registering user', error: error.message });
  }
});

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const [rows] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
    if (rows.length > 0 && await bcrypt.compare(password, rows[0].password)) {
      res.status(200).send('Login successful');
    } else {
      res.status(400).send('Invalid email or password');
    }
  } catch (error) {
    res.status(400).send('Error logging in');
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});