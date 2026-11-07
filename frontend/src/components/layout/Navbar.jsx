import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="border-b border-border bg-surface">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link to="/" className="text-lg font-semibold text-primary-dark">SageCare Booking</Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link to="/services" className="text-body hover:text-primary-dark">Services</Link>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="text-body hover:text-primary-dark">Dashboard</Link>
              {user?.role === 'admin' && <Link to="/admin" className="text-body hover:text-primary-dark">Admin</Link>}
              <button type="button" onClick={() => { logout(); navigate('/'); }} className="text-body hover:text-primary-dark">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-body hover:text-primary-dark">Login</Link>
              <Link to="/register" className="rounded-md bg-primary px-3 py-1.5 text-white hover:bg-primary-dark">
                Register
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}