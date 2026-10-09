/**
 * Centralized API client for all backend requests.
 * 
 * Features:
 * - Token management from localStorage
 * - Authorization header attachment
 * - 401 handling with token clear and redirect
 * - Base path prepending (/api/v1)
 * - Type-safe request helper
 */

const API_BASE_PATH = '/api/v1';
const AUTH_TOKEN_KEY = 'access_token';

/**
 * Type-safe HTTP request helper.
 * 
 * @param path - Request path without base (e.g., '/workspace')
 * @param options - Fetch options
 * @returns Typed response data
 * @throws Error on non-2xx responses
 */
export async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  // Read token from localStorage
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  
  // Prepare headers
  const headers = new Headers(options.headers);
  
  // Attach Authorization header if token exists
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  
  // Set Content-Type for JSON payloads
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  
  // Make request with base path prepended
  const response = await fetch(`${API_BASE_PATH}${path}`, {
    ...options,
    headers,
  });
  
  // Handle 401 Unauthorized: clear token and redirect to login
  if (response.status === 401) {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    window.location.href = '/sign-in';
    throw new Error('Unauthorized');
  }
  
  // Handle other error responses
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }
  
  // Handle 204 No Content
  if (response.status === 204) {
    return null as T;
  }
  
  // Parse and return JSON response
  return response.json() as Promise<T>;
}

/**
 * Store authentication token in localStorage.
 */
export function setAuthToken(token: string): void {
  localStorage.setItem(AUTH_TOKEN_KEY, token);
}

/**
 * Remove authentication token from localStorage.
 */
export function clearAuthToken(): void {
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

/**
 * Get current authentication token from localStorage.
 */
export function getAuthToken(): string | null {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}
