import { ReactNode } from 'react';

interface ProvidersProps {
  children: ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  // Auth context is managed via authStore and useAuth hook
  // No additional providers needed for this MVP
  return <>{children}</>;
}
