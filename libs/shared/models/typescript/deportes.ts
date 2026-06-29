/**
 * Shared TypeScript interfaces for the Deportes (Sports) module.
 * Mirrors backend Pydantic schemas in apps/backend/src/models/schemas.py.
 */

// ---------------------------------------------------------------------------
// Sport
// ---------------------------------------------------------------------------

export interface SportBase {
  name: string;
  icon?: string;
}

export interface SportCreate extends SportBase {}

export interface SportResponse extends SportBase {
  id: number;
  is_custom: boolean;
  created_at: string;
}

// ---------------------------------------------------------------------------
// Sport Activity
// ---------------------------------------------------------------------------

export interface SportActivityBase {
  sport_id: number;
  date: string;
  duration_seconds: number;
  distance_km?: number;
  calories?: number;
  heart_rate_avg?: number;
  extra_data?: Record<string, unknown>;
  notes?: string;
}

export interface SportActivityCreate extends SportActivityBase {}

export interface SportActivityUpdate {
  date?: string;
  duration_seconds?: number;
  distance_km?: number;
  calories?: number;
  heart_rate_avg?: number;
  extra_data?: Record<string, unknown>;
  notes?: string;
}

export interface SportActivityResponse extends SportActivityBase {
  id: number;
  user_id: number;
  created_at: string;
}

// ---------------------------------------------------------------------------
// Sport Stats & Personal Records
// ---------------------------------------------------------------------------

export interface SportStatsResponse {
  sport_id: number;
  sport_name: string;
  total_activities: number;
  total_time_seconds: number;
  total_distance_km?: number;
  average_duration_seconds?: number;
}

export interface PersonalRecordResponse {
  sport_id: number;
  best_time_seconds?: number;
  best_distance_km?: number;
  best_pace_seconds_per_km?: number;
  best_time_date?: string;
  best_distance_date?: string;
}

// ---------------------------------------------------------------------------
// Training Plan
// ---------------------------------------------------------------------------

export interface TrainingPlanWeekUpdate {
  week_number: number;
  target_sessions: number;
  completed_sessions?: number;
  notes?: string;
}

export interface TrainingPlanBase {
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
}

export interface TrainingPlanCreate extends TrainingPlanBase {
  weeks?: TrainingPlanWeekUpdate[];
}

export interface TrainingPlanUpdate {
  name?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  weeks?: TrainingPlanWeekUpdate[];
}

export interface TrainingPlanWeekResponse {
  id: number;
  week_number: number;
  target_sessions: number;
  completed_sessions: number;
  notes?: string;
}

export interface TrainingPlanResponse extends TrainingPlanBase {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface TrainingPlanDetailResponse extends TrainingPlanResponse {
  weeks: TrainingPlanWeekResponse[];
}

// ---------------------------------------------------------------------------
// Race Event
// ---------------------------------------------------------------------------

export interface RaceEventBase {
  name: string;
  sport_id: number;
  event_date: string;
  distance_km?: number;
  location?: string;
  target_time_seconds?: number;
  notes?: string;
}

export interface RaceEventCreate extends RaceEventBase {}

export interface RaceEventUpdate {
  name?: string;
  sport_id?: number;
  event_date?: string;
  distance_km?: number;
  location?: string;
  target_time_seconds?: number;
  notes?: string;
}

export interface RaceEventResponse extends RaceEventBase {
  id: number;
  user_id: number;
  created_at: string;
}
