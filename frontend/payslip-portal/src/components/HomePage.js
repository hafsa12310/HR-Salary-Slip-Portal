import React, { useState } from 'react';
import api from '../services/apiService'; // Import the configured Axios instance
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
            const response = await api.post('http://127.0.0.1:8000/upload/', formData, {
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
            const response = await api.get('http://127.0.0.1:8000/generate-pdf/');
            setNotification({ message: response.data.message, type: 'success' });
        } catch (error) {
            setNotification({ message: 'Failed to generate PDFs', type: 'error' });
        }
    };

    const handleDownloadPayslips = async () => {
        try {
            const response = await api.get('http://127.0.0.1:8000/download-payslips/', {
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
            const response = await api.post('http://127.0.0.1:8000/send-payslips/');
            setNotification({ message: response.data.message, type: 'success' });
        } catch (error) {
            setNotification({ message: 'Failed to send payslips', type: 'error' });
        }
    };

    return (
        <div className="home-page">
            <div className="home-container">
                <h2>Home Page</h2>
                <form onSubmit={handleFileUpload}>
                    <input type="file" />
                    <button type="submit">Upload File</button>
                </form>
                <div className="action-buttons">
                    <button type="button" onClick={handleGeneratePDF}>Generate PDF</button>
                    <button type="button" onClick={handleDownloadPayslips}>Download Payslips</button>
                    <button type="button" onClick={handleSendPayslips}>Send Payslips</button>
                </div>
                {notification.message && (
                    <Notification message={notification.message} type={notification.type} />
                )}
            </div>
        </div>
    );
}

export default HomePage;
