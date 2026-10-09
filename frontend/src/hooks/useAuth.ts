/**
 * Authentication hook.
 * 
 * Provides access to auth state and operations.
 */

import { useState, useEffect } from 'react';
import { authStore } from '../state/authStore';
import { login as apiLogin, logout as apiLogout } from '../api/authApi';
import type { LoginRequest } from '../types/auth';

export function useAuth() {
  const [state, setState] = useState(authStore.getState());

  useEffect(() => {
    const unsubscribe = authStore.subscribe(setState);
    return unsubscribe;
  }, []);

  const login = async (credentials: LoginRequest) => {
    const response = await apiLogin(credentials);
    authStore.setUser(response.user);
    return response;
  };

  const logout = async () => {
    await apiLogout();
    authStore.clearUser();
  };

  return {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    login,
    logout,
  };
}
