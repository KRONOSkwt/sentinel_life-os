/**
 * Shared TypeScript interfaces for workout routines and exercises.
 */

export interface ExerciseBase {
  name: string;
  category: 'strength' | 'cardio' | 'flexibility';
  muscle_groups: string[];
  equipment?: string;
}

export interface ExerciseCreate extends ExerciseBase {}

export interface ExerciseResponse extends ExerciseBase {
  id: number;
  is_custom: boolean;
  created_at: string;
}

export interface RoutineExerciseBase {
  exercise_id: number;
  target_sets: number;
  target_reps: number;
  order: number;
}

export interface RoutineExerciseCreate extends RoutineExerciseBase {}

export interface RoutineExerciseResponse extends RoutineExerciseBase {
  id: number;
  exercise: ExerciseResponse;
}

export interface RoutineBase {
  name: string;
  description?: string;
}

export interface RoutineCreate extends RoutineBase {
  exercises: RoutineExerciseCreate[];
}

export interface RoutineUpdate {
  name?: string;
  description?: string;
  exercises?: RoutineExerciseCreate[];
}

export interface RoutineResponse extends RoutineBase {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface RoutineDetailResponse extends RoutineResponse {
  exercises: RoutineExerciseResponse[];
}
