/**
 * Shared TypeScript interfaces for gamification stats and achievements.
 */

export interface GamificationStatsBase {
  total_points: number;
  current_streak: number;
  longest_streak: number;
  level: number;
}

export interface GamificationStatsResponse extends GamificationStatsBase {
  last_workout_date?: string;
}

export interface AchievementBase {
  achievement_key: string;
}

export interface AchievementResponse extends AchievementBase {
  id: number;
  unlocked_at: string;
}
