/**
 * Common API type definitions.
 */

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: string | null;
    requestId?: string | null;
  };
}
