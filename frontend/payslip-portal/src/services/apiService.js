import axios from 'axios';

const api = axios.create();

api.interceptors.request.use(config => {
    const authTokens = JSON.parse(localStorage.getItem('authTokens'));
    if (authTokens) {
        config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
}, error => Promise.reject(error));

export default api;
