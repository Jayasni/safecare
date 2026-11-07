import { useState } from 'react';
import api from '../../../services/api';

export default function AdminAvailabilityPage() {
  const [form, setForm] = useState({
    service_id: '',
    provider_id: '',
    start_time: '',
    end_time: '',
    capacity: 1,
    is_active: true,
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((current) => ({ ...current, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    try {
      await api.post('/availability', {
        service_id: Number(form.service_id),
        provider_id: form.provider_id ? Number(form.provider_id) : null,
        start_time: new Date(form.start_time).toISOString(),
        end_time: new Date(form.end_time).toISOString(),
        capacity: Number(form.capacity),
        is_active: form.is_active,
      });
      setSuccess('Availability slot created.');
    } catch {
      setError('Unable to create availability slot.');
    }
  };

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-6 text-2xl font-semibold text-slate-900">Manage Availability</h1>
      {error && <p className="mb-4 text-red-600">{error}</p>}
      {success && <p className="mb-4 text-green-600">{success}</p>}
      <form onSubmit={handleSubmit} className="grid gap-3">
        <input name="service_id" value={form.service_id} onChange={handleChange} placeholder="Service ID" required className="rounded border border-slate-300 px-3 py-2" />
        <input name="provider_id" value={form.provider_id} onChange={handleChange} placeholder="Provider ID (optional)" className="rounded border border-slate-300 px-3 py-2" />
        <input name="start_time" type="datetime-local" value={form.start_time} onChange={handleChange} required className="rounded border border-slate-300 px-3 py-2" />
        <input name="end_time" type="datetime-local" value={form.end_time} onChange={handleChange} required className="rounded border border-slate-300 px-3 py-2" />
        <input name="capacity" type="number" min="1" value={form.capacity} onChange={handleChange} required className="rounded border border-slate-300 px-3 py-2" />
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input name="is_active" type="checkbox" checked={form.is_active} onChange={handleChange} />
          Active
        </label>
        <button type="submit" className="rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700">
          Create Slot
        </button>
      </form>
    </main>
  );
}

