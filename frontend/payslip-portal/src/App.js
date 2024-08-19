import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import UploadFile from './components/UploadFile';
import GeneratePDF from './components/GeneratePDF';
import DownloadPayslips from './components/DownloadPayslips';
import SendPayslips from './components/SendPayslips';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/upload">Upload File</Link></li>
            <li><Link to="/generate-pdf">Generate PDFs</Link></li>
            <li><Link to="/download-payslips">Download Payslips</Link></li>
            <li><Link to="/send-payslips">Send Payslips</Link></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/upload" element={<UploadFile />} />
          <Route path="/generate-pdf" element={<GeneratePDF />} />
          <Route path="/download-payslips" element={<DownloadPayslips />} />
          <Route path="/send-payslips" element={<SendPayslips />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
