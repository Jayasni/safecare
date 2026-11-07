import { render, screen } from '@testing-library/react';
import { Badge } from '../components/ui/Badge';

describe('Badge', () => {
  it('renders status text', () => {
    render(<Badge tone="confirmed">confirmed</Badge>);
    expect(screen.getByText('confirmed')).toBeInTheDocument();
  });
});