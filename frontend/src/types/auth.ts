/**
 * Authentication type definitions matching backend Pydantic schemas.
 */

export interface LoginRequest {
  email: string;
  password: string;
}

export interface UserSummary {
  id: number;
  email: string;
  displayName: string;
}

export interface AuthTokenPayload {
  tokenType: string;
  accessToken: string;
  expiresAt: string;
}

export interface AuthResponse {
  user: UserSummary;
  auth: AuthTokenPayload;
}
