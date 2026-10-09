/**
 * Story and vision type definitions matching backend Pydantic schemas.
 */

export interface VisionFields {
  visionStatement?: string | null;
  targetProblem?: string | null;
  businessGoals?: string[];
  successMeasures?: string[];
}

export interface AcceptanceCriterionItem {
  id?: number | null;
  text: string;
}

export interface StoryDraft {
  id?: number | null;
  title: string;
  actor: string;
  need: string;
  outcome: string;
  description?: string | null;
  priority?: string | null;
  backlogOrder: number;
  acceptanceCriteria: AcceptanceCriterionItem[];
}

export interface StorySetUpdateRequest {
  stories: StoryDraft[];
}

export interface ValidationSummary {
  storiesMissingPriority: number;
  storiesMissingAcceptanceCriteria: number;
}

export interface StorySaveResponse {
  workspaceId: number;
  storiesSaved: number;
  lastSavedAt: string;
  validationSummary: ValidationSummary;
}
