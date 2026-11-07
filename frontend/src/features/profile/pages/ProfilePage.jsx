import { useAuth } from '../../../context/AuthContext';

export default function ProfilePage() {
  const { user } = useAuth();
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold text-heading">Profile</h1>
      <p className="mt-2 text-muted">{user?.email}</p>
    </div>
  );
}