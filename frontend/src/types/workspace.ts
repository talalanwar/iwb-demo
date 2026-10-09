/**
 * Workspace type definitions matching backend Pydantic schemas.
 */

import { VisionFields } from './story';

export interface WorkspaceUpdateRequest {
  productName: string;
  shortDescription?: string;
  vision: VisionFields;
}

export interface CompletenessInfo {
  visionSectionComplete: boolean;
  missingFields: string[];
}

export interface WorkspaceSaveResponse {
  workspaceId: number;
  lastSavedAt: string;
  completeness: CompletenessInfo;
}

export interface AcceptanceCriterionItem {
  id?: number | null;
  text: string;
}

export interface StoryResponse {
  id: number;
  title: string;
  actor: string;
  need: string;
  outcome: string;
  description?: string | null;
  priority?: string | null;
  backlogOrder: number;
  acceptanceCriteria: AcceptanceCriterionItem[];
}

export interface ReviewSummary {
  shareToken?: string | null;
  notes: Array<{
    id: number;
    reviewerName: string;
    noteText: string;
    createdAt: string;
  }>;
}

export interface WorkspaceAggregate {
  id: number;
  productName: string;
  shortDescription?: string | null;
  vision: VisionFields;
  stories: StoryResponse[];
  review: ReviewSummary;
  lastSavedAt: string;
}

export interface WorkspaceAggregateResponse {
  workspace: WorkspaceAggregate;
}
