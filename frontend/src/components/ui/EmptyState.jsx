export function EmptyState({ title, description }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-surface p-8 text-center">
      <h3 className="text-base font-medium text-heading">{title}</h3>
      {description && <p className="mt-2 text-sm text-muted">{description}</p>}
    </div>
  );
}