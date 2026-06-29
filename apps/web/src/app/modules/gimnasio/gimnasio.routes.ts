import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./gimnasio.component').then((m) => m.GimnasioComponent),
  },
  {
    path: 'routines',
    loadComponent: () =>
      import('./components/routine-list/routine-list.component').then(
        (m) => m.RoutineListComponent
      ),
  },
  {
    path: 'routines/:id',
    loadComponent: () =>
      import('./components/routine-detail/routine-detail.component').then(
        (m) => m.RoutineDetailComponent
      ),
  },
  {
    path: 'exercises',
    loadComponent: () =>
      import('./components/exercise-catalog/exercise-catalog.component').then(
        (m) => m.ExerciseCatalogComponent
      ),
  },
  {
    path: 'session/:id',
    loadComponent: () =>
      import('./components/workout-session/workout-session.component').then(
        (m) => m.WorkoutSessionComponent
      ),
  },
  {
    path: 'heatmap',
    loadComponent: () =>
      import('./components/heatmap-calendar/heatmap-calendar.component').then(
        (m) => m.HeatmapCalendarComponent
      ),
  },
  {
    path: 'gamification',
    loadComponent: () =>
      import(
        './components/gamification-dashboard/gamification-dashboard.component'
      ).then((m) => m.GamificationDashboardComponent),
  },
];
