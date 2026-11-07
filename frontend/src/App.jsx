import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { AdminRoute, ProtectedRoute } from './components/common/ProtectedRoute';
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';
import CustomerDashboardPage from './features/dashboard/pages/CustomerDashboardPage';
import AdminDashboardPage from './features/dashboard/pages/AdminDashboardPage';
import ServicesPage from './features/services/pages/ServicesPage';
import ServiceAvailabilityPage from './features/services/pages/ServiceAvailabilityPage';
import AdminServicesPage from './features/services/pages/AdminServicesPage';
import AdminAvailabilityPage from './features/availability/pages/AdminAvailabilityPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<p className="p-6 text-slate-700">SageCare Booking</p>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <CustomerDashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <AdminRoute>
                <AdminDashboardPage />
              </AdminRoute>
            }
          />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/services/:id" element={<ServiceAvailabilityPage />} />
          <Route
            path="/admin/services"
            element={
              <AdminRoute>
                <AdminServicesPage />
              </AdminRoute>
            }
          />
          <Route
            path="/admin/availability"
            element={
              <AdminRoute>
                <AdminAvailabilityPage />
              </AdminRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}