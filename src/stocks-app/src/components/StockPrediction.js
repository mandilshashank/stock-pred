import React, { useState, useEffect } from 'react';
import axios from 'axios';

const StockPrediction = ({ symbol }) => {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const response = await axios.get(`http://localhost:5003/datapredict/${symbol}/1week`);
        setPrediction(response.data);
      } catch (err) {
        setError('Failed to fetch prediction');
        console.error(err);
      }
    };

    fetchPrediction();
  }, [symbol]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!prediction) {
    return <div>Loading prediction...</div>;
  }

  return (
    <div>
      <h3>Prediction for {symbol}</h3>
      <p>Predicted value: {prediction.prediction}</p>
      <p>MSE: {prediction.mse}</p>
      <p>RMSE: {prediction.rmse}</p>
    </div>
  );
};

export default StockPrediction;