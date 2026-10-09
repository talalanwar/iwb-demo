/**
 * Review mode API service.
 * 
 * Handles review snapshot and review note operations.
 */

import { request } from './client';
import type {
  ReviewSnapshotResponse,
  ReviewNoteCreateRequest,
  ReviewNoteResponse,
} from '../types/review';

/**
 * Get review mode workspace snapshot via share token.
 * 
 * @param shareToken - Protected review share token
 * @returns Read-only workspace snapshot with review context
 */
export async function getReviewSnapshot(
  shareToken: string
): Promise<ReviewSnapshotResponse> {
  return request<ReviewSnapshotResponse>(`/review/${shareToken}`, {
    method: 'GET',
  });
}

/**
 * Create a new review note.
 * 
 * @param shareToken - Protected review share token
 * @param note - Review note content
 * @returns Created review note with ID
 */
export async function createReviewNote(
  shareToken: string,
  note: ReviewNoteCreateRequest
): Promise<ReviewNoteResponse> {
  return request<ReviewNoteResponse>(`/review/${shareToken}/notes`, {
    method: 'POST',
    body: JSON.stringify(note),
  });
}
