import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DeportesService } from '../../services/deportes.service';
import { TrainingPlanResponse } from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-training-plan-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="plan-list">
      <div class="header">
        <h2>Training Plans</h2>
        <button class="btn-primary" (click)="showCreate = !showCreate">
          {{ showCreate ? 'Cancel' : '+ New Plan' }}
        </button>
      </div>

      @if (showCreate) {
        <div class="create-form">
          <h3>Create Training Plan</h3>
          <div class="form-row">
            <label>Name</label>
            <input type="text" [(ngModel)]="newPlan.name" placeholder="e.g. Marathon Prep" />
          </div>
          <div class="form-row">
            <label>Description</label>
            <textarea [(ngModel)]="newPlan.description" rows="2"></textarea>
          </div>
          <div class="form-row">
            <label>Start Date</label>
            <input type="date" [(ngModel)]="newPlan.start_date" />
          </div>
          <div class="form-row">
            <label>End Date</label>
            <input type="date" [(ngModel)]="newPlan.end_date" />
          </div>
          <button class="btn-primary" (click)="createPlan()" [disabled]="saving()">
            {{ saving() ? 'Creating...' : 'Create Plan' }}
          </button>
        </div>
      }

      @if (loading()) {
        <div class="loading">Loading plans...</div>
      } @else if (plans().length === 0) {
        <div class="empty">
          <p>No training plans yet. Create one to structure your training!</p>
        </div>
      } @else {
        <div class="grid">
          @for (plan of plans(); track plan.id) {
            <div class="card">
              <div class="card-header">
                <h3>{{ plan.name }}</h3>
                <button class="btn-icon" (click)="deletePlan(plan.id)">×</button>
              </div>
              @if (plan.description) {
                <p class="description">{{ plan.description }}</p>
              }
              <div class="plan-dates">
                <span>{{ plan.start_date | date:'mediumDate' }} — {{ plan.end_date | date:'mediumDate' }}</span>
              </div>
              <div class="meta">
                <span>Created: {{ plan.created_at | date:'shortDate' }}</span>
              </div>
            </div>
          }
        </div>
      }
    </div>
  `,
  styles: [`
    .plan-list {
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
    .form-row input, .form-row textarea {
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
    .card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.5rem;
    }
    .card-header h3 {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .btn-icon {
      background: transparent;
      border: none;
      color: var(--color-text-secondary, #94a3b8);
      font-size: 1.2rem;
      cursor: pointer;
      padding: 0 0.25rem;
    }
    .btn-icon:hover {
      color: #ef4444;
    }
    .description {
      color: var(--color-text-secondary, #94a3b8);
      font-size: 0.9rem;
      margin: 0 0 0.75rem 0;
    }
    .plan-dates {
      font-size: 0.85rem;
      color: var(--color-accent-primary, #6366f1);
      margin-bottom: 0.5rem;
    }
    .meta {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
    }
  `],
})
export class TrainingPlanListComponent implements OnInit {
  private readonly deportesService = inject(DeportesService);

  plans = signal<TrainingPlanResponse[]>([]);
  loading = signal(true);
  saving = signal(false);
  showCreate = false;

  newPlan = {
    name: '',
    description: undefined as string | undefined,
    start_date: '',
    end_date: '',
  };

  ngOnInit(): void {
    this.loadPlans();
  }

  loadPlans(): void {
    this.loading.set(true);
    this.deportesService.listPlans().subscribe({
      next: (plans) => {
        this.plans.set(plans);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  createPlan(): void {
    if (!this.newPlan.name || !this.newPlan.start_date || !this.newPlan.end_date) {
      return;
    }
    this.saving.set(true);
    this.deportesService.createPlan(this.newPlan as any).subscribe({
      next: (plan) => {
        this.plans.update((list) => [plan, ...list]);
        this.showCreate = false;
        this.saving.set(false);
        this.newPlan = { name: '', description: undefined, start_date: '', end_date: '' };
      },
      error: () => {
        this.saving.set(false);
      },
    });
  }

  deletePlan(id: number): void {
    if (confirm('Are you sure you want to delete this plan?')) {
      this.deportesService.deletePlan(id).subscribe({
        next: () => {
          this.plans.update((list) => list.filter((p) => p.id !== id));
        },
      });
    }
  }
}
