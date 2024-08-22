import React from 'react';
import './Notification.css'; // Add styles for the notification

function Notification({ message, type, onClose }) {
    if (!message) return null;

    return (
        <div className={`notification ${type}`}>
            <span>{message}</span>
            <button onClick={onClose}>&times;</button>
        </div>
    );
}

export default Notification;
