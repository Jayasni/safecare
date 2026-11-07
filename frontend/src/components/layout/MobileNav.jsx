import { Link, useLocation } from 'react-router-dom';

export function MobileNav({ links }) {
  const location = useLocation();
  return (
    <nav className="flex gap-2 overflow-x-auto border-b border-border bg-surface p-3 md:hidden">
      {links.map((link) => (
        <Link
          key={link.to}
          to={link.to}
          className={`whitespace-nowrap rounded-full px-3 py-1 text-sm ${
            location.pathname === link.to ? 'bg-primary text-white' : 'bg-primary-light text-primary-dark'
          }`}
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}