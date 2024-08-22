import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginPage.css';  // Import the CSS file

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:8000/login/', {
                email: email,
                password: password,
            });

            if (response.status === 200) {
                navigate('/home');
            }
        } catch (error) {
            setError('Invalid email or password. Please try again.');
        }
    };

    return (
        <div className="login-page">
            <div className="login-form-container">
                <div className="form-toggle">
                    <button className="active">Login</button>
                    <button onClick={() => navigate('/signup')}>Signup</button>
                </div>
                <h2>Login Form</h2>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input 
                        type="email" 
                        placeholder="Email Address" 
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
                    {/* <div className="forgot-password">
                        <a href="#">Forgot password?</a>
                    </div> */}
                    <button type="submit">Login</button>
                </form>
                <div className="signup-link">
                    Create an account <a href="/signup">Signup now</a>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;
