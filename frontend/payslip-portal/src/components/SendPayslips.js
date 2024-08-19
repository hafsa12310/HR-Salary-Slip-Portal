import React from 'react';
import axios from 'axios';

const SendPayslips = () => {
    const handleSendPayslips = async () => {
        try {
            const response = await axios.post('http://localhost:8000/send-payslips/');
            alert('Payslips sent successfully');
        } catch (error) {
            console.error('Error sending payslips:', error);
            alert('Failed to send payslips');
        }
    };

    return (
        <div>
            <h2>Send Payslips via Email</h2>
            <button onClick={handleSendPayslips}>Send Payslips</button>
        </div>
    );
};

export default SendPayslips;
