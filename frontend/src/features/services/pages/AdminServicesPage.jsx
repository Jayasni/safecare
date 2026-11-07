import { useEffect, useState } from 'react';
import api from '../../../services/api';

export default function AdminServicesPage() {
  const [services, setServices] = useState([]);
  const [form, setForm] = useState({ name: '', description: '', duration_minutes: 30, price: 100, is_active: true });
  const [error, setError] = useState('');

  const handleToggle = async (service) => {
    try {
      await api.patch(`/services/${service.id}/status`, null, { params: { is_active: !service.is_active } });
      await load();
    } catch {
      setError('Unable to update service status.');
    }
  };

  const load = async () => {
    try {
      const response = await api.get('/services', { params: { active_only: false } });
      setServices(response.data);
    } catch {
      setError('Unable to load services.');
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await api.post('/services', {
        ...form,
        duration_minutes: Number(form.duration_minutes),
        price: Number(form.price),
      });
      setForm({ name: '', description: '', duration_minutes: 30, price: 100, is_active: true });
      await load();
    } catch {
      setError('Unable to create service.');
    }
  };

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((current) => ({ ...current, [name]: type === 'checkbox' ? checked : value }));
  };

  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="mb-6 text-2xl font-semibold text-slate-900">Manage Services</h1>
      {error && <p className="mb-4 text-red-600">{error}</p>}
      <form onSubmit={handleSubmit} className="mb-8 grid gap-3 rounded-lg border border-slate-200 bg-white p-5 shadow-sm sm:grid-cols-2">
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name" required className="rounded border border-slate-300 px-3 py-2" />
        <input name="duration_minutes" type="number" value={form.duration_minutes} onChange={handleChange} placeholder="Duration (min)" required className="rounded border border-slate-300 px-3 py-2" />
        <input name="price" type="number" value={form.price} onChange={handleChange} placeholder="Price" required className="rounded border border-slate-300 px-3 py-2" />
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input name="is_active" type="checkbox" checked={form.is_active} onChange={handleChange} />
          Active
        </label>
        <textarea name="description" value={form.description} onChange={handleChange} placeholder="Description" className="rounded border border-slate-300 px-3 py-2 sm:col-span-2" />
        <button type="submit" className="rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 sm:col-span-2">
          Create Service
        </button>
      </form>
      <div className="space-y-3">
        {services.map((service) => (
          <div key={service.id} className="flex items-center justify-between rounded border border-slate-200 bg-white p-4 shadow-sm">
            <div>
              <p className="font-medium text-slate-900">{service.name}</p>
              <p className="text-sm text-slate-600">{service.description}</p>
              <p className="text-xs text-slate-500">Active: {String(service.is_active)}</p>
            </div>
            <button
              type="button"
              onClick={() => handleToggle(service)}
              className="rounded-md border border-border px-3 py-1 text-sm text-primary hover:bg-primary-light"
            >
              {service.is_active ? 'Deactivate' : 'Activate'}
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}

