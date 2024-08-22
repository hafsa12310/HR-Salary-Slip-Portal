import React, { useState } from 'react';
import axios from 'axios';
import Notification from './Notification';
import './HomePage.css';

function HomePage() {
    const [notification, setNotification] = useState({ message: '', type: '' });

    const handleFileUpload = async (event) => {
        event.preventDefault();
        const fileInput = document.querySelector('input[type="file"]');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await axios.post('http://127.0.0.1:8000/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setNotification({ message: response.data.message, type: 'success' });
        } catch (error) {
            setNotification({ message: 'Failed to upload file', type: 'error' });
        }
    };

    const handleGeneratePDF = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/generate-pdf/');
            setNotification({ message: response.data.message, type: 'success' });
        } catch (error) {
            setNotification({ message: 'Failed to generate PDFs', type: 'error' });
        }
    };

    const handleDownloadPayslips = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/download-payslips/', {
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'payslips.zip');
            document.body.appendChild(link);
            link.click();
            setNotification({ message: 'Payslips downloaded successfully', type: 'success' });
        } catch (error) {
            setNotification({ message: 'Failed to download payslips', type: 'error' });
        }
    };

    const handleSendPayslips = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/send-payslips/');
            setNotification({ message: response.data.message, type: 'success' });
        } catch (error) {
            setNotification({ message: 'Failed to send payslips', type: 'error' });
        }
    };

    return (
        <div className="home-page">
            <Notification
                message={notification.message}
                type={notification.type}
                onClose={() => setNotification({ message: '', type: '' })}
            />
            <header className="header">
                <h1>Dashboard</h1>
            </header>
            <div className="content">
                <section className="section">
                    <h2>Upload Payroll Files</h2>
                    <form onSubmit={handleFileUpload}>
                        <input type="file" />
                        <button type="submit" className="btn btn-primary">Upload</button>
                    </form>
                </section>
                <section className="section">
                    <h2>Generate PDF Reports</h2>
                    <button onClick={handleGeneratePDF} className="btn btn-primary">Generate PDFs</button>
                </section>
                <section className="section">
                    <h2>Download Payslips</h2>
                    <button onClick={handleDownloadPayslips} className="btn btn-primary">Download</button>
                </section>
                <section className="section">
                    <h2>Send Payslips via Email</h2>
                    <button onClick={handleSendPayslips} className="btn btn-primary">Send Emails</button>
                </section>
            </div>
        </div>
    );
}

export default HomePage;
