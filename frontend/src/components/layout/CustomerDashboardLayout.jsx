import { Footer } from './Footer';
import { MobileNav } from './MobileNav';
import { Sidebar } from './Sidebar';

const customerLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/services', label: 'Services' },
];

export function CustomerDashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen flex-col">
      <MobileNav links={customerLinks} />
      <div className="flex flex-1">
        <Sidebar variant="customer" />
        <main className="flex-1">{children}</main>
      </div>
      <Footer />
    </div>
  );
}