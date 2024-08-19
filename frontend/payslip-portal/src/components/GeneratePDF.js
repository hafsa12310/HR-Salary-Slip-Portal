import React from 'react';
import axios from 'axios';

const GeneratePDF = () => {
    const handleGeneratePDF = async () => {
        try {
            const response = await axios.get('http://localhost:8000/generate-pdf/');
            alert('Payslips generated successfully');
        } catch (error) {
            console.error('Error generating PDFs:', error);
            alert('Failed to generate PDFs');
        }
    };

    return (
        <div>
            <h2>Generate Payslips</h2>
            <button onClick={handleGeneratePDF}>Generate PDFs</button>
        </div>
    );
};

export default GeneratePDF;
