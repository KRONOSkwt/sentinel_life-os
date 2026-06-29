import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GimnasioService } from '../../services/gimnasio.service';
import { HeatmapDay } from '@sentinel/shared/models/typescript';

interface HeatmapWeek {
  days: (HeatmapDay | null)[];
}

@Component({
  selector: 'sl-heatmap-calendar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="heatmap-calendar">
      <div class="header">
        <h2>Workout Heatmap</h2>
        <div class="year-selector">
          <button
            class="btn-year"
            [class.active]="selectedYear() === currentYear - 1"
            (click)="selectYear(currentYear - 1)"
          >
            {{ currentYear - 1 }}
          </button>
          <button
            class="btn-year"
            [class.active]="selectedYear() === currentYear"
            (click)="selectYear(currentYear)"
          >
            {{ currentYear }}
          </button>
        </div>
      </div>

      @if (loading()) {
        <div class="loading">Loading heatmap...</div>
      } @else {
        <div class="heatmap-container">
          <div class="month-labels">
            @for (month of monthLabels; track month) {
              <span class="month-label">{{ month }}</span>
            }
          </div>
          <div class="heatmap-grid">
            <div class="day-labels">
              <span class="day-label">Mon</span>
              <span class="day-label">Wed</span>
              <span class="day-label">Fri</span>
            </div>
            <div class="grid">
              @for (week of weeks(); track $index) {
                <div class="week">
                  @for (day of week.days; track $index) {
                    @if (day) {
                      <div
                        class="day"
                        [class]="'intensity-' + day.intensity"
                        [title]="getTooltip(day)"
                        (mouseenter)="showTooltip(day, $event)"
                        (mouseleave)="hideTooltip()"
                      ></div>
                    } @else {
                      <div class="day empty"></div>
                    }
                  }
                </div>
              }
            </div>
          </div>
          <div class="legend">
            <span class="legend-label">Less</span>
            <div class="legend-scale">
              <div class="legend-cell intensity-0"></div>
              <div class="legend-cell intensity-1"></div>
              <div class="legend-cell intensity-2"></div>
              <div class="legend-cell intensity-3"></div>
            </div>
            <span class="legend-label">More</span>
          </div>
        </div>

        @if (tooltipVisible()) {
          <div
            class="tooltip"
            [style.left]="tooltipPosition().x + 'px'"
            [style.top]="tooltipPosition().y + 'px'"
          >
            <strong>{{ tooltipDay()!.date }}</strong>
            <span>{{ tooltipDay()!.workout_count }} workout(s)</span>
          </div>
        }
      }
    </div>
  `,
  styles: [`
    .heatmap-calendar {
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
    .year-selector {
      display: flex;
      gap: 0.5rem;
    }
    .btn-year {
      padding: 0.4rem 0.8rem;
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--color-text-secondary, #94a3b8);
      cursor: pointer;
      font-size: 0.85rem;
    }
    .btn-year:hover {
      background: var(--color-glass-border, rgba(255,255,255,0.2));
    }
    .btn-year.active {
      background: var(--color-accent-primary, #6366f1);
      color: white;
      border-color: var(--color-accent-primary, #6366f1);
    }
    .loading {
      text-align: center;
      padding: 2rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .heatmap-container {
      overflow-x: auto;
    }
    .month-labels {
      display: flex;
      margin-left: 40px;
      margin-bottom: 0.5rem;
    }
    .month-label {
      width: 46px;
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .heatmap-grid {
      display: flex;
    }
    .day-labels {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding-right: 8px;
      height: 98px;
    }
    .day-label {
      font-size: 0.7rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .grid {
      display: flex;
      gap: 3px;
    }
    .week {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .day {
      width: 13px;
      height: 13px;
      border-radius: 2px;
      cursor: pointer;
      transition: transform 0.1s;
    }
    .day:hover {
      transform: scale(1.3);
    }
    .day.empty {
      background: transparent;
      cursor: default;
    }
    .day.empty:hover {
      transform: none;
    }
    .intensity-0 {
      background: #161b22;
    }
    .intensity-1 {
      background: #0e4429;
    }
    .intensity-2 {
      background: #006d32;
    }
    .intensity-3 {
      background: #26a641;
    }
    .legend {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 0.5rem;
      margin-top: 1rem;
    }
    .legend-label {
      font-size: 0.75rem;
      color: var(--color-text-secondary, #94a3b8);
    }
    .legend-scale {
      display: flex;
      gap: 3px;
    }
    .legend-cell {
      width: 13px;
      height: 13px;
      border-radius: 2px;
    }
    .tooltip {
      position: fixed;
      background: var(--color-glass-card-background, rgba(255,255,255,0.95));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      border-radius: 6px;
      padding: 0.5rem 0.75rem;
      font-size: 0.8rem;
      z-index: 1000;
      pointer-events: none;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .tooltip strong {
      display: block;
      color: var(--color-text-primary, #e2e8f0);
    }
    .tooltip span {
      color: var(--color-text-secondary, #94a3b8);
    }
  `],
})
export class HeatmapCalendarComponent implements OnInit {
  private readonly gimnasioService = inject(GimnasioService);

  days = signal<HeatmapDay[]>([]);
  loading = signal(true);
  selectedYear = signal(new Date().getFullYear());
  currentYear = new Date().getFullYear();

  tooltipVisible = signal(false);
  tooltipDay = signal<HeatmapDay | null>(null);
  tooltipPosition = signal({ x: 0, y: 0 });

  readonly monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  weeks = computed(() => {
    const allDays = this.days();
    const year = this.selectedYear();
    const weeks: HeatmapWeek[] = [];

    // Create a map of date -> HeatmapDay
    const dayMap = new Map<string, HeatmapDay>();
    allDays.forEach(d => dayMap.set(d.date, d));

    // Generate all days in the year
    const startDate = new Date(year, 0, 1);
    const endDate = new Date(year, 11, 31);

    let currentWeek: (HeatmapDay | null)[] = [];

    // Pad the first week with nulls for days before Jan 1
    const firstDayOfWeek = startDate.getDay(); // 0 = Sunday, 1 = Monday, ...
    const mondayOffset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
    for (let i = 0; i < mondayOffset; i++) {
      currentWeek.push(null);
    }

    const current = new Date(startDate);
    while (current <= endDate) {
      const dateStr = current.toISOString().split('T')[0];
      const dayData = dayMap.get(dateStr) || {
        date: dateStr,
        intensity: 0,
        workout_count: 0,
      };

      currentWeek.push(dayData);

      // If it's Sunday (end of week), start a new week
      if (current.getDay() === 0) {
        weeks.push({ days: currentWeek });
        currentWeek = [];
      }

      current.setDate(current.getDate() + 1);
    }

    // Add the last partial week
    if (currentWeek.length > 0) {
      weeks.push({ days: currentWeek });
    }

    return weeks;
  });

  ngOnInit(): void {
    this.loadHeatmap();
  }

  loadHeatmap(): void {
    this.loading.set(true);
    this.gimnasioService.getHeatmap(this.selectedYear()).subscribe({
      next: (response) => {
        this.days.set(response.days);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      },
    });
  }

  selectYear(year: number): void {
    this.selectedYear.set(year);
    this.loadHeatmap();
  }

  getTooltip(day: HeatmapDay): string {
    return `${day.date}: ${day.workout_count} workout(s)`;
  }

  showTooltip(day: HeatmapDay, event: MouseEvent): void {
    this.tooltipDay.set(day);
    this.tooltipPosition.set({ x: event.clientX + 10, y: event.clientY - 30 });
    this.tooltipVisible.set(true);
  }

  hideTooltip(): void {
    this.tooltipVisible.set(false);
  }
}
