import React, { useState } from 'react';

function Signup() {
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (password1 !== password2) {
      console.error('Passwords do not match');
      return;
    }
    const response = await fetch('/api/signup/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password: password1, first_name: firstName, last_name: lastName })
    });
    if (response.ok) {
      const data = await response.json();
      console.log(data);
    } else {
      const error = await response.json();
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email:
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
      </label>
      <br />
      <label>
        Password:
        <input type="password" value={password1} onChange={(event) => setPassword1(event.target.value)} required />
      </label>
      <br />
      <label>
        Confirm Password:
        <input type="password" value={password2} onChange={(event) => setPassword2(event.target.value)} required />
      </label>
      <br />
      <label>
        First Name:
        <input type="text" value={firstName} onChange={(event) => setFirstName(event.target.value)} required />
      </label>
      <br />
      <label>
        Last Name:
        <input type="text" value={lastName} onChange={(event) => setLastName(event.target.value)} required />
      </label>
      <br />
      <button type="submit">Sign Up</button>
    </form>
  );
}

export default Signup;