import { Component, inject, Input, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GimnasioService } from '../../services/gimnasio.service';
import { AISuggestionResponse } from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-ai-coach',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="ai-coach">
      <div class="header">
        <h3>AI Coach</h3>
        <span class="badge">Beta</span>
      </div>

      @if (loading()) {
        <div class="loading">Getting suggestion...</div>
      } @else if (suggestion()) {
        <div class="suggestion-card">
          <div class="exercise-info">
            <span class="exercise-name">{{ suggestion()!.exercise_name }}</span>
          </div>
          <div class="weights">
            <div class="weight current">
              <label>Current</label>
              <span>{{ suggestion()!.current_weight }}kg</span>
            </div>
            <div class="arrow">→</div>
            <div class="weight suggested">
              <label>Suggested</label>
              <span>{{ suggestion()!.suggested_weight }}kg</span>
            </div>
          </div>
          <div class="reason">
            <p>{{ suggestion()!.reason }}</p>
          </div>
          <div class="confidence">
            <label>Confidence</label>
            <div class="confidence-bar">
              <div
                class="confidence-fill"
                [style.width.%]="suggestion()!.confidence * 100"
              ></div>
            </div>
            <span class="confidence-value">{{ (suggestion()!.confidence * 100) | number:'1.0-0' }}%</span>
          </div>
        </div>
      } @else {
        <div class="no-suggestion">
          <p>No suggestion available for this exercise.</p>
          <p class="hint">Complete more workouts to get personalized suggestions.</p>
        </div>
      }
    </div>
  `,
  styles: [`
    .ai-coach {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
    }
    .header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .header h3 {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .badge {
      padding: 0.2rem 0.5rem;
      background: var(--color-accent-primary, #6366f1);
      color: white;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 500;
    }
    .loading {
      text-align: center;
      padding: 1rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .suggestion-card {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .exercise-info {
      margin-bottom: 0.5rem;
    }
    .exercise-name {
      font-weight: 600;
      color: var(--color-text-primary, #e2e8f0);
    }
    .weights {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1.5rem;
    }
    .weight {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.25rem;
    }
    .weight label {
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .weight span {
      font-size: 1.5rem;
      font-weight: 700;
    }
    .weight.current span {
      color: var(--color-text-primary, #e2e8f0);
    }
    .weight.suggested span {
      color: var(--color-accent-secondary, #10b981);
    }
    .arrow {
      font-size: 1.5rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .reason {
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      border-radius: 8px;
      padding: 0.75rem;
    }
    .reason p {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
      font-size: 0.9rem;
    }
    .confidence {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .confidence label {
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .confidence-bar {
      flex: 1;
      height: 6px;
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      border-radius: 3px;
      overflow: hidden;
    }
    .confidence-fill {
      height: 100%;
      background: var(--color-accent-primary, #6366f1);
      border-radius: 3px;
      transition: width 0.3s ease;
    }
    .confidence-value {
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--color-text-primary, #e2e8f0);
      min-width: 35px;
    }
    .no-suggestion {
      text-align: center;
      padding: 1rem;
    }
    .no-suggestion p {
      margin: 0;
      color: var(--color-text-secondary, #94a3b8);
    }
    .no-suggestion .hint {
      font-size: 0.85rem;
      margin-top: 0.5rem;
    }
  `],
})
export class AiCoachComponent implements OnInit {
  @Input({ required: true }) exerciseId!: number;

  private readonly gimnasioService = inject(GimnasioService);

  suggestion = signal<AISuggestionResponse | null>(null);
  loading = signal(true);

  ngOnInit(): void {
    this.loadSuggestion();
  }

  loadSuggestion(): void {
    this.loading.set(true);
    this.gimnasioService.getAISuggestion(this.exerciseId).subscribe({
      next: (suggestion) => {
        this.suggestion.set(suggestion);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }
}
