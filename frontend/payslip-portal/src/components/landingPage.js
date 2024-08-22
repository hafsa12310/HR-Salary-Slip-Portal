import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';  // Import the CSS file

function LandingPage() {
    return (
        <div className="landing-page">
            <h1>Welcome to Your Payslip Generation Portal</h1>
            <p>Manage and automate your payroll processes effortlessly with our secure platform.</p>
            <div className="buttons">
                <Link to="/login" className="btn">Login</Link>
                <Link to="/signup" className="btn btn-secondary">Sign Up</Link>
            </div>
        </div>
    );
}

export default LandingPage;
