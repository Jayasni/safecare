import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Badge } from '../../../components/ui/Badge';
import { ConfirmDialog } from '../../../components/ui/ConfirmDialog';
import { EmptyState } from '../../../components/ui/EmptyState';
import { ErrorMessage } from '../../../components/ui/ErrorMessage';
import { Loader } from '../../../components/ui/Loader';
import { Modal } from '../../../components/ui/Modal';
import { bookingService } from '../services/bookingService';
import { availabilityService } from '../../availability/services/availabilityService';

export default function MyBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [bookingToCancel, setBookingToCancel] = useState(null);
  const [rescheduleBooking, setRescheduleBooking] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [selectedNewSlot, setSelectedNewSlot] = useState(null);
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const loadBookings = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await bookingService.listMine({ limit: 100 });
      setBookings(response.data);
    } catch {
      setError('Unable to load bookings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBookings();
  }, []);

  const openReschedule = async (booking) => {
    setRescheduleBooking(booking);
    setSelectedNewSlot(null);
    setLoadingSlots(true);
    try {
      const response = await availabilityService.list({
        service_id: booking.slot.service_id,
        upcoming_only: true,
      });
      setAvailableSlots(response.data.filter((slot) => slot.id !== booking.slot_id));
    } catch {
      setAvailableSlots([]);
    } finally {
      setLoadingSlots(false);
    }
  };

  const handleCancel = async () => {
    if (!bookingToCancel) return;
    setSubmitting(true);
    try {
      await bookingService.cancel(bookingToCancel.id);
      setBookingToCancel(null);
      await loadBookings();
    } catch {
      setError('Unable to cancel booking.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleReschedule = async () => {
    if (!rescheduleBooking || !selectedNewSlot) return;
    setSubmitting(true);
    try {
      await bookingService.reschedule(rescheduleBooking.id, selectedNewSlot);
      setRescheduleBooking(null);
      await loadBookings();
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to reschedule booking.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;
  if (error && bookings.length === 0) return <ErrorMessage message={error} />;

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-semibold text-heading">My Bookings</h1>
      <ErrorMessage message={error} />

      {bookings.length === 0 ? (
        <EmptyState title="No bookings yet" description="Find a service and book an appointment to get started." />
      ) : (
        <div className="space-y-4">
          {bookings.map((booking) => (
            <div key={booking.id} className="rounded-lg border border-border bg-surface p-5 shadow-sm">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <p className="font-semibold text-heading">Booking #{booking.booking_reference}</p>
                  <p className="text-sm text-muted">
                    {new Date(booking.slot.start_time).toLocaleString()} - {new Date(booking.slot.end_time).toLocaleString()}
                  </p>
                  {booking.reason && <p className="mt-2 text-sm text-body">Reason: {booking.reason}</p>}
                </div>
                <Badge tone={booking.status}>{booking.status}</Badge>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                <Link to={`/bookings/${booking.id}`} className="text-sm font-medium text-primary hover:text-primary-dark">
                  View details
                </Link>
                {['pending', 'confirmed'].includes(booking.status) && (
                  <>
                    <button
                      type="button"
                      onClick={() => openReschedule(booking)}
                      className="text-sm font-medium text-primary hover:text-primary-dark"
                    >
                      Reschedule
                    </button>
                    <button
                      type="button"
                      onClick={() => setBookingToCancel(booking)}
                      className="text-sm font-medium text-danger hover:text-red-700"
                    >
                      Cancel
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <ConfirmDialog
        isOpen={Boolean(bookingToCancel)}
        title="Cancel booking"
        message="Are you sure you want to cancel this appointment?"
        confirmLabel="Cancel appointment"
        isDanger
        onConfirm={handleCancel}
        onCancel={() => setBookingToCancel(null)}
      />

      <Modal isOpen={Boolean(rescheduleBooking)} title="Reschedule appointment" onClose={() => setRescheduleBooking(null)}>
        {loadingSlots ? (
          <Loader label="Loading available slots..." />
        ) : availableSlots.length === 0 ? (
          <EmptyState title="No available slots" description="There are no other upcoming slots for this service." />
        ) : (
          <div className="space-y-3">
            {availableSlots.map((slot) => (
              <button
                key={slot.id}
                type="button"
                onClick={() => setSelectedNewSlot(slot.id)}
                className={`w-full rounded-lg border p-4 text-left ${
                  selectedNewSlot === slot.id ? 'border-primary bg-primary/5' : 'border-border bg-surface'
                }`}
              >
                <p className="font-medium text-heading">
                  {new Date(slot.start_time).toLocaleString()} - {new Date(slot.end_time).toLocaleString()}
                </p>
                <p className="text-sm text-muted">Capacity: {slot.capacity}</p>
              </button>
            ))}
            <button
              type="button"
              onClick={handleReschedule}
              disabled={!selectedNewSlot || submitting}
              className="w-full rounded-md bg-primary px-4 py-2 font-medium text-white hover:bg-primary-dark disabled:opacity-60"
            >
              {submitting ? 'Rescheduling...' : 'Confirm new slot'}
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
}
