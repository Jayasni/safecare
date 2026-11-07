import api from '../../../services/api';

export const serviceService = {
  list: (activeOnly = true) => api.get('/services', { params: { active_only: activeOnly } }),
  get: (id) => api.get(`/services/${id}`),
  create: (payload) => api.post('/services', payload),
  update: (id, payload) => api.patch(`/services/${id}`, payload),
  updateStatus: (id, isActive) => api.patch(`/services/${id}/status`, null, { params: { is_active: isActive } }),
};