# Semantic Model and Relationship Design

The screenshots under `assets/powerbi_screenshots/` were captured from the Power BI Desktop work session and show the relationship setup using the source-table names. The query files in `powerbi/power_query/` organize the preparation into staging queries, dimensions and fact tables so that the steps are easier to follow and reuse. The model definition below describes that organized version of the data model.

## Modeling principles

1. Keep event-grain facts separate from season-grain standings.
2. Use single-direction relationships from dimensions to facts (and from descriptive dimensions into `Dim_Races` where noted).
3. Do not assume `(raceId, driverId)` is unique in every source fact; generate a row ID for traceability instead of silently dropping records.
4. The `Dim_Races` table contains one row per scheduled event and acts as the bridge for date, Grand Prix identity and physical circuit.
5. Season standings use an independent `Dim_Season` so the season-level fact grain is not merged into every event result.

## Tables and grains

| Table | Grain | Key / relationship role |
|---|---|---|
| `Dim_Date` | One calendar date | `Date`; contiguous calendar for time intelligence |
| `Dim_Races` | One scheduled race event | `RaceId` from `races.id`; has `Year`, `Round`, `RaceDate`, `CircuitId`, `GrandPrixId` |
| `Dim_Drivers` | One source driver entity | `DriverId` (renamed from source `id`); descriptive attributes and joined nationality label |
| `Dim_Constructors` | One source constructor entity | `ConstructorId` (renamed from source `id`); descriptive attributes and joined country label |
| `Dim_Circuits` | One physical circuit | `CircuitId` (renamed from source `id`); joined host country and continent, latitude/longitude, type |
| `Dim_GrandPrix` | One named Grand Prix identity | `GrandPrixId` (renamed from source `id`); name and readable country label |
| `Dim_Season` | One season year | `Year`; used only with season-level standings facts |
| `Fact_RaceResults` | One source result record | Generated `ResultRowId`; foreign keys `raceId`, `driverId`, `constructorId`; includes outcome, grid, points and flags |
| `Fact_Qualifying` | One source qualifying record | Generated `QualifyingRowId`; `raceId`, `driverId`, `constructorId` |
| `Fact_FastestLaps` | One fastest-lap classification record | Generated `FastestLapRowId`; `raceId`, `driverId`, `constructorId` |
| `Fact_PitStops` | One recorded pit stop | Generated `PitStopRowId`; `raceId`, `driverId`, `constructorId` |
| `Fact_SeasonDriverStandings` | One source driver-season row | Generated row ID; `year`, `driverId`; preserve candidate-key exceptions |
| `Fact_SeasonConstructorStandings` | One source constructor-season row | Generated row ID; `year`, `constructorId`; preserve candidate-key exceptions |
| `QA_SourceProvidedTotals_Drivers` | One driver source summary row | QA only; do not connect to report facts |
| `QA_SourceProvidedTotals_Constructors` | One constructor source summary row | QA only; do not connect to report facts |

## Relationships

| One-side | Many-side | Active | Direction |
|---|---|---|---|
| `Dim_Date[Date]` | `Dim_Races[RaceDate]` | Yes | Single |
| `Dim_Circuits[CircuitId]` | `Dim_Races[CircuitId]` | Yes | Single |
| `Dim_GrandPrix[GrandPrixId]` | `Dim_Races[GrandPrixId]` | Yes | Single |
| `Dim_Races[RaceId]` | `Fact_RaceResults[raceId]` | Yes | Single |
| `Dim_Races[RaceId]` | `Fact_Qualifying[raceId]` | Yes | Single |
| `Dim_Races[RaceId]` | `Fact_FastestLaps[raceId]` | Yes | Single |
| `Dim_Races[RaceId]` | `Fact_PitStops[raceId]` | Yes | Single |
| `Dim_Drivers[DriverId]` | each driver-bearing event/season fact | Yes | Single |
| `Dim_Constructors[ConstructorId]` | each constructor-bearing event/season fact | Yes | Single |
| `Dim_Season[Year]` | `Fact_SeasonDriverStandings[year]` | Yes | Single |
| `Dim_Season[Year]` | `Fact_SeasonConstructorStandings[year]` | Yes | Single |

Do **not** connect `Dim_Season` to `Dim_Races` in this design. Use `Dim_Date[Year]` / `Dim_Races[Year]` for race-grain reports, and `Dim_Season[Year]` for standings visuals. Keep the filter paths explicit and do not add bidirectional relationships just to make a particular visual respond.

## Modeling issues surfaced from the source

- `race_results.csv`: 95 extra rows repeat candidate `(raceId, driverId)` keys. These are retained, not dropped. Use a generated row key.
- `qualifying_results.csv`: one extra row repeats candidate `(raceId, driverId)`. Retain and inspect.
- `season_constructor_standings.csv`: 23 extra rows repeat candidate `(year, constructorId)` keys. Investigate before any measure assumes one row per constructor-season.
- `Dim_Drivers` has 917 rows, but only 860 distinct driver IDs are represented in `Fact_RaceResults`; use separate measures for directory size and fact coverage.
- A Grand Prix identity can map to several circuits, so don't collapse `Dim_GrandPrix` and `Dim_Circuits` into one key.

## Source-provided totals

Keep source pre-aggregated `total*` columns only in QA tables so fact-derived measures can be reconciled without accidentally using precomputed totals in report visuals. Due to duplicated/shared-car history, define the total-win aggregation deliberately and verify selected drivers and constructors separately against the source reference totals.
