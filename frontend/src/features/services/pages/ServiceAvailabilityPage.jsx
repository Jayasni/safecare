import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { EmptyState } from '../../../components/ui/EmptyState';
import { ErrorMessage } from '../../../components/ui/ErrorMessage';
import { Loader } from '../../../components/ui/Loader';
import { bookingService } from '../../appointments/services/bookingService';
import { useAuth } from '../../../context/AuthContext';
import api from '../../../services/api';

export default function ServiceAvailabilityPage() {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [service, setService] = useState(null);
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

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

  const handleBook = async () => {
    if (!selectedSlot) {
      setError('Please select an appointment slot.');
      return;
    }
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    setSubmitting(true);
    setError('');
    try {
      await bookingService.create({ slot_id: selectedSlot, reason });
      setSuccess('Appointment booked successfully.');
      setTimeout(() => navigate('/my-bookings'), 900);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.message || 'Unable to book appointment.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;
  if (error && !service) return <ErrorMessage message={error} />;

  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="mb-2 text-2xl font-semibold text-heading">{service?.name}</h1>
      <p className="mb-6 text-muted">{service?.description}</p>

      <ErrorMessage message={error} />
      {success && <p className="mb-4 rounded-md bg-green-50 px-3 py-2 text-sm text-success">{success}</p>}

      {slots.length === 0 ? (
        <EmptyState title="No available slots" description="There are no upcoming appointment slots for this service." />
      ) : (
        <div className="space-y-4">
          {slots.map((slot) => (
            <div
              key={slot.id}
              onClick={() => setSelectedSlot(slot.id)}
              className={`cursor-pointer rounded-lg border p-4 shadow-sm ${
                selectedSlot === slot.id ? 'border-primary bg-primary/5' : 'border-border bg-surface'
              }`}
            >
              <p className="font-medium text-heading">
                {new Date(slot.start_time).toLocaleString()} - {new Date(slot.end_time).toLocaleString()}
              </p>
              <p className="mt-1 text-sm text-muted">
                Capacity: {slot.capacity} | Provider ID: {slot.provider_id}
              </p>
            </div>
          ))}

          <div>
            <label className="mb-1 block text-sm font-medium text-heading" htmlFor="reason">
              Reason for visit
            </label>
            <input
              id="reason"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="w-full rounded-md border border-border px-3 py-2"
            />
          </div>

          <button
            type="button"
            onClick={handleBook}
            disabled={submitting || !selectedSlot}
            className="rounded-md bg-primary px-4 py-2 font-medium text-white hover:bg-primary-dark disabled:opacity-60"
          >
            {submitting ? 'Booking...' : 'Book Selected Slot'}
          </button>
        </div>
      )}
    </main>
  );
}

