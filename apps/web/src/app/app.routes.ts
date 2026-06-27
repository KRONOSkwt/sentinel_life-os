import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  {
    path: 'home',
    loadComponent: () =>
      import('./modules/home/home.component').then((m) => m.HomeComponent),
  },
  {
    path: 'gimnasio',
    loadComponent: () =>
      import('./modules/gimnasio/gimnasio.component').then(
        (m) => m.GimnasioComponent
      ),
  },
  {
    path: 'deportes',
    loadComponent: () =>
      import('./modules/deportes/deportes.component').then(
        (m) => m.DeportesComponent
      ),
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
  { path: '**', redirectTo: '/home' },
];
