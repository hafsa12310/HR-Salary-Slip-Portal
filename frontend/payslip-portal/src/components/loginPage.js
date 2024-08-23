import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login({ setAuthTokens }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false); // Added loading state
    const navigate = useNavigate(); // Added navigation for redirection

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true); // Start loading

        try {
            const response = await axios.post('http://localhost:8000/login/', {
                email,
                password
            });

            console.log('Response Data:', response.data); // Log the response data

            const { access, refresh } = response.data;

            if (access && refresh) {
                console.log('Saving Tokens:', { access, refresh }); // Log tokens before saving
                localStorage.setItem('authTokens', JSON.stringify({ access, refresh }));
                console.log('Tokens saved to localStorage:', localStorage.getItem('authTokens')); // Verify storage
                setAuthTokens({ access, refresh });
                setError('');
                navigate('/home'); // Redirect to home page upon successful login
            } else {
                setError('Invalid credentials'); // Handle missing tokens
            }
        } catch (err) {
            console.error('Error Response:', err.response); // Log the error response
            setError('Invalid credentials');
        } finally {
            setLoading(false); // Stop loading
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
            </button>
            {error && <p>{error}</p>}
        </form>
    );
}

export default Login;
