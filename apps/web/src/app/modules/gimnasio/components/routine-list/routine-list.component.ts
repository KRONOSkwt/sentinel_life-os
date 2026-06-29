import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { GimnasioService } from '../../services/gimnasio.service';
import { RoutineResponse } from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-routine-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="routine-list">
      <div class="header">
        <h2>Routines</h2>
        <button class="btn-primary" (click)="showCreate = true">+ New Routine</button>
      </div>

      @if (loading()) {
        <div class="loading">Loading routines...</div>
      } @else if (routines().length === 0) {
        <div class="empty">
          <p>No routines yet. Create your first routine to get started!</p>
        </div>
      } @else {
        <div class="grid">
          @for (routine of routines(); track routine.id) {
            <div class="card">
              <h3>{{ routine.name }}</h3>
              @if (routine.description) {
                <p class="description">{{ routine.description }}</p>
              }
              <div class="meta">
                <span>Created: {{ routine.created_at | date:'shortDate' }}</span>
                <span>Updated: {{ routine.updated_at | date:'shortDate' }}</span>
              </div>
              <div class="actions">
                <a [routerLink]="['/gimnasio/routines', routine.id]" class="btn-secondary">
                  View
                </a>
                <button class="btn-danger" (click)="deleteRoutine(routine.id)">
                  Delete
                </button>
              </div>
            </div>
          }
        </div>
      }
    </div>
  `,
  styles: [`
    .routine-list {
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
    .loading, .empty {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }
    .card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
    }
    .card h3 {
      margin: 0 0 0.5rem 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .description {
      color: var(--color-text-secondary, #94a3b8);
      font-size: 0.9rem;
      margin: 0 0 0.75rem 0;
    }
    .meta {
      display: flex;
      gap: 1rem;
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
      margin-bottom: 1rem;
    }
    .actions {
      display: flex;
      gap: 0.5rem;
    }
    .btn-secondary {
      padding: 0.4rem 0.8rem;
      background: transparent;
      color: var(--color-accent-primary, #6366f1);
      border: 1px solid var(--color-accent-primary, #6366f1);
      border-radius: 6px;
      text-decoration: none;
      font-size: 0.85rem;
    }
    .btn-danger {
      padding: 0.4rem 0.8rem;
      background: transparent;
      color: #ef4444;
      border: 1px solid #ef4444;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
    }
    .btn-danger:hover {
      background: #ef4444;
      color: white;
    }
  `],
})
export class RoutineListComponent implements OnInit {
  private readonly gimnasioService = inject(GimnasioService);

  routines = signal<RoutineResponse[]>([]);
  loading = signal(true);
  showCreate = false;

  ngOnInit(): void {
    this.loadRoutines();
  }

  loadRoutines(): void {
    this.loading.set(true);
    this.gimnasioService.listRoutines().subscribe({
      next: (routines) => {
        this.routines.set(routines);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  deleteRoutine(id: number): void {
    if (confirm('Are you sure you want to delete this routine?')) {
      this.gimnasioService.deleteRoutine(id).subscribe({
        next: () => {
          this.routines.update((routines) => routines.filter((r) => r.id !== id));
        },
      });
    }
  }
}
