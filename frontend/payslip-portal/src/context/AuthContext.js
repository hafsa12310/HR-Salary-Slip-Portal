import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [authTokens, setAuthTokens] = useState(
        JSON.parse(localStorage.getItem('authTokens')) || null
    );

    const logout = () => {
        setAuthTokens(null);
        localStorage.removeItem('authTokens');
    };

    return (
        <AuthContext.Provider value={{ authTokens, setAuthTokens, logout }}>
            {children}
        </AuthContext.Provider>
    );
}
