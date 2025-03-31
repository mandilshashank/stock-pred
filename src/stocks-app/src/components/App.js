import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Dashboard from './Dashboard';

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
        <div>
            <Header />
            <h1>Welcome to the App</h1>
            <Dashboard stocks={stockData} />
            <Footer />
        </div>
    );
}

export default App;