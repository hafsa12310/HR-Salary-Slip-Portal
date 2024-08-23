import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './components/landingPage';
import LoginPage from './components/loginPage';
import SignupPage from './components/signupPage';
import HomePage from './components/HomePage';
import PrivateRoute from './components/PrivateRoute';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/home" element={<PrivateRoute element={<HomePage />} />} />  {/* Protect this route */}
            <Route path="/upload" element={<PrivateRoute element={<HomePage />} />} />  {/* Upload file functionality */}
            <Route path="/generate-pdf" element={<PrivateRoute element={<HomePage />} />} />  {/* Generate PDF functionality */}
            <Route path="/download-payslips" element={<PrivateRoute element={<HomePage />} />} />  {/* Download Payslips functionality */}
            <Route path="/send-payslips" element={<PrivateRoute element={<HomePage />} />} />  {/* Send Payslips functionality */}
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
