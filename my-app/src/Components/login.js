import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login({ setUser }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }), // Ensure body is sent as JSON
        });
        const data = await response.json();
        if (response.ok) {
            setUser({ username });
            navigate("/weather");
        } else {
            setError(data.detail || "Login failed");
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h1 style={styles.title}>Login</h1>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={styles.input}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={styles.input}
                />
                <button onClick={handleLogin} style={styles.button}>
                    Login
                </button>
                {error && <p style={styles.error}>{error}</p>}
                <p style={styles.registerText}>
                    Don't have an account? <a href="/register" style={styles.registerLink}>Register</a>
                </p>
            </div>
        </div>
    );
}

const styles = {
    container: {
        backgroundColor: '#121212',
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: '#fff',
    },
    card: {
        backgroundColor: '#1f1f1f',
        padding: '30px',
        borderRadius: '10px',
        boxShadow: '0 6px 15px rgba(255, 215, 30, 0.4)', // Glow effect below card
        width: '300px',
        textAlign: 'center',
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
    },
    title: {
        marginBottom: '20px',
        color: '#f7d31e',
        fontSize: '24px',
        textShadow: '0 0 10px #f7d31e',
    },
    input: {
        width: '100%',
        padding: '10px',
        margin: '10px 0',
        border: 'none',
        borderRadius: '5px',
        outline: 'none',
        fontSize: '16px',
        color: '#fff',
        backgroundColor: '#333',
        transition: 'border-color 0.3s ease, box-shadow 0.3s ease',
    },
    button: {
        width: '100%',
        padding: '12px',
        border: 'none',
        borderRadius: '5px',
        backgroundColor: '#f7d31e',
        color: '#121212',
        fontSize: '18px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease, transform 0.2s ease',
    },
    buttonHover: {
        backgroundColor: '#ffbb33',
    },
    error: {
        color: 'red',
        fontSize: '14px',
    },
    registerText: {
        marginTop: '10px',
        fontSize: '14px',
        color: '#aaa',
    },
    registerLink: {
        color: '#f7d31e',
        textDecoration: 'none',
    },
};

// Adding glow effect below input fields on focus
const input = document.querySelectorAll('input');
input.forEach((el) => {
    el.addEventListener('focus', () => {
        el.style.boxShadow = '0 0 15px #f7d31e'; // Glow effect on focus
    });
    el.addEventListener('blur', () => {
        el.style.boxShadow = 'none'; // Remove glow effect when not focused
    });
});

export default Login;
