import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ element, ...rest }) => {
    const authTokens = JSON.parse(localStorage.getItem('authTokens'));

    return (
        <Route
            {...rest}
            element={authTokens ? element : <Navigate to="/login" />}
        />
    );
};

export default PrivateRoute;
