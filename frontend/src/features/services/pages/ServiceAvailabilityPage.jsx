import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../../services/api';

export default function ServiceAvailabilityPage() {
  const { id } = useParams();
  const [service, setService] = useState(null);
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const [serviceResponse, slotResponse] = await Promise.all([
          api.get(`/services/${id}`),
          api.get(`/availability?service_id=${id}&upcoming_only=true`),
        ]);
        setService(serviceResponse.data);
        setSlots(slotResponse.data);
      } catch {
        setError('Unable to load service availability.');
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <p className="p-6 text-slate-600">Loading availability...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="mb-2 text-2xl font-semibold text-slate-900">{service?.name}</h1>
      <p className="mb-6 text-slate-600">{service?.description}</p>
      <div className="space-y-3">
        {slots.length === 0 && <p className="text-slate-600">No upcoming available slots.</p>}
        {slots.map((slot) => (
          <div key={slot.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <p className="font-medium text-slate-900">
              {new Date(slot.start_time).toLocaleString()} - {new Date(slot.end_time).toLocaleString()}
            </p>
            <p className="mt-1 text-sm text-slate-600">
              Capacity: {slot.capacity} | Provider ID: {slot.provider_id}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}