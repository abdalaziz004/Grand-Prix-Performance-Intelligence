# Data Dictionary — Analytical Columns

This is a practical dictionary for the fields used in the model and headline analysis. The raw CSV headers are preserved in `data/raw/`; this document does not attempt to redefine every source field.

## Race calendar and reference dimensions

| Table / field | Meaning | Notes |
|---|---|---|
| `races.id` → `Dim_Races[RaceId]` | Unique scheduled event ID | Primary race-event key in this snapshot |
| `races.year`, `races.round` | Season year and round order | 2026 calendar extends beyond the result coverage in this release |
| `races.date` → `Dim_Races[RaceDate]` | Scheduled race date | Relates to `Dim_Date[Date]` |
| `races.grandPrixId` | Named Grand Prix identity | Can map to multiple circuits through history |
| `races.circuitId` | Physical venue ID | Keep separate from the Grand Prix identity |
| `circuits.latitude`, `circuits.longitude` | Circuit coordinates | Use for map visuals; preserve source precision |
| `circuits.type` | Source circuit type label | Retain source category; avoid unreviewed remapping |
| `circuits.countryId` | Host-country key for the circuit | Country display name is merged into `Dim_Circuits` |
| `drivers.nationalityCountryId` | Driver nationality-country key | Not interchangeable with `countryOfBirthCountryId` |
| `constructors.countryId` | Constructor country key | Descriptive property; not a driver-nationality key |

## Race results (`race_results.csv` → `Fact_RaceResults`)

| Field | Meaning | Transformation / measure notes |
|---|---|---|
| `raceId` | Race-event foreign key | Links to `Dim_Races[RaceId]`; typed whole number |
| `driverId` | Driver foreign key | Text key; links to `Dim_Drivers[DriverId]` |
| `constructorId` | Constructor foreign key | Text key; links to `Dim_Constructors[ConstructorId]` |
| `positionNumber` | Numeric classified result position where present | Blank for more than explicit DNFs; must remain nullable numeric |
| `positionText` | Source finish/status text | Preserves values such as `DNF`, `DNQ`, `DNS`, `DNPQ`, `NC`, `DSQ`, `EX`, `DNP` and numeric-looking positions |
| `gridPositionNumber` | Numeric grid position where present | Used with finish position to estimate positions gained/lost |
| `qualificationPositionNumber` | Source qualifying position number | Useful for comparison; may be blank in older/exceptional records |
| `points` | Source race-result points | Nullable; fractional points exist; rules change across history |
| `positionsGained` | Source-provided start-to-finish position gain | Useful for spot-checks; define whether your own metric uses the source field or recomputation |
| `time`, `gap`, `interval` | Source text representations | May be a duration, a lap gap or blank; don't cast all text directly to numeric |
| `timeMillis`, `gapMillis`, `intervalMillis` | Source-provided numeric time values where available | Prefer for aggregation and comparison when matching the intended meaning |
| `reasonRetired` | Raw source retirement reason text | Retained alongside a broad heuristic `RetirementCategory` |
| `sharedCar` | Historical shared-car flag | A reason composite candidate keys may not be unique as expected |
| `polePosition`, `fastestLap`, `driverOfTheDay`, `grandSlam` | Source flags | Parse to nullable logical values; profile blank representation before final use |
| `pitStops` | Source row-level number of pit stops | Check source definition and duplicates before summing across result rows |
| `ClassifiedFieldSize` | Project-derived classified-driver count per race | Used to normalize grid-to-finish movement |
| `IsBlankFinishPosition` | Project-derived Boolean for blank numeric result position | It measures blank finish position, not exclusively a DNF |
| `RetirementCategory` | Project-derived broad category | Rule-based convenience grouping, not an official FIA classification |
| `ResultRowId` | Generated row identifier | Technical model key; does not replace source business keys |

## Qualifying results (`qualifying_results.csv` → `Fact_Qualifying`)

| Field | Meaning | Notes |
|---|---|---|
| `raceId`, `driverId`, `constructorId` | Event, driver and constructor foreign keys | Related to dimensions; candidate `(raceId, driverId)` repeats once |
| `positionNumber` | Numeric qualifying classification | Preserve nulls / non-classification |
| `timeMillis`, `q1Millis`, `q2Millis`, `q3Millis` | Source numeric duration fields | Q1/Q2/Q3 are populated only for corresponding formats/eras |
| `time`, `q1`, `q2`, `q3` | Display text duration fields | Keep for tooltip/readability; do not aggregate strings |
| `QualifyingRowId` | Generated row ID | Preserves source rows with duplicate candidate keys |

## Pit stops and fastest laps

| Table / field | Meaning | Notes |
|---|---|---|
| `pit_stops.raceId`, `driverId`, `constructorId` | Parent race/driver/team keys | Foreign-key checks passed for the supplied data |
| `pit_stops.stop`, `lap` | Stop sequence number and lap | Useful for stop-number distribution and pit strategy context |
| `pit_stops.timeMillis` | Pit-stop duration in milliseconds | Source field; pit-stop table begins in 1994 in the supplied snapshot |
| `fastest_laps.positionNumber` | Classification/ranking of the fastest-lap entries | The file contains more than one ranked entry per race, not just the outright fastest lap |
| `fastest_laps.timeMillis` | Lap-time duration in milliseconds | Prefer source numeric duration for comparisons |

## Season-level standings

| Table / field | Meaning | Notes |
|---|---|---|
| `season_driver_standings.year`, `driverId` | Driver-season standing identity | 1,680 rows; candidate `(year, driverId)` is unique in this file |
| `season_constructor_standings.year`, `constructorId` | Constructor-season standing identity | 721 rows; 23 extra rows repeat candidate `(year, constructorId)` keys |
| `positionNumber` | Final standing position where numeric | Nullable numeric |
| `points` | Season standings points | Different grain from race-result points; do not merge into race results |
| `championshipWon` | Source Boolean champion flag | Parse as nullable logical, then inspect blanks |
| `SeasonDriverRowId`, `SeasonConstructorRowId` | Generated model IDs | Preserve source row distinctions while key exceptions are investigated |

## Measures and naming

The requested assignment name `Total Race Starts` is implemented as a row count to match the original task, but that table includes result status rows which were not actual starts. In any public visual, the honest label is **Race-result entries** unless a verified start definition is added. Similarly, use separate labels for `Blank finish-position rate` and `Explicit DNF rate`.
