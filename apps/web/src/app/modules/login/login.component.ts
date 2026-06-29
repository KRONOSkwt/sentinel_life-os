import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'sl-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="login-shell">
      <div class="login-card">
        <h1>Sentinel Life OS</h1>

        @if (error()) {
          <div class="error-banner">{{ error() }}</div>
        }

        @if (mode() === 'login') {
          <p>Sign in to continue</p>
          <form (ngSubmit)="onLogin()">
            <input
              type="email"
              placeholder="Email"
              [(ngModel)]="email"
              name="email"
              required
              class="input"
            />
            <input
              type="password"
              placeholder="Password"
              [(ngModel)]="password"
              name="password"
              required
              class="input"
            />
            <button type="submit" class="login-btn" [disabled]="loading()">
              {{ loading() ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>
          <p class="toggle">
            Don't have an account?
            <a (click)="mode.set('register')">Register</a>
          </p>
        } @else {
          <p>Create your account</p>
          <form (ngSubmit)="onRegister()">
            <input
              type="text"
              placeholder="Full name"
              [(ngModel)]="name"
              name="name"
              required
              class="input"
            />
            <input
              type="email"
              placeholder="Email"
              [(ngModel)]="email"
              name="email"
              required
              class="input"
            />
            <input
              type="password"
              placeholder="Password (min 8 chars)"
              [(ngModel)]="password"
              name="password"
              required
              minlength="8"
              class="input"
            />
            <button type="submit" class="login-btn" [disabled]="loading()">
              {{ loading() ? 'Creating account...' : 'Register' }}
            </button>
          </form>
          <p class="toggle">
            Already have an account?
            <a (click)="mode.set('login')">Sign In</a>
          </p>
        }
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
    .input {
      display: block;
      width: 100%;
      padding: 0.65rem 1rem;
      margin-bottom: 0.75rem;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.05);
      color: #e2e8f0;
      font-size: 0.9rem;
      outline: none;
      box-sizing: border-box;
    }
    .input:focus {
      border-color: #6366f1;
    }
    .input::placeholder {
      color: #64748b;
    }
    .login-btn {
      width: 100%;
      padding: 0.65rem;
      border-radius: 999px;
      border: none;
      background: #6366f1;
      color: #fff;
      font-weight: 600;
      cursor: pointer;
      font-size: 0.9rem;
      margin-top: 0.5rem;
    }
    .login-btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .toggle {
      font-size: 0.85rem;
      margin-top: 1rem;
    }
    .toggle a {
      color: #6366f1;
      cursor: pointer;
      text-decoration: underline;
    }
    .error-banner {
      background: rgba(239,68,68,0.15);
      border: 1px solid rgba(239,68,68,0.3);
      color: #fca5a5;
      padding: 0.5rem 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
      font-size: 0.85rem;
    }
  `],
})
export class LoginComponent {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  mode = signal<'login' | 'register'>('login');
  loading = signal(false);
  error = signal('');

  name = '';
  email = '';
  password = '';

  onLogin(): void {
    this.loading.set(true);
    this.error.set('');

    this.http.post<any>('/auth/login', {
      email: this.email,
      password: this.password,
    }).subscribe({
      next: (res) => {
        this.authService.setTokens(res.access_token, res.refresh_token);
        this.loading.set(false);
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err.error?.detail || 'Login failed');
      },
    });
  }

  onRegister(): void {
    this.loading.set(true);
    this.error.set('');

    this.http.post<any>('/auth/register', {
      name: this.name,
      email: this.email,
      password: this.password,
    }).subscribe({
      next: () => {
        // Auto-login after register
        this.http.post<any>('/auth/login', {
          email: this.email,
          password: this.password,
        }).subscribe({
          next: (res) => {
            this.authService.setTokens(res.access_token, res.refresh_token);
            this.loading.set(false);
            this.router.navigate(['/home']);
          },
          error: (err) => {
            this.loading.set(false);
            this.error.set(err.error?.detail || 'Auto-login failed');
          },
        });
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err.error?.detail || 'Registration failed');
      },
    });
  }
}
