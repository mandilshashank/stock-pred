import React, { useState } from 'react';
import axios from 'axios';
import '../../styles/RegistrationPage.css';

const RegistrationPage = ({ history }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    try {
      const response = await axios.post('http://localhost:5005/api/register', { email, password });
      setSuccess(true);
    } catch (err) {
      setError(err.response.data.message || 'Registration failed');
    }
  };

  if (success) {
    return (
      <div className="form-container">
        <div className="form-box">
          <h2>Registration Successful</h2>
          <p>Your registration was successful. <a href="/login">Click here to login</a>.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="form-container">
      <div className="form-box">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Confirm Password:</label>
            <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="button">Register</button>
        </form>
      </div>
    </div>
  );
};

export default RegistrationPage;