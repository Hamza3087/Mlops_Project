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

    // Global body style for black background
    React.useEffect(() => {
        document.body.style.backgroundColor = '#000';
        return () => {
            document.body.style.backgroundColor = ''; // Reset when the component unmounts
        };
    }, []);

    const containerStyle = {
        fontFamily: 'Arial, sans-serif',
        textAlign: 'center',
        padding: '30px',
        backgroundColor: '#121212',
        borderRadius: '10px',
        maxWidth: '400px',
        margin: 'auto',
        boxShadow: '0 4px 8px rgba(255, 215, 30, 0.5)', // Glow effect around the card
    };

    const inputStyle = {
        padding: '10px',
        margin: '10px 0',
        width: '80%',
        fontSize: '16px',
        borderRadius: '5px',
        border: '1px solid #ccc',
        outline: 'none',
        backgroundColor: '#333',
        color: '#fff',
        transition: 'box-shadow 0.3s ease',
    };

    const buttonStyle = {
        padding: '10px 20px',
        fontSize: '16px',
        backgroundColor: '#f7d31e',
        color: '#121212',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease, transform 0.2s ease',
    };

    const resultStyle = {
        marginTop: '20px',
        fontSize: '20px',
        fontWeight: 'bold',
        color: '#f7d31e',
        textShadow: '0 0 10px #f7d31e', // Glow effect on result text
    };

    return (
        <div style={containerStyle}>
            <h1 style={{ color: '#f7d31e', textShadow: '0 0 10px #f7d31e' }}>Weather Predictor</h1>
            <input
                style={inputStyle}
                type="text"
                placeholder="Humidity"
                value={humidity}
                onChange={(e) => setHumidity(e.target.value)}
                onFocus={(e) => e.target.style.boxShadow = '0 0 15px #f7d31e'} // Glow effect on focus
                onBlur={(e) => e.target.style.boxShadow = 'none'} // Remove glow when focus is lost
            />
            <input
                style={inputStyle}
                type="text"
                placeholder="Wind Speed"
                value={windSpeed}
                onChange={(e) => setWindSpeed(e.target.value)}
                onFocus={(e) => e.target.style.boxShadow = '0 0 15px #f7d31e'} // Glow effect on focus
                onBlur={(e) => e.target.style.boxShadow = 'none'} // Remove glow when focus is lost
            />
            <button style={buttonStyle} onClick={handlePredict}>Predict</button>
            {prediction && (
                <h2 style={resultStyle}>Predicted Temperature: {prediction}°C</h2>
            )}
        </div>
    );
}

export default WeatherPrediction;
