import { Footer } from './Footer';
import { MobileNav } from './MobileNav';
import { Sidebar } from './Sidebar';

const adminLinks = [
  { to: '/admin', label: 'Admin Dashboard' },
  { to: '/admin/services', label: 'Manage Services' },
  { to: '/admin/availability', label: 'Manage Availability' },
];

export function AdminDashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen flex-col">
      <MobileNav links={adminLinks} />
      <div className="flex flex-1">
        <Sidebar variant="admin" />
        <main className="flex-1">{children}</main>
      </div>
      <Footer />
    </div>
  );
}