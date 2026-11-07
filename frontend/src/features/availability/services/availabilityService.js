import api from '../../../services/api';

export const availabilityService = {
  list: (params = {}) => api.get('/availability', { params }),
  get: (id) => api.get(`/availability/${id}`),
  create: (payload) => api.post('/availability', payload),
  update: (id, payload) => api.patch(`/availability/${id}`, payload),
  updateStatus: (id, isActive) => api.patch(`/availability/${id}/status`, null, { params: { is_active: isActive } }),
};