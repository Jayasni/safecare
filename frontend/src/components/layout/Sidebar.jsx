import { Link, useLocation } from 'react-router-dom';

const customerLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/services', label: 'Services' },
];

const adminLinks = [
  { to: '/admin', label: 'Admin Dashboard' },
  { to: '/admin/services', label: 'Manage Services' },
  { to: '/admin/availability', label: 'Manage Availability' },
];

export function Sidebar({ variant = 'customer' }) {
  const location = useLocation();
  const links = variant === 'admin' ? adminLinks : customerLinks;

  return (
    <aside className="hidden w-64 border-r border-border bg-surface p-4 md:block">
      <nav className="space-y-1">
        {links.map((link) => {
          const active = location.pathname === link.to;
          return (
            <Link
              key={link.to}
              to={link.to}
              className={`block rounded-md px-3 py-2 text-sm font-medium ${
                active ? 'bg-primary-light text-primary-dark' : 'text-body hover:bg-primary-light/60'
              }`}
            >
              {link.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}