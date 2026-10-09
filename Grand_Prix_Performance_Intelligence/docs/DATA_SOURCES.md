# Data Sources and Scope

## Source snapshot

- **Dataset:** F1DB — Open Source Formula 1 Database
- **Repository:** <https://github.com/f1db/f1db>
- **Release version stated in the supplied project files:** `v2026.8.2`
- **Release date stated in the supplied project files:** 2026-07-02
- **Format:** UTF-8 CSV, one file per relational table
- **License stated in the supplied project files:** CC BY 4.0

Required attribution for published output:

> Data sourced from F1DB (https://github.com/f1db/f1db), licensed under CC BY 4.0.

## Source table counts

| File | Rows | Grain / notes |
|---|---:|---|
| `races.csv` | 1,171 | One scheduled event per season/round; includes schedule rows with no results in the snapshot |
| `race_results.csv` | 27,467 | Driver/constructor result record; do not assume `(raceId, driverId)` is unique |
| `qualifying_results.csv` | 26,888 | Qualifying classification record; candidate `(raceId, driverId)` repeats once |
| `pit_stops.csv` | 22,308 | One recorded pit-stop event; coverage spans 1994–2026 in this extract |
| `fastest_laps.csv` | 17,020 | Fastest-lap classification entries, not only the fastest driver in each race |
| `drivers.csv` | 917 | Driver directory; 860 distinct driver IDs appear in `race_results.csv` |
| `constructors.csv` | 187 | Constructor directory; 186 IDs appear in `race_results.csv` |
| `circuits.csv` | 78 | Physical circuit entity |
| `countries.csv` | 249 | Country reference list; many rows are not used in the competition fact tables |
| `grands_prix.csv` | 54 | Event-name identity; one identity may map to several physical circuits |
| `season_driver_standings.csv` | 1,680 | Driver-season standings; year/driver candidate key is unique in this file |
| `season_constructor_standings.csv` | 721 | Constructor-season standings; 23 extra rows repeat candidate `(year, constructorId)` keys and need investigation |

All 12 input files contain **98,740 rows combined**. The six fact inputs contain 96,084 rows before model transformations.

## Snapshot freshness

The frozen 2026 source has race-result rows through round 8. Fourteen schedule rows have no result rows in this extract. Some corresponding calendar dates are now in the past; the source package should therefore be described as a historical snapshot released 2 July 2026, not current 2026 results.

## Data interpretation notes

- `positionNumber` blank is not synonymous with `DNF`; `positionText` also includes statuses such as `DNQ`, `DNS`, `DNPQ`, `NC`, `DSQ`, `EX` and `DNP`.
- `race_results.time` includes time strings and lap-gap strings. Use the provided numeric `timeMillis` where suitable; don't convert raw text directly to a number.
- `race_results.points` is structurally blank for many entries, including entries outside points positions and historical formats. Do not automatically impute zero without confirming the metric definition.
- Historical shared-car and constructor/result cases mean candidate keys should be profiled, not treated as absolute truths.
- `countryOfBirthCountryId` and `nationalityCountryId` differ for 61 rows in the supplied driver directory.
- Pit-stop gaps before 1994 are a source-coverage limitation, not evidence of zero stops.
- Points systems, qualifying formats, grid size and race schedules vary across the 1950–2026 range. Era-based comparisons need explicit labels and caveats.
