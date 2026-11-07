import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ErrorMessage } from '../../../components/ui/ErrorMessage';
import { Loader } from '../../../components/ui/Loader';
import api from '../../../services/api';

export default function AdminDashboardPage() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const response = await api.get('/admin/dashboard');
        setSummary(response.data);
      } catch {
        setError('Unable to load admin dashboard.');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-semibold text-heading">Admin Dashboard</h1>
      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg border border-border bg-surface p-4 shadow-sm">
          <p className="text-sm text-muted">Total bookings</p>
          <p className="mt-1 text-2xl font-semibold text-heading">{summary?.total_bookings ?? 0}</p>
        </div>
        <div className="rounded-lg border border-border bg-surface p-4 shadow-sm">
          <p className="text-sm text-muted">Pending</p>
          <p className="mt-1 text-2xl font-semibold text-heading">{summary?.status_counts?.pending ?? 0}</p>
        </div>
        <div className="rounded-lg border border-border bg-surface p-4 shadow-sm">
          <p className="text-sm text-muted">Confirmed</p>
          <p className="mt-1 text-2xl font-semibold text-heading">{summary?.status_counts?.confirmed ?? 0}</p>
        </div>
        <div className="rounded-lg border border-border bg-surface p-4 shadow-sm">
          <p className="text-sm text-muted">Cancelled</p>
          <p className="mt-1 text-2xl font-semibold text-heading">{summary?.status_counts?.cancelled ?? 0}</p>
        </div>
      </div>

      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface p-4 shadow-sm">
          <p className="text-sm text-muted">Services</p>
          <p className="mt-1 text-xl font-semibold text-heading">
            {summary?.active_services ?? 0} active / {summary?.total_services ?? 0} total
          </p>
        </div>
        <div className="rounded-lg border border-border bg-surface p-4 shadow-sm">
          <p className="text-sm text-muted">Providers</p>
          <p className="mt-1 text-xl font-semibold text-heading">
            {summary?.active_providers ?? 0} active / {summary?.total_providers ?? 0} total
          </p>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <Link to="/admin/services" className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-dark">
          Manage Services
        </Link>
        <Link to="/admin/availability" className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-dark">
          Manage Availability
        </Link>
        <Link to="/admin/bookings" className="rounded-md bg-secondary px-4 py-2 text-sm font-medium text-white hover:bg-secondary/90">
          Manage Bookings
        </Link>
      </div>
    </div>
  );
}
