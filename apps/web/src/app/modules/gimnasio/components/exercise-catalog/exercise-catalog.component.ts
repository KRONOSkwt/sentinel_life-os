import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GimnasioService } from '../../services/gimnasio.service';
import { ExerciseResponse } from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-exercise-catalog',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="exercise-catalog">
      <div class="header">
        <h2>Exercise Catalog</h2>
        <button class="btn-primary" (click)="showCreate = true">+ Custom Exercise</button>
      </div>

      <div class="filters">
        <input
          type="text"
          placeholder="Search exercises..."
          [(ngModel)]="searchTerm"
          (input)="onSearch()"
          class="search-input"
        />
        <div class="category-chips">
          @for (category of categories; track category) {
            <button
              class="chip"
              [class.active]="selectedCategory() === category"
              (click)="filterByCategory(category)"
            >
              {{ category }}
            </button>
          }
          @if (selectedCategory()) {
            <button class="chip clear" (click)="clearCategoryFilter()">Clear</button>
          }
        </div>
      </div>

      @if (loading()) {
        <div class="loading">Loading exercises...</div>
      } @else if (exercises().length === 0) {
        <div class="empty">No exercises found.</div>
      } @else {
        <div class="grid">
          @for (exercise of exercises(); track exercise.id) {
            <div class="card">
              <div class="card-header">
                <h3>{{ exercise.name }}</h3>
                @if (exercise.is_custom) {
                  <span class="custom-badge">Custom</span>
                }
              </div>
              <div class="card-body">
                <div class="detail">
                  <label>Category</label>
                  <span class="badge">{{ exercise.category }}</span>
                </div>
                <div class="detail">
                  <label>Muscles</label>
                  <span>{{ exercise.muscle_groups.join(', ') }}</span>
                </div>
                @if (exercise.equipment) {
                  <div class="detail">
                    <label>Equipment</label>
                    <span>{{ exercise.equipment }}</span>
                  </div>
                }
              </div>
            </div>
          }
        </div>
      }
    </div>
  `,
  styles: [`
    .exercise-catalog {
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
    .filters {
      margin-bottom: 1.5rem;
    }
    .search-input {
      width: 100%;
      padding: 0.75rem 1rem;
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 8px;
      color: var(--color-text-primary, #e2e8f0);
      font-size: 1rem;
      margin-bottom: 1rem;
    }
    .search-input::placeholder {
      color: var(--color-text-secondary, #94a3b8);
    }
    .category-chips {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .chip {
      padding: 0.4rem 0.8rem;
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 999px;
      color: var(--color-text-secondary, #94a3b8);
      cursor: pointer;
      font-size: 0.85rem;
    }
    .chip:hover {
      background: var(--color-glass-border, rgba(255,255,255,0.2));
    }
    .chip.active {
      background: var(--color-accent-primary, #6366f1);
      color: white;
      border-color: var(--color-accent-primary, #6366f1);
    }
    .chip.clear {
      background: transparent;
      color: var(--color-text-secondary, #94a3b8);
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
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .card-header h3 {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .custom-badge {
      padding: 0.2rem 0.5rem;
      background: var(--color-accent-secondary, #10b981);
      color: white;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 500;
    }
    .card-body {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
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
    .badge {
      display: inline-block;
      padding: 0.2rem 0.5rem;
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      border-radius: 4px;
      font-size: 0.8rem;
    }
  `],
})
export class ExerciseCatalogComponent implements OnInit {
  private readonly gimnasioService = inject(GimnasioService);

  exercises = signal<ExerciseResponse[]>([]);
  loading = signal(true);
  searchTerm = '';
  selectedCategory = signal<string | null>(null);
  showCreate = false;

  readonly categories = ['strength', 'cardio', 'flexibility'];

  ngOnInit(): void {
    this.loadExercises();
  }

  loadExercises(): void {
    this.loading.set(true);
    this.gimnasioService
      .searchExercises({
        category: this.selectedCategory() || undefined,
        search: this.searchTerm || undefined,
      })
      .subscribe({
        next: (exercises) => {
          this.exercises.set(exercises);
          this.loading.set(false);
        },
        error: () => {
          this.loading.set(false);
        },
      });
  }

  onSearch(): void {
    this.loadExercises();
  }

  filterByCategory(category: string): void {
    this.selectedCategory.set(category);
    this.loadExercises();
  }

  clearCategoryFilter(): void {
    this.selectedCategory.set(null);
    this.loadExercises();
  }
}
