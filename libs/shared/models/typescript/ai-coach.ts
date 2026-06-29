/**
 * Shared TypeScript interfaces for AI coach suggestions.
 */

export interface AISuggestionBase {
  exercise_id: number;
  exercise_name: string;
  current_weight: number;
  suggested_weight: number;
  reason: string;
  confidence: number;
}

export interface AISuggestionResponse extends AISuggestionBase {}
