import React from 'react';
import axios from 'axios';

const DownloadPayslips = () => {
    const handleDownloadPayslips = async () => {
        try {
            const response = await axios.get('http://localhost:8000/download-payslips/', {
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'payslips.zip');
            document.body.appendChild(link);
            link.click();
        } catch (error) {
            console.error('Error downloading payslips:', error);
            alert('Failed to download payslips');
        }
    };

    return (
        <div>
            <h2>Download Payslips</h2>
            <button onClick={handleDownloadPayslips}>Download Payslips</button>
        </div>
    );
};

export default DownloadPayslips;
