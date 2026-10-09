/**
 * Authentication API service.
 * 
 * Handles login and logout operations.
 */

import { request, setAuthToken, clearAuthToken } from './client';
import type { LoginRequest, AuthResponse } from '../types/auth';

/**
 * Sign in with email and password.
 * 
 * @param credentials - Login credentials
 * @returns Authentication response with user info and token
 */
export async function login(credentials: LoginRequest): Promise<AuthResponse> {
  const response = await request<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
  
  // Store token in localStorage after successful login
  setAuthToken(response.auth.accessToken);
  
  return response;
}

/**
 * Sign out current user.
 * 
 * Clears local token and notifies backend for session termination.
 */
export async function logout(): Promise<void> {
  try {
    await request<void>('/auth/logout', {
      method: 'POST',
    });
  } finally {
    // Always clear token locally even if backend call fails
    clearAuthToken();
  }
}
