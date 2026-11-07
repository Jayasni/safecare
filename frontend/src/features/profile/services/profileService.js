import api from '../../../services/api';

export const profileService = {
  get: () => api.get('/users/me'),
  update: (payload) => api.patch('/users/me', payload),
};