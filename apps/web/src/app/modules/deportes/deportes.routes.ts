import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./deportes.component').then((m) => m.DeportesComponent),
  },
  {
    path: 'activities',
    loadComponent: () =>
      import('./components/activity-list/activity-list.component').then(
        (m) => m.ActivityListComponent
      ),
  },
  {
    path: 'activities/:id',
    loadComponent: () =>
      import('./components/activity-detail/activity-detail.component').then(
        (m) => m.ActivityDetailComponent
      ),
  },
  {
    path: 'plans',
    loadComponent: () =>
      import('./components/training-plan-list/training-plan-list.component').then(
        (m) => m.TrainingPlanListComponent
      ),
  },
  {
    path: 'calendar',
    loadComponent: () =>
      import('./components/race-calendar/race-calendar.component').then(
        (m) => m.RaceCalendarComponent
      ),
  },
  {
    path: 'records',
    loadComponent: () =>
      import('./components/sport-stats/sport-stats.component').then(
        (m) => m.SportStatsComponent
      ),
  },
];
