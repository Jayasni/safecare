import { useAuth } from '../../../context/AuthContext';

export default function CustomerDashboardPage() {
  const { user, logout } = useAuth();

  return (
    <main className="mx-auto max-w-4xl p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Customer Dashboard</h1>
        <button
          type="button"
          onClick={logout}
          className="rounded border border-slate-300 px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
        >
          Logout
        </button>
      </div>
      <p className="text-slate-600">Welcome, {user?.full_name}.</p>
    </main>
  );
}