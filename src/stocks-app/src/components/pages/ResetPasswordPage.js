import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ResetPasswordPage = ({ history }) => {
  const { token } = useParams();
  const [newPassword, setNewPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleResetPassword = async (e) => {
    e.preventDefault();
    try {
      const apiUrl = process.env.NODE_ENV === 'production'
          ? 'http://ec2-54-175-107-161.compute-1.amazonaws.com:5005/api/reset-password'
          : 'http://localhost:5005/api/reset-password';
      const response = await axios.post(apiUrl, { token, newPassword });
      setSuccess('Password has been reset successfully');
      setTimeout(() => {
        history.push('/login');
      }, 2000);
    } catch (err) {
      setError('Error resetting password');
    }
  };

  return (
    <div className="form-container">
      <div className="form-box">
        <h2>Reset Password</h2>
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        <form onSubmit={handleResetPassword}>
          <div className="form-group">
            <label>New Password:</label>
            <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
          </div>
          <button type="submit" className="button">Reset Password</button>
        </form>
      </div>
    </div>
  );
};

export default ResetPasswordPage;