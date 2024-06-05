import axios from 'axios';
import Config from '@/config/config.js';
import { refreshAccessToken } from '@/api/user.js';

export const apiClient = axios.create({
  baseURL: Config.baseURL,
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newAccessToken = await refreshAccessToken();
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return Promise.reject(err);
      }
    }

    if (error.response.status === 403) {
      console.error('Access denied');
    } else if (error.response.status === 500) {
      console.error('Server error');
    }

    return Promise.reject(error);
  }
);

export const handleResponse = (response) => {
  return response.data;
};

export const handleError = (error) => {
  console.error('API call error:', error);
  throw error;
};
