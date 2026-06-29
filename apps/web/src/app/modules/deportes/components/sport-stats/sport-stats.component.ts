import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DeportesService } from '../../services/deportes.service';
import {
  SportResponse,
  SportStatsResponse,
  PersonalRecordResponse,
} from '@sentinel/shared/models/typescript';

@Component({
  selector: 'sl-sport-stats',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="sport-stats">
      <div class="header">
        <h2>Sport Records</h2>
      </div>

      <div class="sport-selector">
        <label>Select Sport</label>
        <select [(ngModel)]="selectedSportId" (change)="onSportChange()">
          <option [ngValue]="0" disabled>Choose a sport...</option>
          @for (sport of sports(); track sport.id) {
            <option [ngValue]="sport.id">{{ sport.name }}</option>
          }
        </select>
      </div>

      @if (loading()) {
        <div class="loading">Loading stats...</div>
      } @else if (stats()) {
        <div class="stats-section">
          <h3>Overall Stats</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-value">{{ stats()!.total_activities }}</span>
              <span class="stat-label">Activities</span>
            </div>
            <div class="stat-card">
              <span class="stat-value">{{ formatDuration(stats()!.total_time_seconds) }}</span>
              <span class="stat-label">Total Time</span>
            </div>
            @if (stats()!.total_distance_km) {
              <div class="stat-card">
                <span class="stat-value">{{ stats()!.total_distance_km | number:'1.1-1' }}</span>
                <span class="stat-label">Total km</span>
              </div>
            }
            @if (stats()!.average_duration_seconds) {
              <div class="stat-card">
                <span class="stat-value">{{ formatDuration(stats()!.average_duration_seconds!) }}</span>
                <span class="stat-label">Avg Duration</span>
              </div>
            }
          </div>
        </div>

        @if (personalRecords()) {
          <div class="records-section">
            <h3>Personal Records</h3>
            <div class="records-list">
              @if (personalRecords()!.best_time_seconds) {
                <div class="record-card">
                  <span class="record-label">Best Time</span>
                  <span class="record-value">{{ formatDuration(personalRecords()!.best_time_seconds!) }}</span>
                  @if (personalRecords()!.best_time_date) {
                    <span class="record-date">{{ personalRecords()!.best_time_date | date:'mediumDate' }}</span>
                  }
                </div>
              }
              @if (personalRecords()!.best_distance_km) {
                <div class="record-card">
                  <span class="record-label">Best Distance</span>
                  <span class="record-value">{{ personalRecords()!.best_distance_km | number:'1.2-2' }} km</span>
                  @if (personalRecords()!.best_distance_date) {
                    <span class="record-date">{{ personalRecords()!.best_distance_date | date:'mediumDate' }}</span>
                  }
                </div>
              }
              @if (personalRecords()!.best_pace_seconds_per_km) {
                <div class="record-card">
                  <span class="record-label">Best Pace</span>
                  <span class="record-value">{{ formatPace(personalRecords()!.best_pace_seconds_per_km!) }}</span>
                </div>
              }
            </div>
          </div>
        }

        <div class="chart-placeholder">
          <h3>Progress Chart</h3>
          <div class="placeholder-box">
            <p>Chart coming soon — track your progress over time.</p>
          </div>
        </div>
      } @else if (selectedSportId > 0) {
        <div class="empty">No stats available for this sport yet.</div>
      }
    </div>
  `,
  styles: [`
    .sport-stats {
      padding: 1.5rem;
    }
    .header {
      margin-bottom: 1.5rem;
    }
    .header h2 {
      margin: 0;
      color: var(--color-text-primary, #e2e8f0);
    }
    .sport-selector {
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
      margin-bottom: 2rem;
      max-width: 300px;
    }
    .sport-selector label {
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
      text-transform: uppercase;
    }
    .sport-selector select {
      padding: 0.5rem;
      background: var(--color-glass-background, rgba(255,255,255,0.05));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--color-text-primary, #e2e8f0);
      font-size: 0.9rem;
    }
    .loading, .empty {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .stats-section, .records-section, .chart-placeholder {
      margin-bottom: 2rem;
    }
    .stats-section h3, .records-section h3, .chart-placeholder h3 {
      color: var(--color-text-primary, #e2e8f0);
      margin-bottom: 1rem;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 1rem;
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
    .records-list {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .record-card {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 10px;
      padding: 1rem 1.25rem;
      display: flex;
      align-items: center;
      gap: 1.5rem;
    }
    .record-label {
      font-size: 0.85rem;
      color: var(--color-text-secondary, #94a3b8);
      min-width: 100px;
    }
    .record-value {
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--color-accent-primary, #6366f1);
    }
    .record-date {
      margin-left: auto;
      font-size: 0.8rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .placeholder-box {
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px dashed var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 12px;
      padding: 3rem;
      text-align: center;
    }
    .placeholder-box p {
      color: var(--color-text-secondary, #94a3b8);
      margin: 0;
    }
  `],
})
export class SportStatsComponent implements OnInit {
  private readonly deportesService = inject(DeportesService);

  sports = signal<SportResponse[]>([]);
  stats = signal<SportStatsResponse | null>(null);
  personalRecords = signal<PersonalRecordResponse | null>(null);
  loading = signal(false);
  selectedSportId = 0;

  ngOnInit(): void {
    this.deportesService.listSports().subscribe({
      next: (sports) => this.sports.set(sports),
    });
  }

  onSportChange(): void {
    if (this.selectedSportId <= 0) return;
    this.loading.set(true);
    this.stats.set(null);
    this.personalRecords.set(null);

    this.deportesService.getSportStats(this.selectedSportId).subscribe({
      next: (stats) => {
        this.stats.set(stats);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });

    this.deportesService.getPersonalRecords(this.selectedSportId).subscribe({
      next: (prs) => this.personalRecords.set(prs),
    });
  }

  formatDuration(seconds: number): string {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (h > 0) return `${h}h ${m}m`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
  }

  formatPace(secondsPerKm: number): string {
    const m = Math.floor(secondsPerKm / 60);
    const s = secondsPerKm % 60;
    return `${m}:${s.toString().padStart(2, '0')} /km`;
  }
}
