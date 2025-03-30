import React from 'react';
import StockPrediction from './StockPrediction';

const Dashboard = ({ stocks }) => {
  return (
    <div>
      <h2>Stock Dashboard</h2>
      {stocks.map(stock => (
        <div key={stock.symbol}>
          <h3>{stock.symbol}</h3>
          <StockPrediction symbol={stock.symbol} />
        </div>
      ))}
    </div>
  );
};

export default Dashboard;