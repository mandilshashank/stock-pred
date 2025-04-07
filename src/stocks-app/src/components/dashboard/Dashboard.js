import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockPrediction from '../StockPrediction';
import '../../styles/Dashboard.css';

const Dashboard = ({ stocks }) => {
  const [portfolio, setPortfolio] = useState([]);
  const [ticker, setTicker] = useState('');
  const [shares, setShares] = useState('');
  const [error, setError] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('User not logged in');
      setIsLoggedIn(false);
      return;
    }
    setIsLoggedIn(true);

    const fetchPortfolio = async () => {
      try {
        const response = await axios.get('http://localhost:5005/api/portfolio', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setPortfolio(response.data);
      } catch (err) {
        setError('Error fetching portfolio: ' + err.response.data.message);
      }
    };

    fetchPortfolio();
  }, []);

  const handleAddStock = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) {
      setError('User not logged in');
      return;
    }

    try {
      await axios.post('http://localhost:5005/api/portfolio', { ticker, shares }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPortfolio([...portfolio, { ticker, shares }]);
      setTicker('');
      setShares('');
    } catch (err) {
      setError('Error adding stock: ' + err.response.data.message);
    }
  };

  const handleDeleteStock = async (ticker) => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('User not logged in');
      return;
    }

    try {
      await axios.delete(`http://localhost:5005/api/portfolio/${ticker}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPortfolio(portfolio.filter(stock => stock.ticker !== ticker));
    } catch (err) {
      setError('Error deleting stock: ' + err.response.data.message);
    }
  };

  return (
    <div>
      <div className="dashboard-container">
        <h2>My Portfolio</h2>
        {error && <div className="error-message">{error}</div>}
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Shares</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {portfolio.map((stock, index) => (
              <tr key={index}>
                <td>{stock.ticker}</td>
                <td>{stock.shares}</td>
                <td>
                  <button onClick={() => handleDeleteStock(stock.ticker)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <form onSubmit={handleAddStock}>
          <div className="form-group">
            <label>Ticker:</label>
            <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Shares:</label>
            <input type="number" value={shares} onChange={(e) => setShares(e.target.value)} required />
          </div>
          <button type="submit" className="button">Add Stock</button>
        </form>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map(stock => (
              <tr key={stock.symbol}>
                <td>{stock.symbol}</td>
                <td><StockPrediction symbol={stock.symbol} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;