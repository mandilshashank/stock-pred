require('dotenv').config();

const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql2/promise');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const nodemailer = require('nodemailer');


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

  try {
    const [emailRows] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
    if (emailRows.length > 0) {
      return res.status(400).json({ message: 'This email address is already registered. Please log in or use the "Forgot Password" option.' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    await db.query('INSERT INTO users (email, password) VALUES (?, ?)', [email, hashedPassword]);
    res.status(201).send('User registered successfully');
  } catch (error) {
    res.status(500).json({ message: 'Error registering user', error: error.message });
  }
});

app.post('/api/validate-email', async (req, res) => {
  const { email } = req.body;
  try {
    const [rows] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
    if (rows.length > 0) {
      return res.status(400).json({ message: 'This email address is already registered. Please log in or use the "Forgot Password" option.' });
    }
    res.status(200).send('Email is available');
  } catch (error) {
    res.status(500).json({ message: 'Error validating email', error: error.message });
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

app.post('/api/forgot-password', async (req, res) => {
  const { email } = req.body;
  try {
    const [user] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
    if (user.length === 0) {
      return res.status(400).json({ message: 'No user found with this email address.' });
    }
    const token = crypto.randomBytes(20).toString('hex');
    const tokenExpiration = Date.now() + 3600000; // 1 hour

    await db.query('UPDATE users SET resetPasswordToken = ?, resetPasswordExpires = ? WHERE email = ?', [token, tokenExpiration, email]);

    const transporter = nodemailer.createTransport({
      service: 'Gmail',
      auth: {
        user: 'mandil.shashank@gmail.com',
        pass: process.env.EMAIL_PASSWORD,
      },
    });

    const resetUrl = process.env.NODE_ENV === 'production'
          ? `http://ec2-54-175-107-161.compute-1.amazonaws.com/reset-password/${token}`
          : `http://localhost:3000/reset-password/${token}`;

    const mailOptions = {
          to: email,
          from: 'passwordreset@stock-app.com',
          subject: 'Password Reset',
          text: `You are receiving this because you (or someone else) have requested the reset of the password for your account.\n\n
                 Please click on the following link, or paste this into your browser to complete the process:\n\n
                 ${resetUrl}\n\n
                 If you did not request this, please ignore this email and your password will remain unchanged.\n`,
        };

    await transporter.sendMail(mailOptions);
    res.status(200).json({ message: 'Password reset email sent.' });
  } catch (error) {
    res.status(500).json({ message: 'Error processing request', error: error.message });
  }
});

app.post('/api/reset-password', async (req, res) => {
  const { token, newPassword } = req.body;

  if (!token || !newPassword) {
      return res.status(400).json({ message: 'Token and new password are required' });
  }

  try {
    const [user] = await db.query('SELECT * FROM users WHERE resetPasswordToken = ? AND resetPasswordExpires > ?', [token, Date.now()]);
    if (user.length === 0) {
      return res.status(400).json({ message: 'Password reset token is invalid or has expired.' });
    }

    const hashedPassword = await bcrypt.hash(newPassword, 10);
    await db.query('UPDATE users SET password = ?, resetPasswordToken = NULL, resetPasswordExpires = NULL WHERE email = ?', [hashedPassword, user[0].email]);

    res.status(200).json({ message: 'Password has been reset.' });
  } catch (error) {
    res.status(500).json({ message: 'Error resetting password', error: error.message });
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

app.delete('/api/portfolio/:ticker', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ message: 'Authorization header missing' });
  }

  const token = authHeader.split(' ')[1];
  const { ticker } = req.params;
  try {
    const decoded = jwt.verify(token, secretKey);
    await db.query('DELETE FROM portfolio WHERE user_id = ? AND ticker = ?', [decoded.userId, ticker]);
    res.status(200).json({ message: 'Stock deleted successfully' });
  } catch (error) {
    res.status(400).json({ message: 'Error deleting stock', error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});