import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { GimnasioService } from '../../services/gimnasio.service';
import {
  SessionResponse,
  SetResponse,
  SetCreate,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-workout-session',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="workout-session">
      @if (loading()) {
        <div class="loading">Loading session...</div>
      } @else if (session()) {
        <div class="header">
          <div class="title-row">
            <a routerLink="/gimnasio" class="back-link">← Back to Gym</a>
            <h2>Workout Session</h2>
          </div>
          <div class="session-meta">
            <span>Started: {{ session()!.started_at | date:'medium' }}</span>
            @if (session()!.duration_seconds) {
              <span>Duration: {{ formatDuration(session()!.duration_seconds!) }}</span>
            }
          </div>
        </div>

        @if (!session()!.completed_at) {
          <div class="active-session">
            <div class="set-logger">
              <h3>Log Set</h3>
              <div class="form-row">
                <div class="form-group">
                  <label>Exercise</label>
                  <select [(ngModel)]="newSet.exercise_id" class="form-control">
                    <option value="">Select exercise</option>
                    <!-- Exercise options would be loaded -->
                  </select>
                </div>
                <div class="form-group">
                  <label>Set #</label>
                  <input
                    type="number"
                    [(ngModel)]="newSet.set_number"
                    min="1"
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label>Weight (kg)</label>
                  <input
                    type="number"
                    [(ngModel)]="newSet.weight"
                    min="0"
                    step="0.5"
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label>Reps</label>
                  <input
                    type="number"
                    [(ngModel)]="newSet.reps"
                    min="1"
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label>RPE (1-10)</label>
                  <input
                    type="range"
                    [(ngModel)]="newSet.rpe"
                    min="1"
                    max="10"
                    step="0.5"
                    class="form-control"
                  />
                  <span class="rpe-value">{{ newSet.rpe }}</span>
                </div>
              </div>
              <button
                class="btn-primary"
                (click)="logSet()"
                [disabled]="!newSet.exercise_id"
              >
                Log Set
              </button>
            </div>

            <div class="logged-sets">
              <h3>Logged Sets</h3>
              @if (session()!.sets.length === 0) {
                <div class="empty">No sets logged yet.</div>
              } @else {
                <div class="sets-list">
                  @for (set of session()!.sets; track set.id) {
                    <div class="set-card" [class.pr]="set.is_pr">
                      <div class="set-info">
                        <span class="exercise">Exercise #{{ set.exercise_id }}</span>
                        <span class="set-number">Set {{ set.set_number }}</span>
                      </div>
                      <div class="set-details">
                        <span>{{ set.weight }}kg × {{ set.reps }}</span>
                        @if (set.rpe) {
                          <span class="rpe">RPE {{ set.rpe }}</span>
                        }
                        @if (set.is_pr) {
                          <span class="pr-badge">PR!</span>
                        }
                      </div>
                    </div>
                  }
                </div>
              }
            </div>

            <div class="actions">
              <button class="btn-success" (click)="completeSession()">
                Complete Session
              </button>
            </div>
          </div>
        } @else {
          <div class="completed-session">
            <div class="success-message">
              <h3>Session Completed!</h3>
              <p>Great workout! You've completed your session.</p>
            </div>
            <div class="session-summary">
              <div class="stat">
                <label>Total Sets</label>
                <span>{{ session()!.sets.length }}</span>
              </div>
              <div class="stat">
                <label>PRs</label>
                <span>{{ getPRCount() }}</span>
              </div>
              <div class="stat">
                <label>Duration</label>
                <span>{{ formatDuration(session()!.duration_seconds || 0) }}</span>
              </div>
            </div>
          </div>
        }
      } @else {
        <div class="error">Session not found.</div>
      }
    </div>
  `,
  styles: [`
    .workout-session {
      padding: 1.5rem;
    }
    .header {
      margin-bottom: 2rem;
    }
    .title-row {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      margin-bottom: 0.5rem;
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
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .session-meta {
      display: flex;
      gap: 1.5rem;
      color: var(--color-text-secondary, #94a3b8);
      font-size: 0.9rem;
    }
    .active-session {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
    }
    @media (max-width: 900px) {
      .active-session {
        grid-template-columns: 1fr;
      }
    }
    .set-logger {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.5rem;
    }
    .set-logger h3 {
      margin: 0 0 1rem 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .form-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    .form-group label {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .form-control {
      padding: 0.6rem;
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--color-text-primary, #e2e8f0);
    }
    select.form-control {
      cursor: pointer;
    }
    input[type="range"] {
      cursor: pointer;
    }
    .rpe-value {
      text-align: center;
      font-weight: 500;
      color: var(--color-accent-primary, #6366f1);
    }
    .btn-primary {
      width: 100%;
      padding: 0.75rem;
      background: var(--color-accent-primary, #6366f1);
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
    }
    .btn-primary:hover:not(:disabled) {
      background: var(--color-accent-hover, #5558e6);
    }
    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .logged-sets {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.5rem;
    }
    .logged-sets h3 {
      margin: 0 0 1rem 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .empty {
      text-align: center;
      padding: 1rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .sets-list {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    .set-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem;
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      border-radius: 8px;
    }
    .set-card.pr {
      border-left: 3px solid var(--color-accent-secondary, #10b981);
    }
    .set-info {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .exercise {
      font-size: 0.85rem;
      color: var(--color-text-primary, #e2e8f0);
    }
    .set-number {
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .set-details {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .rpe {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .pr-badge {
      padding: 0.2rem 0.5rem;
      background: var(--color-accent-secondary, #10b981);
      color: white;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 600;
    }
    .actions {
      grid-column: 1 / -1;
      display: flex;
      justify-content: center;
    }
    .btn-success {
      padding: 0.75rem 2rem;
      background: var(--color-accent-secondary, #10b981);
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
      font-size: 1rem;
    }
    .btn-success:hover {
      background: #059669;
    }
    .completed-session {
      text-align: center;
      padding: 2rem;
    }
    .success-message h3 {
      color: var(--color-accent-secondary, #10b981);
      margin-bottom: 0.5rem;
    }
    .success-message p {
      color: var(--color-text-secondary, #94a3b8);
      margin-bottom: 2rem;
    }
    .session-summary {
      display: flex;
      justify-content: center;
      gap: 3rem;
    }
    .stat {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    .stat label {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .stat span {
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--color-text-primary, #e2e8f0);
    }
    .loading, .error {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
  `],
})
export class WorkoutSessionComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly gimnasioService = inject(GimnasioService);

  session = signal<SessionResponse | null>(null);
  loading = signal(true);

  newSet: SetCreate = {
    exercise_id: 0,
    set_number: 1,
    weight: 0,
    reps: 1,
    rpe: 5,
  };

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.loadSession(id);
    }
  }

  loadSession(id: number): void {
    this.loading.set(true);
    this.gimnasioService.getSession(id).subscribe({
      next: (session) => {
        this.session.set(session);
        this.loading.set(false);
        // Set next set number
        if (session.sets.length > 0) {
          this.newSet.set_number = Math.max(...session.sets.map((s: SetResponse) => s.set_number)) + 1;
        }
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  logSet(): void {
    const sessionId = this.session()?.id;
    if (sessionId && this.newSet.exercise_id) {
      this.gimnasioService.logSet(sessionId, this.newSet).subscribe({
        next: (set) => {
          this.session.update(s => s ? { ...s, sets: [...s.sets, set] } : s);
          this.newSet.set_number++;
          this.newSet.weight = 0;
          this.newSet.reps = 1;
        },
      });
    }
  }

  completeSession(): void {
    const sessionId = this.session()?.id;
    if (sessionId) {
      this.gimnasioService.completeSession(sessionId, {}).subscribe({
        next: (session) => {
          this.session.set(session);
        },
      });
    }
  }

  getPRCount(): number {
    return this.session()?.sets.filter((s: SetResponse) => s.is_pr).length || 0;
  }

  formatDuration(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  }
}
