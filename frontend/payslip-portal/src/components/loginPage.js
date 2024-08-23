import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // Ensure the CSS is aligned with the SignupPage.css

function Login({ setAuthTokens }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAuthTokens(data); // Store tokens after successful login
        navigate('/home'); // Redirect to home after successful login
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Invalid credentials');
      }
    } catch (err) {
      setError('An error occurred: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="wrapper">
      <div className="title-text">
        <div className="title login">Login Form</div>
      </div>
      <div className="form-container">
        <div className="form-inner">
          <form onSubmit={handleLogin} className="login">
            <div className="field">
              <input
                type="email"
                placeholder="Email Address"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </div>
            <div className="field">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </div>
            <div className="pass-link"><a href="#">Forgot password?</a></div>
            <div className="field btn">
              <div className="btn-layer"></div>
              <input type="submit" value={loading ? 'Logging in...' : 'Login'} disabled={loading} />
            </div>
            {error && <p className="error-message">{error}</p>}
            <div className="signup-link">Not a member? <a href="/signup">Signup now</a></div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
