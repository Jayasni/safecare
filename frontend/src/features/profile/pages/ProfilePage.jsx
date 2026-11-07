import { useEffect, useState } from 'react';
import { useAuth } from '../../../context/AuthContext';
import { profileService } from '../services/profileService';

export default function ProfilePage() {
  const { user } = useAuth();
  const [form, setForm] = useState({ full_name: '', phone: '' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const response = await profileService.get();
        setForm({
          full_name: response.data.full_name || '',
          phone: response.data.phone || '',
        });
      } catch {
        setError('Unable to load profile.');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    setSaving(true);
    try {
      await profileService.update({
        full_name: form.full_name,
        phone: form.phone || null,
      });
      setSuccess('Profile updated successfully.');
    } catch {
      setError('Unable to update profile.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <p className="p-6 text-muted">Loading profile...</p>;

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-semibold text-heading">Profile</h1>
      <p className="mb-4 text-sm text-muted">Email: {user?.email}</p>
      {error && <p className="mb-4 text-sm text-danger">{error}</p>}
      {success && <p className="mb-4 text-sm text-success">{success}</p>}
      <form onSubmit={handleSubmit} className="max-w-md space-y-4">
        <div>
          <label className="mb-1 block text-sm font-medium text-heading" htmlFor="full_name">
            Full Name
          </label>
          <input
            id="full_name"
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            required
            className="w-full rounded-md border border-border px-3 py-2"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-heading" htmlFor="phone">
            Phone
          </label>
          <input
            id="phone"
            name="phone"
            value={form.phone}
            onChange={handleChange}
            className="w-full rounded-md border border-border px-3 py-2"
          />
        </div>
        <button
          type="submit"
          disabled={saving}
          className="rounded-md bg-primary px-4 py-2 font-medium text-white hover:bg-primary-dark disabled:opacity-60"
        >
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </form>
    </div>
  );
}
