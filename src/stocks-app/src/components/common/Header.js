import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/Header.css';

const Header = () => {
  return (
    <header>
      <h1>Stock App</h1>
      <nav>
        <Link to="/register" className="button">Register</Link>
        <Link to="/login" className="button">Login</Link>
      </nav>
    </header>
  );
};

export default Header;