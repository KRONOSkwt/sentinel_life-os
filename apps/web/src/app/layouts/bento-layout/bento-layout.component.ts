import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'sl-bento-layout',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <div class="bento-shell">
      <header class="bento-header">
        <h1 class="brand">Sentinel Life OS</h1>
        <nav class="bento-nav">
          <a routerLink="/home" class="nav-pill">Home</a>
          <a routerLink="/gimnasio" class="nav-pill">Gimnasio</a>
          <a routerLink="/deportes" class="nav-pill">Deportes</a>
          <a routerLink="/lesiones" class="nav-pill">Lesiones</a>
          <a routerLink="/pastoral" class="nav-pill">Pastoral</a>
          <a routerLink="/filosofia" class="nav-pill">Filosofia</a>
          <a routerLink="/ciberseguridad" class="nav-pill">Ciberseguridad</a>
        </nav>
      </header>
      <main class="bento-grid">
        <router-outlet />
      </main>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100dvh; }

    .bento-shell {
      display: flex;
      flex-direction: column;
      min-height: 100dvh;
      background: var(--color-surface-background, #0f0f23);
      color: var(--color-text-primary, #e2e8f0);
    }

    /* ---- Header ---- */
    .bento-header {
      display: flex;
      align-items: center;
      gap: 1.5rem;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      background: var(--color-glass-background, rgba(255,255,255,0.08));
      backdrop-filter: blur(12px);
    }

    .brand {
      font-size: 1.15rem;
      font-weight: 700;
      margin: 0;
      color: var(--color-accent-primary, #6366f1);
    }

    .bento-nav {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .nav-pill {
      padding: 0.35rem 0.85rem;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 500;
      text-decoration: none;
      color: var(--color-text-secondary, #94a3b8);
      background: var(--color-glass-card-background, rgba(255,255,255,0.1));
      border: 1px solid var(--color-glass-border, rgba(255,255,255,0.15));
      transition: all 0.2s;
    }
    .nav-pill:hover {
      color: var(--color-text-primary, #e2e8f0);
      background: var(--color-glass-border, rgba(255,255,255,0.2));
    }

    /* ---- Grid ---- */
    .bento-grid {
      flex: 1;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
      padding: 1.5rem;
    }

    /* Responsive collapse */
    @media (max-width: 720px) {
      .bento-header { flex-direction: column; align-items: flex-start; }
      .bento-grid { grid-template-columns: 1fr; }
    }
  `],
})
export class BentoLayoutComponent {}
