import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleRegister = async () => {
        const response = await fetch("http://127.0.0.1:8000/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password }),  // Correctly send the JSON
        });
        const data = await response.json();
        if (response.ok) {
            setUsername("");
            setEmail("");
            setPassword("");
            navigate("/login");
        } else {
            setError(data.detail || "Registration failed");
        }
    };

    return (
        <div>
            <h1>Register</h1>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleRegister}>Register</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <p>
                Already have an account? <a href="/login">Login</a>
            </p>
        </div>
    );
}

export default Register;