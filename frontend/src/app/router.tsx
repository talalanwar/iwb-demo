import { createBrowserRouter, Navigate } from 'react-router-dom';
import { RequireAuth } from '../components/auth/RequireAuth';
import SignInPage from '../pages/SignInPage';
import OnboardingPage from '../pages/OnboardingPage';
import SavedWorkspacesPage from '../pages/SavedWorkspacesPage';
import SettingsPage from '../pages/SettingsPage';
import WorkspacePage from '../pages/WorkspacePage';
import BacklogPage from '../pages/BacklogPage';
import ReadinessPage from '../pages/ReadinessPage';
import ReviewPage from '../pages/ReviewPage';

export const router = createBrowserRouter([
  {
    path: '/sign-in',
    element: <SignInPage />
  },
  {
    path: '/onboarding',
    element: (
      <RequireAuth>
        <OnboardingPage />
      </RequireAuth>
    )
  },
  {
    path: '/workspaces',
    element: (
      <RequireAuth>
        <SavedWorkspacesPage />
      </RequireAuth>
    )
  },
  {
    path: '/settings',
    element: (
      <RequireAuth>
        <SettingsPage />
      </RequireAuth>
    )
  },
  {
    path: '/',
    element: (
      <RequireAuth>
        <Navigate to="/workspace" replace />
      </RequireAuth>
    )
  },
  {
    path: '/workspace',
    element: (
      <RequireAuth>
        <WorkspacePage />
      </RequireAuth>
    )
  },
  {
    path: '/backlog',
    element: (
      <RequireAuth>
        <BacklogPage />
      </RequireAuth>
    )
  },
  {
    path: '/readiness',
    element: (
      <RequireAuth>
        <ReadinessPage />
      </RequireAuth>
    )
  },
  {
    path: '/review/:shareToken',
    element: (
      <RequireAuth>
        <ReviewPage />
      </RequireAuth>
    )
  }
]);
