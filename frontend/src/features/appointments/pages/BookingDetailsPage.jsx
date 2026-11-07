import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Badge } from '../../../components/ui/Badge';
import { ErrorMessage } from '../../../components/ui/ErrorMessage';
import { Loader } from '../../../components/ui/Loader';
import { bookingService } from '../services/bookingService';

export default function BookingDetailsPage() {
  const { id } = useParams();
  const [booking, setBooking] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const [bookingResponse, historyResponse] = await Promise.all([
          bookingService.get(id),
          bookingService.history(id),
        ]);
        setBooking(bookingResponse.data);
        setHistory(historyResponse.data);
      } catch {
        setError('Unable to load booking details.');
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;
  if (!booking) return <ErrorMessage message="Booking not found." />;

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-heading">Booking Details</h1>
        <Badge tone={booking.status}>{booking.status}</Badge>
      </div>

      <div className="mb-6 rounded-lg border border-border bg-surface p-5 shadow-sm">
        <p><span className="font-medium">Reference:</span> {booking.booking_reference}</p>
        <p><span className="font-medium">Slot:</span> {new Date(booking.slot.start_time).toLocaleString()} - {new Date(booking.slot.end_time).toLocaleString()}</p>
        <p><span className="font-medium">Service ID:</span> {booking.slot.service_id}</p>
        <p><span className="font-medium">Provider ID:</span> {booking.slot.provider_id || 'N/A'}</p>
        {booking.reason && <p><span className="font-medium">Reason:</span> {booking.reason}</p>}
      </div>

      <h2 className="mb-3 text-lg font-semibold text-heading">Booking history</h2>
      <div className="space-y-3">
        {history.length === 0 && <p className="text-muted">No history available.</p>}
        {history.map((item) => (
          <div key={item.id} className="rounded-lg border border-border bg-surface p-4 shadow-sm">
            <p className="font-medium text-heading">{item.event_type}</p>
            <p className="text-sm text-muted">
              {item.old_status || 'none'} → {item.new_status || 'none'} at {new Date(item.changed_at).toLocaleString()}
            </p>
            {item.change_reason && <p className="mt-1 text-sm text-body">{item.change_reason}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}

