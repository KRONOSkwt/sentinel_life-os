import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DeportesService } from '../../services/deportes.service';
import {
  SportResponse,
  RaceEventResponse,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-race-calendar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="race-calendar">
      <div class="header">
        <h2>Race Calendar</h2>
        <button class="btn-primary" (click)="showCreate = !showCreate">
          {{ showCreate ? 'Cancel' : '+ Add Race' }}
        </button>
      </div>

      @if (showCreate) {
        <div class="create-form">
          <h3>Add Race Event</h3>
          <div class="form-row">
            <label>Name</label>
            <input type="text" [(ngModel)]="newRace.name" placeholder="e.g. Buenos Aires Marathon" />
          </div>
          <div class="form-row">
            <label>Sport</label>
            <select [(ngModel)]="newRace.sport_id">
              <option [ngValue]="0" disabled>Select sport...</option>
              @for (sport of sports(); track sport.id) {
                <option [ngValue]="sport.id">{{ sport.name }}</option>
              }
            </select>
          </div>
          <div class="form-row">
            <label>Date</label>
            <input type="date" [(ngModel)]="newRace.event_date" />
          </div>
          <div class="form-row">
            <label>Distance (km)</label>
            <input type="number" step="0.1" [(ngModel)]="newRace.distance_km" />
          </div>
          <div class="form-row">
            <label>Location</label>
            <input type="text" [(ngModel)]="newRace.location" />
          </div>
          <div class="form-row">
            <label>Target Time (seconds)</label>
            <input type="number" [(ngModel)]="newRace.target_time_seconds" />
          </div>
          <div class="form-row">
            <label>Notes</label>
            <textarea [(ngModel)]="newRace.notes" rows="2"></textarea>
          </div>
          <button class="btn-primary" (click)="createRace()" [disabled]="saving()">
            {{ saving() ? 'Adding...' : 'Add Race' }}
          </button>
        </div>
      }

      @if (loading()) {
        <div class="loading">Loading races...</div>
      } @else if (races().length === 0) {
        <div class="empty">
          <p>No races scheduled. Add your first race event!</p>
        </div>
      } @else {
        <div class="grid">
          @for (race of races(); track race.id) {
            <div class="card" [class.past]="isPast(race.event_date)">
              <div class="card-header">
                <h3>{{ race.name }}</h3>
                <button class="btn-icon" (click)="deleteRace(race.id)">×</button>
              </div>
              <div class="race-date" [class.upcoming]="!isPast(race.event_date)">
                {{ race.event_date | date:'fullDate' }}
                @if (!isPast(race.event_date)) {
                  <span class="days-badge">{{ daysUntil(race.event_date) }}d</span>
                }
              </div>
              <div class="race-details">
                <span class="sport-badge">{{ getSportName(race.sport_id) }}</span>
                @if (race.distance_km) {
                  <span class="detail">{{ race.distance_km | number:'1.1-1' }} km</span>
                }
                @if (race.location) {
                  <span class="detail">{{ race.location }}</span>
                }
              </div>
              @if (race.target_time_seconds) {
                <div class="target">
                  Target: {{ formatDuration(race.target_time_seconds) }}
                </div>
              }
            </div>
          }
        </div>
      }
    </div>
  `,
  styles: [`
    .race-calendar {
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
    .card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 1.25rem;
    }
    .card.past {
      opacity: 0.6;
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
    .race-date {
      font-size: 0.9rem;
      color: var(--color-text-secondary, #94a3b8);
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .race-date.upcoming {
      color: var(--color-accent-primary, #6366f1);
    }
    .days-badge {
      padding: 0.15rem 0.5rem;
      background: var(--color-accent-primary, rgba(99, 102, 241, 0.15));
      color: var(--color-accent-primary, #6366f1);
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .race-details {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 0.5rem;
    }
    .sport-badge {
      padding: 0.2rem 0.6rem;
      background: var(--color-accent-primary, rgba(99, 102, 241, 0.15));
      color: var(--color-accent-primary, #6366f1);
      border-radius: 16px;
      font-size: 0.75rem;
      font-weight: 500;
    }
    .detail {
      font-size: 0.85rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .target {
      font-size: 0.85rem;
      color: var(--color-text-primary, #e2e8f0);
      margin-top: 0.5rem;
    }
  `],
})
export class RaceCalendarComponent implements OnInit {
  private readonly deportesService = inject(DeportesService);

  races = signal<RaceEventResponse[]>([]);
  sports = signal<SportResponse[]>([]);
  loading = signal(true);
  saving = signal(false);
  showCreate = false;

  newRace = {
    name: '',
    sport_id: 0,
    event_date: '',
    distance_km: undefined as number | undefined,
    location: undefined as string | undefined,
    target_time_seconds: undefined as number | undefined,
    notes: undefined as string | undefined,
  };

  ngOnInit(): void {
    this.loadRaces();
    this.deportesService.listSports().subscribe({
      next: (sports) => this.sports.set(sports),
    });
  }

  loadRaces(): void {
    this.loading.set(true);
    this.deportesService.listRaces().subscribe({
      next: (races) => {
        // Sort: upcoming first, then past
        const now = new Date().toISOString().split('T')[0];
        const upcoming = races.filter((r) => r.event_date >= now);
        const past = races.filter((r) => r.event_date < now);
        this.races.set([...upcoming, ...past]);
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

  isPast(dateStr: string): boolean {
    return dateStr < new Date().toISOString().split('T')[0];
  }

  daysUntil(dateStr: string): number {
    const now = new Date();
    const target = new Date(dateStr);
    return Math.ceil((target.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  }

  formatDuration(seconds: number): string {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
  }

  createRace(): void {
    if (!this.newRace.name || !this.newRace.sport_id || !this.newRace.event_date) {
      return;
    }
    this.saving.set(true);
    this.deportesService.createRace(this.newRace as any).subscribe({
      next: (race) => {
        this.loadRaces(); // Re-sort
        this.showCreate = false;
        this.saving.set(false);
        this.resetForm();
      },
      error: () => {
        this.saving.set(false);
      },
    });
  }

  deleteRace(id: number): void {
    if (confirm('Are you sure you want to delete this race?')) {
      this.deportesService.deleteRace(id).subscribe({
        next: () => {
          this.races.update((list) => list.filter((r) => r.id !== id));
        },
      });
    }
  }

  private resetForm(): void {
    this.newRace = {
      name: '',
      sport_id: 0,
      event_date: '',
      distance_km: undefined,
      location: undefined,
      target_time_seconds: undefined,
      notes: undefined,
    };
  }
}
