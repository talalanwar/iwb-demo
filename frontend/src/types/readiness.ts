/**
 * Readiness evaluation type definitions matching backend Pydantic schemas.
 */

export interface GapItem {
  code: string;
  message: string;
  navigateTo: string;
}

export interface ReadinessSummary {
  visionComplete: boolean;
  businessGoalsCount: number;
  storyCount: number;
  storiesWithAcceptanceCriteria: number;
  storiesWithPriority: number;
  reviewNotesCount: number;
}

export interface ReadinessResponse {
  workspaceId: number;
  status: string;
  summary: ReadinessSummary;
  gaps: GapItem[];
  releaseReadinessInterpretation: string;
}
