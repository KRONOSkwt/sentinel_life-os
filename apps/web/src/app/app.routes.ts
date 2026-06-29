import { Routes } from '@angular/router';
import { AuthGuard } from './core/auth/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },

  // Public route
  {
    path: 'login',
    loadComponent: () =>
      import('./modules/login/login.component').then((m) => m.LoginComponent),
  },

  // Protected routes — wrapped in BentoLayoutComponent
  {
    path: '',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./layouts/bento-layout/bento-layout.component').then(
        (m) => m.BentoLayoutComponent
      ),
    children: [
      {
        path: 'home',
        loadComponent: () =>
          import('./modules/home/home.component').then((m) => m.HomeComponent),
      },
      {
        path: 'gimnasio',
        loadChildren: () =>
          import('./modules/gimnasio/gimnasio.routes').then((m) => m.routes),
      },
      {
        path: 'deportes',
        loadChildren: () =>
          import('./modules/deportes/deportes.routes').then((m) => m.routes),
      },
      {
        path: 'lesiones',
        loadComponent: () =>
          import('./modules/lesiones/lesiones.component').then(
            (m) => m.LesionesComponent
          ),
      },
      {
        path: 'pastoral',
        loadComponent: () =>
          import('./modules/pastoral/pastoral.component').then(
            (m) => m.PastoralComponent
          ),
      },
      {
        path: 'filosofia',
        loadComponent: () =>
          import('./modules/filosofia/filosofia.component').then(
            (m) => m.FilosofiaComponent
          ),
      },
      {
        path: 'ciberseguridad',
        loadComponent: () =>
          import('./modules/ciberseguridad/ciberseguridad.component').then(
            (m) => m.CiberseguridadComponent
          ),
      },
    ],
  },

  { path: '**', redirectTo: '/home' },
];
