import React from 'react';
import Header from './common/Header';
import Footer from './common/Footer';
import Dashboard from './dashboard/Dashboard';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import RegistrationPage from './pages/RegistrationPage';
import LoginPage from './pages/LoginPage';
import PageNotFound from './pages/PageNotFound';

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
    return (
        <Router>
            <Header />
            <Switch>
                <Route path="/register" component={RegistrationPage} />
                <Route path="/login" component={LoginPage} />
                <Route exact path="/" render={() => (
                    <div>
                        <h1>Welcome to the App</h1>
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