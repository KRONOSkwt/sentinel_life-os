import { Injectable } from '@angular/core';

const TOKEN_KEY = 'sentinel_access_token';
const REFRESH_KEY = 'sentinel_refresh_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  // ------------------------------------------------------------------
  // Token persistence (localStorage — offline-first per design)
  // ------------------------------------------------------------------

  getAccessToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  }

  setTokens(access: string, refresh: string): void {
    localStorage.setItem(TOKEN_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
  }

  clearTokens(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
  }

  isAuthenticated(): boolean {
    const token = this.getAccessToken();
    if (!token) return false;

    // Check expiry via JWT exp claim (base64url)
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }
}
