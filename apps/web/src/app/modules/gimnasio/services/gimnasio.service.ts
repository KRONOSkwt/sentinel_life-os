import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  ExerciseResponse,
  ExerciseCreate,
  RoutineResponse,
  RoutineDetailResponse,
  RoutineCreate,
  RoutineUpdate,
  SessionResponse,
  SessionCreate,
  SessionComplete,
  SetResponse,
  SetCreate,
  WeightChartResponse,
  AISuggestionResponse,
  GamificationStatsResponse,
  AchievementResponse,
  HeatmapResponse,
} from '@sentinel/shared/models/typescript';

@Injectable({ providedIn: 'root' })
export class GimnasioService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/gimnasio';

  // ---------------------------------------------------------------------------
  // Exercise Catalog
  // ---------------------------------------------------------------------------

  searchExercises(params: {
    category?: string;
    muscle?: string;
    search?: string;
  }): Observable<ExerciseResponse[]> {
    let httpParams = new HttpParams();
    if (params.category) httpParams = httpParams.set('category', params.category);
    if (params.muscle) httpParams = httpParams.set('muscle', params.muscle);
    if (params.search) httpParams = httpParams.set('search', params.search);
    return this.http.get<ExerciseResponse[]>(`${this.baseUrl}/exercises`, {
      params: httpParams,
    });
  }

  createExercise(exercise: ExerciseCreate): Observable<ExerciseResponse> {
    return this.http.post<ExerciseResponse>(`${this.baseUrl}/exercises`, exercise);
  }

  // ---------------------------------------------------------------------------
  // Routines
  // ---------------------------------------------------------------------------

  listRoutines(): Observable<RoutineResponse[]> {
    return this.http.get<RoutineResponse[]>(`${this.baseUrl}/routines`);
  }

  getRoutine(id: number): Observable<RoutineDetailResponse> {
    return this.http.get<RoutineDetailResponse>(`${this.baseUrl}/routines/${id}`);
  }

  createRoutine(routine: RoutineCreate): Observable<RoutineResponse> {
    return this.http.post<RoutineResponse>(`${this.baseUrl}/routines`, routine);
  }

  updateRoutine(id: number, routine: RoutineUpdate): Observable<RoutineResponse> {
    return this.http.put<RoutineResponse>(`${this.baseUrl}/routines/${id}`, routine);
  }

  deleteRoutine(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/routines/${id}`);
  }

  // ---------------------------------------------------------------------------
  // Workout Sessions
  // ---------------------------------------------------------------------------

  startSession(session: SessionCreate): Observable<SessionResponse> {
    return this.http.post<SessionResponse>(`${this.baseUrl}/sessions`, session);
  }

  listSessions(params?: {
    from?: string;
    to?: string;
  }): Observable<SessionResponse[]> {
    let httpParams = new HttpParams();
    if (params?.from) httpParams = httpParams.set('from', params.from);
    if (params?.to) httpParams = httpParams.set('to', params.to);
    return this.http.get<SessionResponse[]>(`${this.baseUrl}/sessions`, {
      params: httpParams,
    });
  }

  getSession(id: number): Observable<SessionResponse> {
    return this.http.get<SessionResponse>(`${this.baseUrl}/sessions/${id}`);
  }

  logSet(sessionId: number, set: SetCreate): Observable<SetResponse> {
    return this.http.put<SetResponse>(
      `${this.baseUrl}/sessions/${sessionId}/sets`,
      set
    );
  }

  completeSession(
    sessionId: number,
    data: SessionComplete
  ): Observable<SessionResponse> {
    return this.http.put<SessionResponse>(
      `${this.baseUrl}/sessions/${sessionId}/complete`,
      data
    );
  }

  // ---------------------------------------------------------------------------
  // Weight Chart
  // ---------------------------------------------------------------------------

  getWeightChart(
    exerciseId: number,
    range: '30' | '90' | '365' | 'all' = '90'
  ): Observable<WeightChartResponse> {
    return this.http.get<WeightChartResponse>(
      `${this.baseUrl}/weight/${exerciseId}`,
      { params: { range } }
    );
  }

  // ---------------------------------------------------------------------------
  // AI Coach
  // ---------------------------------------------------------------------------

  getAISuggestion(exerciseId: number): Observable<AISuggestionResponse> {
    return this.http.get<AISuggestionResponse>(
      `${this.baseUrl}/ai-coach/${exerciseId}`
    );
  }

  // ---------------------------------------------------------------------------
  // Gamification
  // ---------------------------------------------------------------------------

  getGamificationStats(): Observable<GamificationStatsResponse> {
    return this.http.get<GamificationStatsResponse>(
      `${this.baseUrl}/gamification/stats`
    );
  }

  getAchievements(): Observable<AchievementResponse[]> {
    return this.http.get<AchievementResponse[]>(
      `${this.baseUrl}/gamification/achievements`
    );
  }

  // ---------------------------------------------------------------------------
  // Heatmap
  // ---------------------------------------------------------------------------

  getHeatmap(year: number): Observable<HeatmapResponse> {
    return this.http.get<HeatmapResponse>(`${this.baseUrl}/heatmap`, {
      params: { year: year.toString() },
    });
  }
}
