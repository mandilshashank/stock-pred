// src/stocks-app/src/components/Dashboard.js
import React from 'react';
import StockPrediction from './StockPrediction';
import '../styles/Dashboard.css';

const Dashboard = ({ stocks }) => {
  return (
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
  );
};

export default Dashboard;