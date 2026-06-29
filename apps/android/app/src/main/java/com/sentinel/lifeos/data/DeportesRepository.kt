package com.sentinel.lifeos.data

import com.sentinel.shared.models.*
import java.time.Instant

/**
 * Repository for the Deportes (Sports) module.
 * Abstracts data access — currently returns mock data.
 * Swap the implementation for a Retrofit/Ktor-backed one when the network layer is ready.
 */
interface DeportesRepository {
    // Sports
    suspend fun listSports(customOnly: Boolean = false): List<SportResponse>
    suspend fun createSport(sport: SportCreate): SportResponse

    // Activities
    suspend fun listActivities(
        fromDate: String? = null,
        toDate: String? = null,
        limit: Int = 50,
        offset: Int = 0,
    ): List<SportActivityResponse>
    suspend fun getActivity(activityId: Int): SportActivityResponse
    suspend fun logActivity(activity: SportActivityCreate): SportActivityResponse
    suspend fun updateActivity(activityId: Int, update: SportActivityUpdate): SportActivityResponse
    suspend fun deleteActivity(activityId: Int)

    // Stats & PRs
    suspend fun getSportStats(sportId: Int): SportStatsResponse
    suspend fun getPersonalRecords(sportId: Int): PersonalRecordResponse

    // Training Plans
    suspend fun listPlans(): List<TrainingPlanResponse>
    suspend fun getPlan(planId: Int): TrainingPlanDetailResponse
    suspend fun createPlan(plan: TrainingPlanCreate): TrainingPlanDetailResponse
    suspend fun updatePlan(planId: Int, update: TrainingPlanUpdate): TrainingPlanDetailResponse
    suspend fun deletePlan(planId: Int)

    // Race Events
    suspend fun listRaces(
        upcomingOnly: Boolean = false,
        limit: Int = 50,
        offset: Int = 0,
    ): List<RaceEventResponse>
    suspend fun createRace(race: RaceEventCreate): RaceEventResponse
    suspend fun updateRace(raceId: Int, update: RaceEventUpdate): RaceEventResponse
    suspend fun deleteRace(raceId: Int)
}

/**
 * Mock implementation using hardcoded data.
 * Follows GimnasioScreen pattern — mock data until network layer is wired.
 */
class MockDeportesRepository : DeportesRepository {

    private val sports = mutableListOf(
        SportResponse(1, "Running", "\uD83C\uDFC3", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(2, "Cycling", "\uD83D\uDEB4", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(3, "Swimming", "\uD83C\uDFCA", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(4, "Basketball", "\uD83C\uDFC0", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(5, "Soccer", "\u26BD", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(6, "Tennis", "\uD83C\uDFBE", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(7, "Yoga", "\uD83E\uDDD8", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(8, "Hiking", "\uD83E\uDD7E", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(9, "Boxing", "\uD83E\uDD4A", false, Instant.parse("2026-01-01T00:00:00Z")),
        SportResponse(10, "Rowing", "\uD83C\uDFC3", false, Instant.parse("2026-01-01T00:00:00Z")),
    )

    private val activities = mutableListOf(
        SportActivityResponse(1, 1, 1, Instant.parse("2026-06-28T07:00:00Z"), 2700, 8.5, 420, 145, null, "Morning run", Instant.parse("2026-06-28T07:45:00Z")),
        SportActivityResponse(2, 1, 2, Instant.parse("2026-06-27T17:30:00Z"), 5400, 35.0, 890, 132, null, "Evening ride", Instant.parse("2026-06-27T19:00:00Z")),
        SportActivityResponse(3, 1, 3, Instant.parse("2026-06-26T06:30:00Z"), 3600, 2.0, 310, 128, null, "Pool laps", Instant.parse("2026-06-26T07:30:00Z")),
        SportActivityResponse(4, 1, 1, Instant.parse("2026-06-25T06:00:00Z"), 1800, 5.0, 250, 150, null, "Tempo run", Instant.parse("2026-06-25T06:30:00Z")),
        SportActivityResponse(5, 1, 7, Instant.parse("2026-06-24T18:00:00Z"), 3600, null, 180, 95, null, "Vinyasa flow", Instant.parse("2026-06-24T19:00:00Z")),
    )

    private val plans = mutableListOf(
        TrainingPlanResponse(1, "Marathon Prep", "16-week marathon training", Instant.parse("2026-07-01T00:00:00Z"), Instant.parse("2026-10-15T00:00:00Z"), Instant.parse("2026-06-25T00:00:00Z"), Instant.parse("2026-06-25T00:00:00Z")),
        TrainingPlanResponse(2, "Base Building", "8-week aerobic base", Instant.parse("2026-06-01T00:00:00Z"), Instant.parse("2026-07-27T00:00:00Z"), Instant.parse("2026-05-30T00:00:00Z"), Instant.parse("2026-05-30T00:00:00Z")),
    )

    private val races = mutableListOf(
        RaceEventResponse(1, 1, "City Marathon", 1, Instant.parse("2026-10-12T07:00:00Z"), 42.195, "Buenos Aires", 18000, "Target sub-5h", Instant.parse("2026-06-01T00:00:00Z")),
        RaceEventResponse(2, 1, "10K Park Run", 1, Instant.parse("2026-07-15T08:00:00Z"), 10.0, "Palermo", 5400, null, Instant.parse("2026-06-10T00:00:00Z")),
        RaceEventResponse(3, 2, "Gran Fondo", 2, Instant.parse("2026-08-20T07:30:00Z"), 120.0, "Sierra de la Ventana", null, "First century", Instant.parse("2026-06-15T00:00:00Z")),
    )

    private var nextId = 100

    // Sports
    override suspend fun listSports(customOnly: Boolean): List<SportResponse> =
        if (customOnly) sports.filter { it.is_custom } else sports.toList()

    override suspend fun createSport(sport: SportCreate): SportResponse {
        val new = SportResponse(nextId++, sport.name, sport.icon, true, Instant.now())
        sports.add(new)
        return new
    }

    // Activities
    override suspend fun listActivities(
        fromDate: String?, toDate: String?, limit: Int, offset: Int,
    ): List<SportActivityResponse> {
        var filtered = activities.sortedByDescending { it.date }
        fromDate?.let { from ->
            val fromDateInst = Instant.parse(from)
            filtered = filtered.filter { !it.date.isBefore(fromDateInst) }
        }
        toDate?.let { to ->
            val toDateInst = Instant.parse(to)
            filtered = filtered.filter { !it.date.isAfter(toDateInst) }
        }
        return filtered.drop(offset).take(limit)
    }

    override suspend fun getActivity(activityId: Int): SportActivityResponse =
        activities.first { it.id == activityId }

    override suspend fun logActivity(activity: SportActivityCreate): SportActivityResponse {
        val new = SportActivityResponse(
            id = nextId++,
            user_id = 1,
            sport_id = activity.sport_id,
            date = activity.date,
            duration_seconds = activity.duration_seconds,
            distance_km = activity.distance_km,
            calories = activity.calories,
            heart_rate_avg = activity.heart_rate_avg,
            extra_data = activity.extra_data,
            notes = activity.notes,
            created_at = Instant.now(),
        )
        activities.add(new)
        return new
    }

    override suspend fun updateActivity(activityId: Int, update: SportActivityUpdate): SportActivityResponse {
        val idx = activities.indexOfFirst { it.id == activityId }
        val existing = activities[idx]
        val updated = existing.copy(
            date = update.date ?: existing.date,
            duration_seconds = update.duration_seconds ?: existing.duration_seconds,
            distance_km = update.distance_km ?: existing.distance_km,
            calories = update.calories ?: existing.calories,
            heart_rate_avg = update.heart_rate_avg ?: existing.heart_rate_avg,
            extra_data = update.extra_data ?: existing.extra_data,
            notes = update.notes ?: existing.notes,
        )
        activities[idx] = updated
        return updated
    }

    override suspend fun deleteActivity(activityId: Int) {
        activities.removeAll { it.id == activityId }
    }

    // Stats & PRs
    override suspend fun getSportStats(sportId: Int): SportStatsResponse {
        val sportActivities = activities.filter { it.sport_id == sportId }
        val total = sportActivities.size
        val totalTime = sportActivities.sumOf { it.duration_seconds }
        val totalDist = sportActivities.mapNotNull { it.distance_km }.takeIf { it.isNotEmpty() }?.sum()
        val avgDuration = if (total > 0) totalTime.toDouble() / total else null
        val sportName = sports.firstOrNull { it.id == sportId }?.name ?: "Unknown"
        return SportStatsResponse(sportId, sportName, total, totalTime, totalDist, avgDuration)
    }

    override suspend fun getPersonalRecords(sportId: Int): PersonalRecordResponse {
        val sportActivities = activities.filter { it.sport_id == sportId }
        val bestTime = sportActivities.minByOrNull { it.duration_seconds }
        val bestDist = sportActivities.maxByOrNull { it.distance_km ?: 0.0 }
        return PersonalRecordResponse(
            sport_id = sportId,
            best_time_seconds = bestTime?.duration_seconds,
            best_distance_km = bestDist?.distance_km,
            best_pace_seconds_per_km = null,
            best_time_date = bestTime?.date,
            best_distance_date = bestDist?.date,
        )
    }

    // Training Plans
    override suspend fun listPlans(): List<TrainingPlanResponse> = plans.toList()

    override suspend fun getPlan(planId: Int): TrainingPlanDetailResponse {
        val plan = plans.first { it.id == planId }
        return TrainingPlanDetailResponse(
            id = plan.id,
            name = plan.name,
            description = plan.description,
            start_date = plan.start_date,
            end_date = plan.end_date,
            created_at = plan.created_at,
            updated_at = plan.updated_at,
        )
    }

    override suspend fun createPlan(plan: TrainingPlanCreate): TrainingPlanDetailResponse {
        val newPlan = TrainingPlanResponse(
            id = nextId++,
            name = plan.name,
            description = plan.description,
            start_date = plan.start_date,
            end_date = plan.end_date,
            created_at = Instant.now(),
            updated_at = Instant.now(),
        )
        plans.add(newPlan)
        return TrainingPlanDetailResponse(
            id = newPlan.id,
            name = newPlan.name,
            description = newPlan.description,
            start_date = newPlan.start_date,
            end_date = newPlan.end_date,
            created_at = newPlan.created_at,
            updated_at = newPlan.updated_at,
        )
    }

    override suspend fun updatePlan(planId: Int, update: TrainingPlanUpdate): TrainingPlanDetailResponse {
        val idx = plans.indexOfFirst { it.id == planId }
        val existing = plans[idx]
        val updated = existing.copy(
            name = update.name ?: existing.name,
            description = update.description ?: existing.description,
            start_date = update.start_date ?: existing.start_date,
            end_date = update.end_date ?: existing.end_date,
            updated_at = Instant.now(),
        )
        plans[idx] = updated
        return getPlan(planId)
    }

    override suspend fun deletePlan(planId: Int) {
        plans.removeAll { it.id == planId }
    }

    // Race Events
    override suspend fun listRaces(
        upcomingOnly: Boolean, limit: Int, offset: Int,
    ): List<RaceEventResponse> {
        var filtered = races.sortedBy { it.event_date }
        if (upcomingOnly) {
            filtered = filtered.filter { !it.event_date.isBefore(Instant.now()) }
        }
        return filtered.drop(offset).take(limit)
    }

    override suspend fun createRace(race: RaceEventCreate): RaceEventResponse {
        val new = RaceEventResponse(
            id = nextId++,
            user_id = 1,
            name = race.name,
            sport_id = race.sport_id,
            event_date = race.event_date,
            distance_km = race.distance_km,
            location = race.location,
            target_time_seconds = race.target_time_seconds,
            notes = race.notes,
            created_at = Instant.now(),
        )
        races.add(new)
        return new
    }

    override suspend fun updateRace(raceId: Int, update: RaceEventUpdate): RaceEventResponse {
        val idx = races.indexOfFirst { it.id == raceId }
        val existing = races[idx]
        val updated = existing.copy(
            name = update.name ?: existing.name,
            sport_id = update.sport_id ?: existing.sport_id,
            event_date = update.event_date ?: existing.event_date,
            distance_km = update.distance_km ?: existing.distance_km,
            location = update.location ?: existing.location,
            target_time_seconds = update.target_time_seconds ?: existing.target_time_seconds,
            notes = update.notes ?: existing.notes,
        )
        races[idx] = updated
        return updated
    }

    override suspend fun deleteRace(raceId: Int) {
        races.removeAll { it.id == raceId }
    }
}
