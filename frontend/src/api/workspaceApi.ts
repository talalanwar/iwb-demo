/**
 * Workspace API service.
 * 
 * Handles workspace CRUD operations, vision updates, and story management.
 */

import { request } from './client';
import type {
  WorkspaceAggregateResponse,
  WorkspaceUpdateRequest,
  WorkspaceSaveResponse,
} from '../types/workspace';
import type { StorySetUpdateRequest, StorySaveResponse } from '../types/story';
import type { ReadinessResponse } from '../types/readiness';

/**
 * Get or create the single workspace for the authenticated user.
 * 
 * @returns Workspace aggregate with vision, stories, and review data
 */
export async function getWorkspace(): Promise<WorkspaceAggregateResponse> {
  return request<WorkspaceAggregateResponse>('/workspace', {
    method: 'GET',
  });
}

/**
 * Update workspace metadata and vision.
 * 
 * @param data - Workspace metadata and vision fields
 * @returns Save confirmation with completeness status
 */
export async function updateWorkspace(
  data: WorkspaceUpdateRequest
): Promise<WorkspaceSaveResponse> {
  return request<WorkspaceSaveResponse>('/workspace', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Update the full story set with criteria and priorities.
 * 
 * @param data - Complete story set update
 * @returns Save confirmation with validation summary
 */
export async function updateStories(
  data: StorySetUpdateRequest
): Promise<StorySaveResponse> {
  return request<StorySaveResponse>('/workspace/stories', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Get workspace readiness evaluation.
 * 
 * @returns Readiness status with gaps and summary
 */
export async function getReadiness(): Promise<ReadinessResponse> {
  return request<ReadinessResponse>('/workspace/readiness', {
    method: 'GET',
  });
}
