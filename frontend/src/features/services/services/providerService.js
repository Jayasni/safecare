import api from '../../../services/api';

export const providerService = {
  list: (activeOnly = true) => api.get('/providers', { params: { active_only: activeOnly } }),
  get: (id) => api.get(`/providers/${id}`),
  create: (payload) => api.post('/providers', payload),
  update: (id, payload) => api.patch(`/providers/${id}`, payload),
  updateStatus: (id, isActive) => api.patch(`/providers/${id}/status`, null, { params: { is_active: isActive } }),
};