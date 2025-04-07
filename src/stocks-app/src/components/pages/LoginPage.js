// src/stocks-app/src/components/pages/LoginPage.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../../styles/LoginPage.css';

const LoginPage = ({ history, onLoginStatusChange }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const apiUrl = process.env.NODE_ENV === 'production'
          ? 'http://ec2-54-175-107-161.compute-1.amazonaws.com:5005/api/login'
          : 'http://localhost:5005/api/login';
      const response = await axios.post(apiUrl, { email, password });
      localStorage.setItem('token', response.data.token); // Save the token in localStorage
      onLoginStatusChange(true);
      history.push('/dashboard'); // Redirect to the dashboard
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="form-container">
      <div className="form-box">
        <h2>Login</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="button">Login</button>
        </form>
        <div className="forgot-password-link">
          <Link to="/forgot-password">Forgot Password?</Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;