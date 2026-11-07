export function Select({ label, error, options = [], className = '', ...props }) {
  return (
    <label className="block">
      {label && <span className="mb-1 block text-sm font-medium text-heading">{label}</span>}
      <select
        className={`w-full rounded-md border border-border px-3 py-2 text-sm text-body outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 ${className}`}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <span className="mt-1 block text-xs text-danger">{error}</span>}
    </label>
  );
}