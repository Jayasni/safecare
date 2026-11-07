import api from '../../../services/api';

export const bookingService = {
  create: (payload) => api.post('/bookings', payload),
  listMine: (params = {}) => api.get('/bookings/my', { params }),
  get: (id) => api.get(`/bookings/${id}`),
  reschedule: (id, newSlotId) => api.patch(`/bookings/${id}/reschedule`, { new_slot_id: newSlotId }),
  cancel: (id) => api.patch(`/bookings/${id}/cancel`),
  history: (id) => api.get(`/bookings/${id}/history`),
  adminList: (params = {}) => api.get('/admin/bookings', { params }),
  adminUpdateStatus: (id, status) => api.patch(`/admin/bookings/${id}/status`, null, { params: { new_status: status } }),
};