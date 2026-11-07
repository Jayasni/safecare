import { useAuth } from '../../../context/AuthContext';

export default function MyBookingsPage() {
  const { user } = useAuth();
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold text-heading">My Bookings</h1>
      <p className="mt-2 text-muted">Booking list for {user?.full_name} will be implemented in Phase 07.</p>
    </div>
  );
}