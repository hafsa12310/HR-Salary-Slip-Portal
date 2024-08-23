import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Signup() {
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(''); // Clear previous errors
    setSuccess(''); // Clear previous success messages

    if (password1 !== password2) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password: password1, first_name: firstName, last_name: lastName })
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
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email:
        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        Password:
        <input
          type="password"
          value={password1}
          onChange={(event) => setPassword1(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        Confirm Password:
        <input
          type="password"
          value={password2}
          onChange={(event) => setPassword2(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        First Name:
        <input
          type="text"
          value={firstName}
          onChange={(event) => setFirstName(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        Last Name:
        <input
          type="text"
          value={lastName}
          onChange={(event) => setLastName(event.target.value)}
          required
        />
      </label>
      <br />
      <button type="submit">Sign Up</button>
      {error && <p>{error}</p>}
      {success && <p>{success}</p>}
    </form>
  );
}

export default Signup;
