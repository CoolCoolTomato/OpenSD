import { apiClient, handleResponse, handleError } from './api.js';

export const get_models = () => {
  return apiClient.get('/api/get_models/')
    .then(handleResponse)
    .catch(handleError);
};

export const get_config = () => {
  return apiClient.get('/api/get_config/')
    .then(handleResponse)
    .catch(handleError);
};

export const set_config = (data) => {
  return apiClient.post('/api/set_config/', data)
    .then(handleResponse)
    .catch(handleError);
};

export const get_schedulers = () => {
  return apiClient.get('/api/get_schedulers/')
    .then(handleResponse)
    .catch(handleError);
};

export const get_samplers = () => {
  return apiClient.get('/api/get_samplers/')
    .then(handleResponse)
    .catch(handleError);
};

export const text2img = (data) => {
  return apiClient.post('/api/text2img/', data)
    .then(handleResponse)
    .catch(handleError);
};

export const images = () => {
  return apiClient.get('/api/images/')
    .then(handleResponse)
    .catch(handleError);
};

export const deleteImages = (data) => {
  return apiClient.post('/api/delete_image/', data)
    .then(handleResponse)
    .catch(handleError);
};

export const img2img = (data) => {
  return apiClient.post('/api/img2img/', data)
    .then(handleResponse)
    .catch(handleError);
};