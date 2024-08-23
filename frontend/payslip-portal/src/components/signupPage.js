import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignupPage.css'; // Optional: Link your CSS file if you have specific styles

function Signup() {
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false); // Loading state
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(''); // Clear previous errors
    setSuccess(''); // Clear previous success messages
    setLoading(true); // Start loading

    if (password1 !== password2) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password: password1,
          first_name: firstName,
          last_name: lastName,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess('User registered successfully');
        console.log(data);
        navigate('/login'); // Redirect to the login page after successful registration
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'An error occurred during registration');
      }
    } catch (err) {
      setError('An error occurred: ' + err.message);
    } finally {
      setLoading(false); // End loading
    }
  };

  return (
    <div className="wrapper">
      <div className="title-text">
        <div className="title signup">Signup Form</div>
      </div>
      <div className="form-container">
        <div className="form-inner">
          <form onSubmit={handleSubmit} className="signup">
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
                value={password1}
                onChange={(event) => setPassword1(event.target.value)}
                required
              />
            </div>
            <div className="field">
              <input
                type="password"
                placeholder="Confirm Password"
                value={password2}
                onChange={(event) => setPassword2(event.target.value)}
                required
              />
            </div>
            <div className="field">
              <input
                type="text"
                placeholder="First Name"
                value={firstName}
                onChange={(event) => setFirstName(event.target.value)}
                required
              />
            </div>
            <div className="field">
              <input
                type="text"
                placeholder="Last Name"
                value={lastName}
                onChange={(event) => setLastName(event.target.value)}
                required
              />
            </div>
            <div className="field btn">
              <div className="btn-layer"></div>
              <input type="submit" value={loading ? 'Signing up...' : 'Signup'} disabled={loading} />
            </div>
            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}
          </form>
        </div>
      </div>
    </div>
  );
}

export default Signup;
