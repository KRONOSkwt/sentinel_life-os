/**
 * Shared TypeScript interfaces for workout sessions and sets.
 */

export interface SetBase {
  exercise_id: number;
  set_number: number;
  weight: number;
  reps: number;
  rpe?: number;
}

export interface SetCreate extends SetBase {}

export interface SetResponse extends SetBase {
  id: number;
  session_id: number;
  is_pr: boolean;
  created_at: string;
}

export interface SessionBase {
  routine_id?: number;
}

export interface SessionCreate extends SessionBase {}

export interface SessionComplete {
  notes?: string;
}

export interface SessionResponse {
  id: number;
  user_id: number;
  routine_id?: number;
  started_at: string;
  completed_at?: string;
  duration_seconds?: number;
  notes?: string;
  sets: SetResponse[];
  created_at: string;
}

export interface WeightChartEntry {
  date: string;
  weight: number;
  reps: number;
  set_number: number;
}

export interface WeightChartResponse {
  exercise_id: number;
  exercise_name: string;
  data: WeightChartEntry[];
}
