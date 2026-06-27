import { Component } from '@angular/core';

@Component({
  selector: 'sl-home',
  standalone: true,
  template: `
    <div class="home">
      <h1>Sentinel Life OS</h1>
      <p>Welcome to your Life OS dashboard.</p>
    </div>
  `,
  styles: [`
    .home {
      padding: 2rem;
      text-align: center;
    }
    h1 {
      font-size: 2rem;
      color: #1a1a2e;
    }
  `],
})
export class HomeComponent {}
