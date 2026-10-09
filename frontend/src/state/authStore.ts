/**
 * Authentication state store.
 * 
 * Manages user authentication state using a simple reactive store pattern.
 * This can be replaced with Redux, Zustand, or other state management as needed.
 */

import { getAuthToken } from '../api/client';
import type { UserSummary } from '../types/auth';

interface AuthState {
  user: UserSummary | null;
  isAuthenticated: boolean;
}

type Listener = (state: AuthState) => void;

class AuthStore {
  private state: AuthState = {
    user: null,
    isAuthenticated: !!getAuthToken(),
  };
  
  private listeners: Set<Listener> = new Set();

  getState(): AuthState {
    return this.state;
  }

  setState(updates: Partial<AuthState>): void {
    this.state = { ...this.state, ...updates };
    this.notify();
  }

  setUser(user: UserSummary): void {
    this.setState({ user, isAuthenticated: true });
  }

  clearUser(): void {
    this.setState({ user: null, isAuthenticated: false });
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify(): void {
    this.listeners.forEach(listener => listener(this.state));
  }
}

export const authStore = new AuthStore();
