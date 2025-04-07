import React, { useState } from 'react';
import axios from 'axios';

const RegistrationPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [isSubmitDisabled, setIsSubmitDisabled] = useState(false);
  const [error, setError] = useState('');

  const validateEmail = async (email) => {
    try {
      await axios.post('http://localhost:5005/api/validate-email', { email });
      setEmailError('');
      setIsSubmitDisabled(false);
    } catch (error) {
      setEmailError(error.response.data.message);
      setIsSubmitDisabled(true);
    }
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    validateEmail(e.target.value);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!emailError && password === confirmPassword) {
      try {
        await axios.post('http://localhost:5005/api/register', { email, password });
        // Handle successful registration
      } catch (error) {
        setError('Error registering user: ' + error.response.data.message);
      }
    } else if (password !== confirmPassword) {
      setError('Passwords do not match');
    }
  };

  return (
    <div className="form-container">
      <div className="form-box">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" value={email} onChange={handleEmailChange} required />
            {emailError && <div className="error-message">{emailError} <a href="/forgot-password">Forgot Password?</a></div>}
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
          <button type="submit" className="button" disabled={isSubmitDisabled}>Register</button>
        </form>
      </div>
    </div>
  );
};

export default RegistrationPage;