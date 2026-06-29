import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DeportesService } from '../../services/deportes.service';
import {
  SportResponse,
  SportActivityResponse,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-activity-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="activity-detail">
      @if (loading()) {
        <div class="loading">Loading activity...</div>
      } @else if (activity()) {
        <div class="header">
          <a routerLink="/deportes/activities" class="back-link">← Back to Activities</a>
          <h2>{{ getSportName(activity()!.sport_id) }} Activity</h2>
          <span class="date">{{ activity()!.date | date:'fullDate' }}</span>
        </div>

        @if (!editMode) {
          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-value">{{ formatDuration(activity()!.duration_seconds) }}</span>
              <span class="stat-label">Duration</span>
            </div>
            @if (activity()!.distance_km) {
              <div class="stat-card">
                <span class="stat-value">{{ activity()!.distance_km | number:'1.2-2' }}</span>
                <span class="stat-label">km</span>
              </div>
            }
            @if (activity()!.calories) {
              <div class="stat-card">
                <span class="stat-value">{{ activity()!.calories }}</span>
                <span class="stat-label">Calories</span>
              </div>
            }
            @if (activity()!.heart_rate_avg) {
              <div class="stat-card">
                <span class="stat-value">{{ activity()!.heart_rate_avg }}</span>
                <span class="stat-label">Avg HR</span>
              </div>
            }
          </div>

          @if (activity()!.notes) {
            <div class="notes-section">
              <h3>Notes</h3>
              <p>{{ activity()!.notes }}</p>
            </div>
          }

          <div class="actions">
            <button class="btn-secondary" (click)="editMode = true">Edit</button>
            <button class="btn-danger" (click)="deleteActivity()">Delete</button>
          </div>
        } @else {
          <div class="edit-form">
            <div class="form-row">
              <label>Date</label>
              <input type="date" [(ngModel)]="editData.date" />
            </div>
            <div class="form-row">
              <label>Duration (seconds)</label>
              <input type="number" [(ngModel)]="editData.duration_seconds" />
            </div>
            <div class="form-row">
              <label>Distance (km)</label>
              <input type="number" step="0.1" [(ngModel)]="editData.distance_km" />
            </div>
            <div class="form-row">
              <label>Calories</label>
              <input type="number" [(ngModel)]="editData.calories" />
            </div>
            <div class="form-row">
              <label>Avg Heart Rate</label>
              <input type="number" [(ngModel)]="editData.heart_rate_avg" />
            </div>
            <div class="form-row">
              <label>Notes</label>
              <textarea [(ngModel)]="editData.notes" rows="3"></textarea>
            </div>
            <div class="form-actions">
              <button class="btn-primary" (click)="saveEdit()" [disabled]="saving()">
                {{ saving() ? 'Saving...' : 'Save' }}
              </button>
              <button class="btn-secondary" (click)="editMode = false">Cancel</button>
            </div>
          </div>
        }
      } @else {
        <div class="error">Activity not found.</div>
      }
    </div>
  `,
  styles: [`
    .activity-detail {
      padding: 1.5rem;
    }
    .header {
      margin-bottom: 2rem;
    }
    .back-link {
      color: var(--color-accent-primary, #6366f1);
      text-decoration: none;
      font-size: 0.9rem;
    }
    .back-link:hover {
      text-decoration: underline;
    }
    .header h2 {
      margin: 0.5rem 0 0.25rem 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .date {
      font-size: 0.9rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }
    .stat-card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
    }
    .stat-value {
      display: block;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-text-primary, #e2e8f0);
    }
    .stat-label {
      display: block;
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
      margin-top: 0.25rem;
    }
    .notes-section {
      margin-bottom: 2rem;
    }
    .notes-section h3 {
      color: var(--color-text-primary, #e2e8f0);
      margin-bottom: 0.5rem;
    }
    .notes-section p {
      color: var(--color-text-secondary, #94a3b8);
      margin: 0;
    }
    .actions {
      display: flex;
      gap: 1rem;
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
    .btn-secondary {
      padding: 0.5rem 1rem;
      background: transparent;
      color: var(--color-text-primary, #e2e8f0);
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 8px;
      cursor: pointer;
    }
    .btn-danger {
      padding: 0.5rem 1rem;
      background: transparent;
      color: #ef4444;
      border: 1px solid #ef4444;
      border-radius: 8px;
      cursor: pointer;
    }
    .btn-danger:hover {
      background: #ef4444;
      color: white;
    }
    .edit-form {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
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
    .form-row input, .form-row textarea {
      padding: 0.5rem;
      background: var(--color-glass-background, rgba(255,255,255,0.05));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--color-text-primary, #e2e8f0);
      font-size: 0.9rem;
    }
    .form-actions {
      display: flex;
      gap: 0.75rem;
      margin-top: 1rem;
    }
    .loading, .error {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
  `],
})
export class ActivityDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly deportesService = inject(DeportesService);

  activity = signal<SportActivityResponse | null>(null);
  sports = signal<SportResponse[]>([]);
  loading = signal(true);
  saving = signal(false);
  editMode = false;
  editData = {
    date: '',
    duration_seconds: 0,
    distance_km: undefined as number | undefined,
    calories: undefined as number | undefined,
    heart_rate_avg: undefined as number | undefined,
    notes: undefined as string | undefined,
  };

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.deportesService.listSports().subscribe({
      next: (sports) => this.sports.set(sports),
    });
    if (id) {
      this.loadActivity(id);
    }
  }

  loadActivity(id: number): void {
    this.loading.set(true);
    this.deportesService.getActivity(id).subscribe({
      next: (activity) => {
        this.activity.set(activity);
        this.editData = {
          date: activity.date,
          duration_seconds: activity.duration_seconds,
          distance_km: activity.distance_km,
          calories: activity.calories,
          heart_rate_avg: activity.heart_rate_avg,
          notes: activity.notes,
        };
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

  saveEdit(): void {
    const id = this.activity()?.id;
    if (!id) return;
    this.saving.set(true);
    this.deportesService.updateActivity(id, this.editData).subscribe({
      next: (updated) => {
        this.activity.set(updated);
        this.editMode = false;
        this.saving.set(false);
      },
      error: () => {
        this.saving.set(false);
      },
    });
  }

  deleteActivity(): void {
    const id = this.activity()?.id;
    if (!id) return;
    if (confirm('Are you sure you want to delete this activity?')) {
      this.deportesService.deleteActivity(id).subscribe({
        next: () => {
          window.location.href = '/deportes/activities';
        },
      });
    }
  }
}
