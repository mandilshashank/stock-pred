import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import axios from 'axios';
import '../../styles/Header.css';

const Header = ({ isLoggedIn, onLoginStatusChange }) => {
  const history = useHistory();
  const [email, setEmail] = useState('');

  useEffect(() => {
    const fetchUserEmail = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://localhost:5005/api/user', {
            headers: { Authorization: `Bearer ${token}` }
          });
          setEmail(response.data.email);
        } catch (err) {
          console.error('Error fetching user email:', err.response.data.message);
        }
      }
    };

    if (isLoggedIn) {
      fetchUserEmail();
    }
  }, [isLoggedIn]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    onLoginStatusChange(false);
    history.push('/login');
  };

  return (
    <header>
      <h1>Stock App</h1>
      <nav>
        {isLoggedIn ? (
          <>
            <div className="profile-dropdown">
              <button className="profile-button">{email}</button>
              <div className="dropdown-content">
                <button onClick={handleLogout}>Logout</button>
              </div>
            </div>
          </>
        ) : (
          <>
            <Link to="/register" className="button">Register</Link>
            <Link to="/login" className="button">Login</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;