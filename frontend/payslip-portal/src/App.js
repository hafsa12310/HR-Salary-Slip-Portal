  import React from 'react';
  import { useState } from 'react';
  import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
  import LandingPage from './components/landingPage';
  import LoginPage from './components/loginPage';
  import SignupPage from './components/signupPage';
  import HomePage from './components/HomePage';
  import PrivateRoute from './components/PrivateRoute';
  import { AuthProvider } from './context/AuthContext';
  import { Navigate } from 'react-router-dom';
  

  function App() {

    const [authTokens, setAuthTokens] = useState(null);
    return (
      <AuthProvider>
        <Router>
          <div>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage setAuthTokens={setAuthTokens} />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/home" element={authTokens ? <HomePage /> : <Navigate to="/login" />} />              
              <Route path="/upload" />  
              <Route path="/generate-pdf" element={<HomePage />} />
              <Route path="/download-payslips" element={<HomePage />} /> 
              <Route path="/send-payslips"  element={<HomePage />} />  
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    );
  }

  export default App;
