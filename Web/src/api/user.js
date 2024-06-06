import { apiClient, handleResponse, handleError } from './api.js';

export const register = (data) => {
  return apiClient.post('/register/', data)
    .then(handleResponse)
    .catch(handleError);
};

export const login = (data) => {
  return apiClient.post('/api/login/', data)
    .then(handleResponse)
    .catch(handleError);
};

export const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await apiClient.post('/api/login/refresh/', {
      refresh: refreshToken
    });
    const { access } = response.data;
    localStorage.setItem('access_token', access);
    return access;
  } catch (error) {
    handleError(error);
  }
};


export const logout = (data) => {
  return apiClient.post('/api/logout/', data)
    .then(handleResponse)
    .catch(handleError);
};


export const getuser = () => {
  return apiClient.get('/api/getuser/')
    .then(handleResponse)
    .catch(handleError);
};