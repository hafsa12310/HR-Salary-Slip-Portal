import React from 'react';
import { Navigate } from 'react-router-dom';

function PrivateRoute({ element }) {
    const isAuthenticated = !!localStorage.getItem('user_id');  // Check if the user_id is stored in local storage

    return isAuthenticated ? element : <Navigate to="/login" />;
}

export default PrivateRoute;
