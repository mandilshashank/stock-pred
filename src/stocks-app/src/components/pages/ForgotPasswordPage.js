// In `src/stocks-app/src/components/pages/ForgotPasswordPage.js`

import React, { useState } from 'react';
import axios from 'axios';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5005/api/forgot-password', { email });
      setMessage(response.data.message);
      setError('');
    } catch (error) {
      setError(error.response.data.message);
      setMessage('');
    }
  };

  return (
    <div className="form-container">
      <div className="form-box">
        <h2>Forgot Password</h2>
        <form onSubmit={handleForgotPassword}>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          {message && <div className="success-message">{message}</div>}
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="button">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;