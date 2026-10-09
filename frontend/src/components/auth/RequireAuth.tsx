/**
 * Route guard component for protected routes.
 * 
 * Redirects to sign-in page if user is not authenticated.
 */

import { Navigate } from 'react-router-dom';
import { getAuthToken } from '../../api/client';

interface RequireAuthProps {
  children: React.ReactNode;
}

export function RequireAuth({ children }: RequireAuthProps) {
  const token = getAuthToken();

  if (!token) {
    // Redirect to sign-in page if not authenticated
    return <Navigate to="/sign-in" replace />;
  }

  return <>{children}</>;
}
