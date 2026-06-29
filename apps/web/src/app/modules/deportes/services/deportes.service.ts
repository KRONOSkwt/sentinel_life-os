import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  SportCreate,
  SportResponse,
  SportActivityCreate,
  SportActivityUpdate,
  SportActivityResponse,
  SportStatsResponse,
  PersonalRecordResponse,
  TrainingPlanCreate,
  TrainingPlanUpdate,
  TrainingPlanResponse,
  RaceEventCreate,
  RaceEventUpdate,
  RaceEventResponse,
} from '@sentinel/shared/models/typescript';

@Injectable({ providedIn: 'root' })
export class DeportesService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/deportes';

  // ---------------------------------------------------------------------------
  // Sports
  // ---------------------------------------------------------------------------

  listSports(): Observable<SportResponse[]> {
    return this.http.get<SportResponse[]>(`${this.baseUrl}/sports`);
  }

  createSport(sport: SportCreate): Observable<SportResponse> {
    return this.http.post<SportResponse>(`${this.baseUrl}/sports`, sport);
  }

  // ---------------------------------------------------------------------------
  // Activities
  // ---------------------------------------------------------------------------

  logActivity(activity: SportActivityCreate): Observable<SportActivityResponse> {
    return this.http.post<SportActivityResponse>(`${this.baseUrl}/activities`, activity);
  }

  listActivities(params?: {
    from?: string;
    to?: string;
  }): Observable<SportActivityResponse[]> {
    let httpParams = new HttpParams();
    if (params?.from) httpParams = httpParams.set('from', params.from);
    if (params?.to) httpParams = httpParams.set('to', params.to);
    return this.http.get<SportActivityResponse[]>(`${this.baseUrl}/activities`, {
      params: httpParams,
    });
  }

  getActivity(id: number): Observable<SportActivityResponse> {
    return this.http.get<SportActivityResponse>(`${this.baseUrl}/activities/${id}`);
  }

  updateActivity(id: number, activity: SportActivityUpdate): Observable<SportActivityResponse> {
    return this.http.put<SportActivityResponse>(`${this.baseUrl}/activities/${id}`, activity);
  }

  deleteActivity(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/activities/${id}`);
  }

  // ---------------------------------------------------------------------------
  // Stats & Personal Records
  // ---------------------------------------------------------------------------

  getSportStats(sportId: number): Observable<SportStatsResponse> {
    return this.http.get<SportStatsResponse>(`${this.baseUrl}/stats/${sportId}`);
  }

  getPersonalRecords(sportId: number): Observable<PersonalRecordResponse> {
    return this.http.get<PersonalRecordResponse>(`${this.baseUrl}/prs/${sportId}`);
  }

  // ---------------------------------------------------------------------------
  // Training Plans
  // ---------------------------------------------------------------------------

  listPlans(): Observable<TrainingPlanResponse[]> {
    return this.http.get<TrainingPlanResponse[]>(`${this.baseUrl}/plans`);
  }

  createPlan(plan: TrainingPlanCreate): Observable<TrainingPlanResponse> {
    return this.http.post<TrainingPlanResponse>(`${this.baseUrl}/plans`, plan);
  }

  getPlan(id: number): Observable<TrainingPlanResponse> {
    return this.http.get<TrainingPlanResponse>(`${this.baseUrl}/plans/${id}`);
  }

  updatePlan(id: number, plan: TrainingPlanUpdate): Observable<TrainingPlanResponse> {
    return this.http.put<TrainingPlanResponse>(`${this.baseUrl}/plans/${id}`, plan);
  }

  deletePlan(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/plans/${id}`);
  }

  // ---------------------------------------------------------------------------
  // Race Calendar
  // ---------------------------------------------------------------------------

  listRaces(): Observable<RaceEventResponse[]> {
    return this.http.get<RaceEventResponse[]>(`${this.baseUrl}/races`);
  }

  createRace(race: RaceEventCreate): Observable<RaceEventResponse> {
    return this.http.post<RaceEventResponse>(`${this.baseUrl}/races`, race);
  }

  updateRace(id: number, race: RaceEventUpdate): Observable<RaceEventResponse> {
    return this.http.put<RaceEventResponse>(`${this.baseUrl}/races/${id}`, race);
  }

  deleteRace(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/races/${id}`);
  }
}
