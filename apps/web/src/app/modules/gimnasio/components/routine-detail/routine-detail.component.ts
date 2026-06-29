import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { GimnasioService } from '../../services/gimnasio.service';
import {
  RoutineDetailResponse,
  RoutineExerciseResponse,
  ExerciseResponse,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-routine-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="routine-detail">
      @if (loading()) {
        <div class="loading">Loading routine...</div>
      } @else if (routine()) {
        <div class="header">
          <div class="title-row">
            <a routerLink="/gimnasio/routines" class="back-link">← Back to Routines</a>
            <h2>{{ routine()!.name }}</h2>
          </div>
          @if (routine()!.description) {
            <p class="description">{{ routine()!.description }}</p>
          }
        </div>

        <div class="exercises-section">
          <h3>Exercises</h3>
          @if (routine()!.exercises.length === 0) {
            <div class="empty">No exercises in this routine yet.</div>
          } @else {
            <div class="exercise-list">
              @for (exercise of routine()!.exercises; track exercise.id; let i = $index) {
                <div class="exercise-card">
                  <div class="exercise-header">
                    <span class="order">{{ i + 1 }}</span>
                    <span class="name">{{ exercise.exercise.name }}</span>
                    <span class="category badge">{{ exercise.exercise.category }}</span>
                  </div>
                  <div class="exercise-details">
                    <div class="detail">
                      <label>Sets</label>
                      <span>{{ exercise.target_sets }}</span>
                    </div>
                    <div class="detail">
                      <label>Reps</label>
                      <span>{{ exercise.target_reps }}</span>
                    </div>
                    <div class="detail">
                      <label>Muscles</label>
                      <span>{{ exercise.exercise.muscle_groups.join(', ') }}</span>
                    </div>
                  </div>
                </div>
              }
            </div>
          }
        </div>

        <div class="actions">
          <button class="btn-primary" (click)="startSession()">
            Start Workout
          </button>
          <button class="btn-secondary" (click)="editMode = !editMode">
            {{ editMode ? 'Cancel Edit' : 'Edit Routine' }}
          </button>
        </div>
      } @else {
        <div class="error">Routine not found.</div>
      }
    </div>
  `,
  styles: [`
    .routine-detail {
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
    .description {
      color: var(--color-text-secondary, #94a3b8);
      margin: 0;
    }
    .exercises-section h3 {
      color: var(--color-text-primary, #e2e8f0);
      margin-bottom: 1rem;
    }
    .empty {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .exercise-list {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .exercise-card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 10px;
      padding: 1rem;
    }
    .exercise-header {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
    }
    .order {
      width: 24px;
      height: 24px;
      background: var(--color-accent-primary, #6366f1);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .name {
      font-weight: 500;
      color: var(--color-text-primary, #e2e8f0);
    }
    .badge {
      padding: 0.2rem 0.5rem;
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      border-radius: 4px;
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .exercise-details {
      display: flex;
      gap: 1.5rem;
    }
    .detail {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .detail label {
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .detail span {
      color: var(--color-text-primary, #e2e8f0);
    }
    .actions {
      display: flex;
      gap: 1rem;
      margin-top: 2rem;
    }
    .btn-primary {
      padding: 0.6rem 1.2rem;
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
    .btn-secondary {
      padding: 0.6rem 1.2rem;
      background: transparent;
      color: var(--color-text-primary, #e2e8f0);
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 8px;
      cursor: pointer;
    }
    .loading, .error {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
  `],
})
export class RoutineDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly gimnasioService = inject(GimnasioService);

  routine = signal<RoutineDetailResponse | null>(null);
  loading = signal(true);
  editMode = false;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.loadRoutine(id);
    }
  }

  loadRoutine(id: number): void {
    this.loading.set(true);
    this.gimnasioService.getRoutine(id).subscribe({
      next: (routine) => {
        this.routine.set(routine);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  startSession(): void {
    const routineId = this.routine()?.id;
    if (routineId) {
      this.gimnasioService.startSession({ routine_id: routineId }).subscribe({
        next: (session) => {
          // Navigate to active session
          window.location.href = `/gimnasio/session/${session.id}`;
        },
      });
    }
  }
}
