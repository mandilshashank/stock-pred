const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql2/promise');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const app = express();
const port = 5005;
const secretKey = crypto.randomBytes(64).toString('hex');

app.use(bodyParser.json());
app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = [
      'http://localhost:3000',
      'http://ec2-54-175-107-161.compute-1.amazonaws.com'
    ];
    if (allowedOrigins.includes(origin) || !origin) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

app.options('*', (req, res) => {
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.header('Access-Control-Allow-Credentials', 'true');
  res.sendStatus(200);
});

const db = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'StockMarket1234!',
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
      const token = jwt.sign({ userId: rows[0].id }, secretKey, { expiresIn: '1h' });
      res.status(200).json({ message: 'Login successful', token });
    } else {
      res.status(400).send('Invalid email or password');
    }
  } catch (error) {
    res.status(400).send('Error logging in');
  }
});

app.get('/api/portfolio', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ message: 'Authorization header missing' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, secretKey);
    const [rows] = await db.query('SELECT * FROM portfolio WHERE user_id = ?', [decoded.userId]);
    res.status(200).json(rows);
  } catch (error) {
    res.status(400).json({ message: 'Error fetching portfolio', error: error.message });
  }
});

app.post('/api/portfolio', async (req, res) => {
  const token = req.headers.authorization.split(' ')[1];
  const { ticker, shares } = req.body;
  try {
    const decoded = jwt.verify(token, secretKey);
    await db.query('INSERT INTO portfolio (user_id, ticker, shares) VALUES (?, ?, ?)', [decoded.userId, ticker, shares]);
    res.status(201).send('Stock added successfully');
  } catch (error) {
    res.status(400).json({ message: 'Error adding stock', error: error.message });
  }
});

app.get('/api/user', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ message: 'Authorization header missing' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, secretKey);
    const [rows] = await db.query('SELECT email FROM users WHERE id = ?', [decoded.userId]);
    res.status(200).json(rows[0]);
  } catch (error) {
    res.status(400).json({ message: 'Error fetching user email', error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});