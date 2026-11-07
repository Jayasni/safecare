import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { AdminRoute, ProtectedRoute } from './components/common/ProtectedRoute';
import { AdminDashboardLayout } from './components/layout/AdminDashboardLayout';
import { CustomerDashboardLayout } from './components/layout/CustomerDashboardLayout';
import { PublicLayout } from './components/layout/PublicLayout';
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';
import CustomerDashboardPage from './features/dashboard/pages/CustomerDashboardPage';
import AdminDashboardPage from './features/dashboard/pages/AdminDashboardPage';
import AdminBookingsPage from './features/dashboard/pages/AdminBookingsPage';
import ServicesPage from './features/services/pages/ServicesPage';
import ServiceAvailabilityPage from './features/services/pages/ServiceAvailabilityPage';
import AdminServicesPage from './features/services/pages/AdminServicesPage';
import AdminAvailabilityPage from './features/availability/pages/AdminAvailabilityPage';
import MyBookingsPage from './features/appointments/pages/MyBookingsPage';
import BookingDetailsPage from './features/appointments/pages/BookingDetailsPage';
import ProfilePage from './features/profile/pages/ProfilePage';

function HomePage() {
  return (
    <div className="mx-auto max-w-5xl p-6">
      <h1 className="text-3xl font-semibold text-heading">Welcome to SageCare Booking</h1>
      <p className="mt-3 text-muted">Find and manage your appointments online.</p>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<PublicLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/services" element={<ServicesPage />} />
            <Route path="/services/:id" element={<ServiceAvailabilityPage />} />
          </Route>

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <CustomerDashboardLayout>
                  <CustomerDashboardPage />
                </CustomerDashboardLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/my-bookings"
            element={
              <ProtectedRoute>
                <CustomerDashboardLayout>
                  <MyBookingsPage />
                </CustomerDashboardLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/bookings/:id"
            element={
              <ProtectedRoute>
                <CustomerDashboardLayout>
                  <BookingDetailsPage />
                </CustomerDashboardLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <CustomerDashboardLayout>
                  <ProfilePage />
                </CustomerDashboardLayout>
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin"
            element={
              <AdminRoute>
                <AdminDashboardLayout>
                  <AdminDashboardPage />
                </AdminDashboardLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/services"
            element={
              <AdminRoute>
                <AdminDashboardLayout>
                  <AdminServicesPage />
                </AdminDashboardLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/availability"
            element={
              <AdminRoute>
                <AdminDashboardLayout>
                  <AdminAvailabilityPage />
                </AdminDashboardLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/bookings"
            element={
              <AdminRoute>
                <AdminDashboardLayout>
                  <AdminBookingsPage />
                </AdminDashboardLayout>
              </AdminRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}