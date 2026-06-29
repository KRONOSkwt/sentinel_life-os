import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'sl-deportes',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],
  template: `
    <div class="deportes-shell">
      <nav class="tab-nav">
        <a routerLink="/deportes/activities" routerLinkActive="active" class="tab">
          Activities
        </a>
        <a routerLink="/deportes/plans" routerLinkActive="active" class="tab">
          Plans
        </a>
        <a routerLink="/deportes/calendar" routerLinkActive="active" class="tab">
          Calendar
        </a>
        <a routerLink="/deportes/records" routerLinkActive="active" class="tab">
          Records
        </a>
      </nav>
      <main class="tab-content">
        <router-outlet />
      </main>
    </div>
  `,
  styles: [`
    .deportes-shell {
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    .tab-nav {
      display: flex;
      gap: 0.5rem;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      background: var(--color-glass-background, rgba(255,255,255,0.05));
      overflow-x: auto;
    }
    .tab {
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 500;
      text-decoration: none;
      color: var(--color-text-secondary, #94a3b8);
      white-space: nowrap;
      transition: all 0.2s;
    }
    .tab:hover {
      color: var(--color-text-primary, #e2e8f0);
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
    }
    .tab.active {
      color: var(--color-accent-primary, #6366f1);
      background: var(--color-accent-primary, rgba(99, 102, 241, 0.1));
    }
    .tab-content {
      flex: 1;
      overflow: auto;
    }
  `],
})
export class DeportesComponent {}
