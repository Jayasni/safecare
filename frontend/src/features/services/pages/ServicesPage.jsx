import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../../services/api';

export default function ServicesPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const response = await api.get('/services');
        setServices(response.data);
      } catch {
        setError('Unable to load services.');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <p className="p-6 text-slate-600">Loading services...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="mb-6 text-2xl font-semibold text-slate-900">Services</h1>
      <div className="grid gap-4 sm:grid-cols-2">
        {services.map((service) => (
          <article key={service.id} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-medium text-slate-900">{service.name}</h2>
            <p className="mt-2 text-sm text-slate-600">{service.description || 'No description'}</p>
            <p className="mt-3 text-sm text-slate-700">
              Duration: {service.duration_minutes} min | Price: {service.price}
            </p>
            <Link
              to={`/services/${service.id}`}
              className="mt-4 inline-block text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              View availability
            </Link>
          </article>
        ))}
      </div>
    </main>
  );
}