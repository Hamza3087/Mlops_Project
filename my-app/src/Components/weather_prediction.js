import React, { useState } from 'react';

function WeatherPrediction() {
    const [humidity, setHumidity] = useState("");
    const [windSpeed, setWindSpeed] = useState("");
    const [prediction, setPrediction] = useState("");

    const handlePredict = async () => {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ humidity, wind_speed: windSpeed }),
        });
        const data = await response.json();
        setPrediction(data.temperature);
    };


    return (
        <div>
            <h1>Weather Predictor</h1>
            <input
                type="text"
                placeholder="Humidity"
                value={humidity}
                onChange={(e) => setHumidity(e.target.value)}
            />
            <input
                type="text"
                placeholder="Wind Speed"
                value={windSpeed}
                onChange={(e) => setWindSpeed(e.target.value)}
            />
            <button onClick={handlePredict}>Predict</button>
            <h2>Predicted Temperature: {prediction}</h2>
        </div>
    );
}

export default WeatherPrediction;