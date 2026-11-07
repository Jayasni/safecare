import { useEffect, useState } from 'react';
import { Badge } from '../../../components/ui/Badge';
import { EmptyState } from '../../../components/ui/EmptyState';
import { ErrorMessage } from '../../../components/ui/ErrorMessage';
import { Loader } from '../../../components/ui/Loader';
import { bookingService } from '../../appointments/services/bookingService';

const STATUSES = ['pending', 'confirmed', 'cancelled', 'completed'];

export default function AdminBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [statusFilter, setStatusFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await bookingService.adminList(statusFilter ? { status: statusFilter } : {});
      setBookings(response.data);
    } catch {
      setError('Unable to load bookings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [statusFilter]);

  const handleStatusUpdate = async (bookingId, newStatus) => {
    try {
      await bookingService.adminUpdateStatus(bookingId, newStatus);
      await load();
    } catch {
      setError('Unable to update booking status.');
    }
  };

  if (loading) return <Loader />;
  if (error && bookings.length === 0) return <ErrorMessage message={error} />;

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-semibold text-heading">Manage Bookings</h1>
      <ErrorMessage message={error} />

      <div className="mb-4">
        <label className="mr-2 text-sm font-medium text-heading" htmlFor="status-filter">
          Status:
        </label>
        <select
          id="status-filter"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="rounded-md border border-border px-3 py-2"
        >
          <option value="">All</option>
          {STATUSES.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>

      {bookings.length === 0 ? (
        <EmptyState title="No bookings found" description="There are no bookings matching the selected filter." />
      ) : (
        <div className="space-y-3">
          {bookings.map((booking) => (
            <div key={booking.id} className="rounded-lg border border-border bg-surface p-4 shadow-sm">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <p className="font-semibold text-heading">#{booking.booking_reference}</p>
                  <p className="text-sm text-muted">
                    User {booking.user_id} | Slot {booking.slot_id} | {new Date(booking.slot.start_time).toLocaleString()}
                  </p>
                </div>
                <Badge tone={booking.status}>{booking.status}</Badge>
              </div>

              <div className="mt-3 flex items-center gap-2">
                <select
                  defaultValue={booking.status}
                  onChange={(e) => handleStatusUpdate(booking.id, e.target.value)}
                  className="rounded-md border border-border px-2 py-1 text-sm"
                >
                  {STATUSES.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
