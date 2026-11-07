export function ErrorMessage({ message }) {
  if (!message) return null;
  return <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-danger">{message}</p>;
}
