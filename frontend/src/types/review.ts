/**
 * Review mode type definitions matching backend Pydantic schemas.
 */

import { VisionFields } from './story';

export interface ReviewNoteCreateRequest {
  reviewerName: string;
  noteText: string;
}

export interface ReviewNoteResponse {
  id: number;
  reviewerName: string;
  noteText: string;
  createdAt: string;
}

export interface ReviewStoryResponse {
  title: string;
  priority?: string | null;
  acceptanceCriteria: string[];
}

export interface ReviewReadinessSummary {
  status: string;
  gaps: Array<{
    code: string;
    message: string;
    navigateTo: string;
  }>;
}

export interface ReviewWorkspaceSnapshot {
  productName: string;
  vision: VisionFields;
  stories: ReviewStoryResponse[];
  readiness: ReviewReadinessSummary;
  reviewNotes: ReviewNoteResponse[];
}

export interface ReviewSnapshotResponse {
  workspace: ReviewWorkspaceSnapshot;
}
