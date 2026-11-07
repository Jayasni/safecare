import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Badge } from '../../../components/ui/Badge';
import { EmptyState } from '../../../components/ui/EmptyState';
import { Loader } from '../../../components/ui/Loader';
import { bookingService } from '../../appointments/services/bookingService';

export default function CustomerDashboardPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const response = await bookingService.listMine({ limit: 100 });
        setBookings(response.data);
      } catch {
        setError('Unable to load dashboard data.');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <Loader />;
  if (error) return <p className="p-6 text-danger">{error}</p>;

  const upcoming = bookings.filter((booking) =>
    ['pending', 'confirmed'].includes(booking.status) &&
    new Date(booking.slot.start_time) >= new Date(),
  );
  const counts = {
    total: bookings.length,
    pending: bookings.filter((booking) => booking.status === 'pending').length,
    confirmed: bookings.filter((booking) => booking.status === 'confirmed').length,
    completed: bookings.filter((booking) => booking.status === 'completed').length,
    cancelled: bookings.filter((booking) => booking.status === 'cancelled').length,
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-heading">Customer Dashboard</h1>
        <Link to="/services" className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-dark">
          Book Appointment
        </Link>
      </div>

      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {Object.entries(counts).map(([label, value]) => (
          <div key={label} className="rounded-lg border border-border bg-surface p-4 shadow-sm">
            <p className="text-sm capitalize text-muted">{label}</p>
            <p className="mt-1 text-2xl font-semibold text-heading">{value}</p>
          </div>
        ))}
      </div>

      <h2 className="mb-3 text-lg font-semibold text-heading">Upcoming appointments</h2>
      {upcoming.length === 0 ? (
        <EmptyState title="No upcoming appointments" description="Book your first appointment to get started." />
      ) : (
        <div className="space-y-3">
          {upcoming.slice(0, 5).map((booking) => (
            <div key={booking.id} className="flex flex-col justify-between rounded-lg border border-border bg-surface p-4 shadow-sm sm:flex-row sm:items-center">
              <div>
                <p className="font-medium text-heading">Booking #{booking.booking_reference}</p>
                <p className="text-sm text-muted">
                  {new Date(booking.slot.start_time).toLocaleString()} - {new Date(booking.slot.end_time).toLocaleString()}
                </p>
              </div>
              <Badge tone={booking.status}>{booking.status}</Badge>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
