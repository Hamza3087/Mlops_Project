// App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from "../src/Components/login";
import Register from "./Components/register";
import WeatherPrediction from "./Components/weather_prediction";

function App() {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <div>
        <nav>
          {user ? (
            <>
              <p>Welcome, {user.username}</p>
              <Link to="/weather">Go to Weather Prediction</Link>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </nav>
        <Routes>
          <Route path="/" element={<Login setUser={setUser} />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/weather" element={user ? <WeatherPrediction /> : <Login setUser={setUser} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;