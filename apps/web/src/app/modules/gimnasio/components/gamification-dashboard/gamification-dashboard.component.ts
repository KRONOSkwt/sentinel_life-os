import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GimnasioService } from '../../services/gimnasio.service';
import {
  GamificationStatsResponse,
  AchievementResponse,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-gamification-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="gamification-dashboard">
      <div class="header">
        <h2>Gamification</h2>
      </div>

      @if (loading()) {
        <div class="loading">Loading stats...</div>
      } @else {
        <div class="stats-grid">
          <div class="stat-card points">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <span class="stat-value">{{ stats()?.total_points || 0 }}</span>
              <span class="stat-label">Total Points</span>
            </div>
          </div>

          <div class="stat-card streak">
            <div class="stat-icon">🔥</div>
            <div class="stat-content">
              <span class="stat-value">{{ stats()?.current_streak || 0 }}</span>
              <span class="stat-label">Current Streak</span>
            </div>
          </div>

          <div class="stat-card best-streak">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <span class="stat-value">{{ stats()?.longest_streak || 0 }}</span>
              <span class="stat-label">Best Streak</span>
            </div>
          </div>

          <div class="stat-card level">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <span class="stat-value">Level {{ stats()?.level || 1 }}</span>
              <span class="stat-label">{{ getPointsToNextLevel() }} pts to next</span>
            </div>
          </div>
        </div>

        <div class="achievements-section">
          <h3>Achievements</h3>
          @if (achievements().length === 0) {
            <div class="empty">No achievements unlocked yet. Keep working out!</div>
          } @else {
            <div class="achievements-grid">
              @for (achievement of achievements(); track achievement.id) {
                <div class="achievement-card unlocked">
                  <div class="achievement-icon">{{ getAchievementIcon(achievement.achievement_key) }}</div>
                  <div class="achievement-info">
                    <span class="achievement-name">{{ getAchievementName(achievement.achievement_key) }}</span>
                    <span class="achievement-date">Unlocked: {{ achievement.unlocked_at | date:'shortDate' }}</span>
                  </div>
                </div>
              }
            </div>
          }

          <div class="locked-achievements">
            <h4>Locked Achievements</h4>
            <div class="achievements-grid">
              @for (achievement of lockedAchievements(); track achievement.key) {
                <div class="achievement-card locked">
                  <div class="achievement-icon">🔒</div>
                  <div class="achievement-info">
                    <span class="achievement-name">{{ achievement.name }}</span>
                    <span class="achievement-progress">{{ achievement.progress }}</span>
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    .gamification-dashboard {
      padding: 1.5rem;
    }
    .header {
      margin-bottom: 1.5rem;
    }
    .header h2 {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .loading {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }
    .stat-card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .stat-icon {
      font-size: 2rem;
    }
    .stat-content {
      display: flex;
      flex-direction: column;
    }
    .stat-value {
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-text-primary, #e2e8f0);
    }
    .stat-label {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .achievements-section h3 {
      color: var(--color-text-primary, #e2e8f0);
      margin-bottom: 1rem;
    }
    .empty {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .achievements-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }
    .achievement-card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 10px;
      padding: 1rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .achievement-card.unlocked {
      border-color: var(--color-accent-secondary, #10b981);
    }
    .achievement-card.locked {
      opacity: 0.6;
    }
    .achievement-icon {
      font-size: 1.5rem;
    }
    .achievement-info {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .achievement-name {
      font-weight: 500;
      color: var(--color-text-primary, #e2e8f0);
    }
    .achievement-date, .achievement-progress {
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .locked-achievements {
      margin-top: 2rem;
    }
    .locked-achievements h4 {
      color: var(--color-text-secondary, #94a3b8);
      margin-bottom: 1rem;
      font-size: 0.9rem;
    }
  `],
})
export class GamificationDashboardComponent implements OnInit {
  private readonly gimnasioService = inject(GimnasioService);

  stats = signal<GamificationStatsResponse | null>(null);
  achievements = signal<AchievementResponse[]>([]);
  loading = signal(true);

  private readonly achievementDefs = [
    { key: 'first_workout', name: 'First Workout', icon: '🎉', target: 1, progressFn: (s: GamificationStatsResponse) => `Complete 1 workout` },
    { key: 'iron_will', name: 'Iron Will', icon: '🔥', target: 7, progressFn: (s: GamificationStatsResponse) => `${s.current_streak}/7 day streak` },
    { key: 'century_club', name: 'Century Club', icon: '💯', target: 100, progressFn: (s: GamificationStatsResponse) => `${s.total_points} points` },
    { key: 'pr_master', name: 'PR Master', icon: '🏆', target: 50, progressFn: (s: GamificationStatsResponse) => `Log 50 PRs` },
    { key: 'weight_warrior', name: 'Weight Warrior', icon: '💪', target: 10, progressFn: (s: GamificationStatsResponse) => `10 exercises in a week` },
    { key: 'dedication', name: 'Dedication', icon: '📅', target: 30, progressFn: (s: GamificationStatsResponse) => `${s.current_streak}/30 day streak` },
    { key: 'centurion', name: 'Centurion', icon: '👑', target: 1000, progressFn: (s: GamificationStatsResponse) => `${s.total_points}/1000 points` },
    { key: 'iron_legend', name: 'Iron Legend', icon: '⚡', target: 100, progressFn: (s: GamificationStatsResponse) => `${s.current_streak}/100 day streak` },
    { key: 'perfect_week', name: 'Perfect Week', icon: '✨', target: 7, progressFn: (s: GamificationStatsResponse) => `Workout every day for 7 days` },
    { key: 'level_10', name: 'Level 10', icon: '🌟', target: 10, progressFn: (s: GamificationStatsResponse) => `Level ${s.level}/10` },
  ];

  lockedAchievements = signal<Array<{ key: string; name: string; icon: string; progress: string }>>([]);

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading.set(true);
    this.gimnasioService.getGamificationStats().subscribe({
      next: (stats) => {
        this.stats.set(stats);
        this.updateLockedAchievements(stats);
      },
    });

    this.gimnasioService.getAchievements().subscribe({
      next: (achievements) => {
        this.achievements.set(achievements);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  updateLockedAchievements(stats: GamificationStatsResponse): void {
    const unlockedKeys = new Set(this.achievements().map(a => a.achievement_key));
    const locked = this.achievementDefs
      .filter(def => !unlockedKeys.has(def.key))
      .map(def => ({
        key: def.key,
        name: def.name,
        icon: def.icon,
        progress: def.progressFn(stats),
      }));
    this.lockedAchievements.set(locked);
  }

  getPointsToNextLevel(): number {
    const currentLevel = this.stats()?.level || 1;
    const currentPoints = this.stats()?.total_points || 0;
    const nextLevelPoints = currentLevel * 500;
    return nextLevelPoints - currentPoints;
  }

  getAchievementIcon(key: string): string {
    return this.achievementDefs.find(d => d.key === key)?.icon || '🏅';
  }

  getAchievementName(key: string): string {
    return this.achievementDefs.find(d => d.key === key)?.name || key;
  }
}
