import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DeportesService } from '../../services/deportes.service';
import {
  SportResponse,
  SportActivityResponse,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-activity-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="activity-list">
      <div class="header">
        <h2>Activities</h2>
        <button class="btn-primary" (click)="showCreate = !showCreate">
          {{ showCreate ? 'Cancel' : '+ Log Activity' }}
        </button>
      </div>

      @if (showCreate) {
        <div class="create-form">
          <h3>Log New Activity</h3>
          <div class="form-row">
            <label>Sport</label>
            <select [(ngModel)]="newActivity.sport_id">
              <option [ngValue]="0" disabled>Select sport...</option>
              @for (sport of sports(); track sport.id) {
                <option [ngValue]="sport.id">{{ sport.name }}</option>
              }
            </select>
          </div>
          <div class="form-row">
            <label>Date</label>
            <input type="date" [(ngModel)]="newActivity.date" />
          </div>
          <div class="form-row">
            <label>Duration (seconds)</label>
            <input type="number" [(ngModel)]="newActivity.duration_seconds" />
          </div>
          <div class="form-row">
            <label>Distance (km)</label>
            <input type="number" step="0.1" [(ngModel)]="newActivity.distance_km" />
          </div>
          <div class="form-row">
            <label>Calories</label>
            <input type="number" [(ngModel)]="newActivity.calories" />
          </div>
          <div class="form-row">
            <label>Notes</label>
            <textarea [(ngModel)]="newActivity.notes" rows="2"></textarea>
          </div>
          <button class="btn-primary" (click)="createActivity()" [disabled]="saving()">
            {{ saving() ? 'Saving...' : 'Save Activity' }}
          </button>
        </div>
      }

      @if (loading()) {
        <div class="loading">Loading activities...</div>
      } @else if (activities().length === 0) {
        <div class="empty">
          <p>No activities logged yet. Start tracking your sports!</p>
        </div>
      } @else {
        <div class="grid">
          @for (activity of activities(); track activity.id) {
            <a [routerLink]="['/deportes/activities', activity.id]" class="card-link">
              <div class="card">
                <div class="card-header">
                  <span class="sport-badge">{{ getSportName(activity.sport_id) }}</span>
                  <span class="date">{{ activity.date | date:'mediumDate' }}</span>
                </div>
                <div class="card-stats">
                  <div class="stat">
                    <span class="stat-value">{{ formatDuration(activity.duration_seconds) }}</span>
                    <span class="stat-label">Duration</span>
                  </div>
                  @if (activity.distance_km) {
                    <div class="stat">
                      <span class="stat-value">{{ activity.distance_km | number:'1.1-1' }}</span>
                      <span class="stat-label">km</span>
                    </div>
                  }
                  @if (activity.calories) {
                    <div class="stat">
                      <span class="stat-value">{{ activity.calories }}</span>
                      <span class="stat-label">cal</span>
                    </div>
                  }
                </div>
                @if (activity.notes) {
                  <p class="notes">{{ activity.notes }}</p>
                }
              </div>
            </a>
          }
        </div>
      }
    </div>
  `,
  styles: [`
    .activity-list {
      padding: 1.5rem;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }
    .header h2 {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .btn-primary {
      padding: 0.5rem 1rem;
      background: var(--color-accent-primary, #6366f1);
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
    }
    .btn-primary:hover {
      background: var(--color-accent-hover, #5558e6);
    }
    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .loading, .empty {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .create-form {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
    }
    .create-form h3 {
      margin: 0 0 1rem 0;
      color: var(--color-text-primary, #e2e8f0);
      font-size: 1rem;
    }
    .form-row {
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
      margin-bottom: 0.75rem;
    }
    .form-row label {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .form-row input, .form-row select, .form-row textarea {
      padding: 0.5rem;
      background: var(--color-glass-background, rgba(255,255,255,0.05));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--color-text-primary, #e2e8f0);
      font-size: 0.9rem;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }
    .card-link {
      text-decoration: none;
    }
    .card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
      transition: border-color 0.2s;
    }
    .card:hover {
      border-color: var(--color-accent-primary, #6366f1);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .sport-badge {
      padding: 0.25rem 0.75rem;
      background: var(--color-accent-primary, rgba(99, 102, 241, 0.15));
      color: var(--color-accent-primary, #6366f1);
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 500;
    }
    .date {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .card-stats {
      display: flex;
      gap: 1.5rem;
    }
    .stat {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }
    .stat-value {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--color-text-primary, #e2e8f0);
    }
    .stat-label {
      font-size: 0.7rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .notes {
      margin: 0.75rem 0 0 0;
      font-size: 0.85rem;
      color: var(--color-text-secondary, #94a3b8);
    }
  `],
})
export class ActivityListComponent implements OnInit {
  private readonly deportesService = inject(DeportesService);

  activities = signal<SportActivityResponse[]>([]);
  sports = signal<SportResponse[]>([]);
  loading = signal(true);
  saving = signal(false);
  showCreate = false;

  newActivity = {
    sport_id: 0,
    date: new Date().toISOString().split('T')[0],
    duration_seconds: 0,
    distance_km: undefined as number | undefined,
    calories: undefined as number | undefined,
    notes: undefined as string | undefined,
  };

  ngOnInit(): void {
    this.loadActivities();
    this.deportesService.listSports().subscribe({
      next: (sports) => this.sports.set(sports),
    });
  }

  loadActivities(): void {
    this.loading.set(true);
    this.deportesService.listActivities().subscribe({
      next: (activities) => {
        this.activities.set(activities);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  getSportName(sportId: number): string {
    return this.sports().find((s) => s.id === sportId)?.name ?? 'Sport';
  }

  formatDuration(seconds: number): string {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (h > 0) return `${h}h ${m}m`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
  }

  createActivity(): void {
    if (!this.newActivity.sport_id || !this.newActivity.date || this.newActivity.duration_seconds <= 0) {
      return;
    }
    this.saving.set(true);
    this.deportesService.logActivity(this.newActivity as any).subscribe({
      next: (activity) => {
        this.activities.update((list) => [activity, ...list]);
        this.showCreate = false;
        this.saving.set(false);
        this.resetForm();
      },
      error: () => {
        this.saving.set(false);
      },
    });
  }

  private resetForm(): void {
    this.newActivity = {
      sport_id: 0,
      date: new Date().toISOString().split('T')[0],
      duration_seconds: 0,
      distance_km: undefined,
      calories: undefined,
      notes: undefined,
    };
  }
}
