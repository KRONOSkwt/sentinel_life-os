import { Component } from '@angular/core';

@Component({
  selector: 'sl-login',
  standalone: true,
  template: `
    <div class="login-shell">
      <div class="login-card">
        <h1>Sentinel Life OS</h1>
        <p>Sign in to continue</p>
        <!-- TODO: wire up real auth form -->
        <button class="login-btn">Login</button>
      </div>
    </div>
  `,
  styles: [`
    .login-shell {
      display: grid;
      place-items: center;
      min-height: 100dvh;
      background: #0f0f23;
    }
    .login-card {
      background: #1a1a2e;
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 16px;
      padding: 2.5rem;
      text-align: center;
      color: #e2e8f0;
      min-width: 320px;
    }
    h1 { font-size: 1.5rem; color: #6366f1; margin: 0 0 0.5rem; }
    p { color: #94a3b8; margin: 0 0 1.5rem; }
    .login-btn {
      padding: 0.65rem 2rem;
      border-radius: 999px;
      border: none;
      background: #6366f1;
      color: #fff;
      font-weight: 600;
      cursor: pointer;
    }
  `],
})
export class LoginComponent {}
