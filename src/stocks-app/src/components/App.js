import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import RegistrationPage from './pages/RegistrationPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './dashboard/Dashboard';
import PageNotFound from './pages/PageNotFound';
import Footer from './common/Footer';
import Header from './common/Header';
import ResetPasswordPage from './pages/ResetPasswordPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';

const stockData = [
    { symbol: 'AAPL', price: 150.00 },
    { symbol: 'GOOGL', price: 2800.00 },
    { symbol: 'AMZN', price: 3500.00 },
    { symbol: 'META', price: 3500.00 },
    { symbol: 'GOOG', price: 3500.00 },
    { symbol: 'NVDA', price: 3500.00 },
    { symbol: 'NFLX', price: 3500.00 },
];

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const handleLoginStatusChange = (status) => {
    setIsLoggedIn(status);
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  return (
    <Router>
      <Header isLoggedIn={isLoggedIn} onLoginStatusChange={handleLoginStatusChange} />
      <Switch>
        <Route path="/register" component={RegistrationPage} />
        <Route path="/login" render={(props) => <LoginPage {...props} onLoginStatusChange={handleLoginStatusChange} />} />
        <Route path="/reset-password/:token" component={ResetPasswordPage} />
        <Route path="/forgot-password" component={ForgotPasswordPage} />
        <Route path="/dashboard" render={() => <Dashboard stocks={stockData} />} />
        <Route exact path="/" render={() => (
          <div>
            <Dashboard stocks={stockData} />
          </div>
        )} />
        <Route component={PageNotFound} />
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;