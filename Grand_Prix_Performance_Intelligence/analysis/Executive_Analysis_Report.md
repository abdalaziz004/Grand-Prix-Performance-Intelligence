# Executive Analysis

## Summary

I used the F1DB snapshot to compare historic Formula 1 performance and check whether the source supports the metrics being reported. The clearest season result is Red Bull in 2023, with 21 wins from 22 race events (95.45%). The most important data-quality finding is that a blank finishing position and an explicit DNF are not the same thing.

## Scope

The snapshot contains 12 CSV tables and 98,740 rows excluding headers. It includes race results, qualifying, fastest laps, pit stops, drivers, constructors, circuits, countries, Grand Prix names and season standings. The data is a fixed release (`v2026.8.2`), not a live feed.

| Item | Count |
|---|---:|
| Race calendar rows | 1,171 |
| Result rows | 27,467 |
| Distinct races with result rows | 1,157 |
| Driver records in directory | 917 |
| Drivers found in race results | 860 |
| Pit-stop records | 22,308 |

## Findings

### 1. Constructor win share in 2023

Red Bull recorded a winning result in 21 of the 22 race events represented for 2023. The win share is:

`21 / 22 = 95.45%`

This is useful when describing the degree of dominance within a season. It doesn't explain the cause of the results on its own; that would require looking at drivers, qualifying, reliability, race pace and other context.

### 2. Blank positions versus DNF

There are 10,897 result rows with a blank numeric `positionNumber` (39.67% of result rows). The literal source label `positionText = DNF` appears 8,756 times (31.88%). Other blank-position rows include different status outcomes, so I kept the measures separate. The broader blank-position measure should not be labelled as a mechanical failure rate.

### 3. The 2026 extract is incomplete

The calendar contains 14 scheduled 2026 rows without corresponding result rows in this snapshot. These are later rounds missing from the captured release. They should not be read as cancelled races, zero results or a complete 2026 season.

### 4. Natural-key assumptions need checking

Some combinations that look like unique keys are repeated. The audit found 95 extra `(raceId, driverId)` candidate-key rows in race results and 23 extra `(year, constructorId)` candidate-key rows in season constructor standings. The source rows are preserved. I use generated row IDs to identify source records and distinct race IDs when the question is about race events.

### 5. Race identity and circuit identity differ

A named Grand Prix may use different physical circuits across its history. In this snapshot, the French Grand Prix identity maps to seven circuits; the United States and Spanish Grand Prix identities each map to six. That is why the model keeps Grand Prix and circuit as separate dimensions.

### 6. Coverage matters

The pit-stop table spans 1994–2026. Missing pit-stop data before 1994 must not be interpreted as zero stops. Championship points and qualifying formats also changed over time, so raw cross-era totals need context.

## What this means for the report

- Put KPI definitions in the report or tooltip, not only in this document.
- Show both explicit DNF rate and blank-finishing-position rate when discussing reliability.
- Use win share to compare seasons rather than comparing raw win counts alone.
- Keep event-level results separate from season standings.
- Display the snapshot date and note that 2026 results are incomplete.
- When discussing circuits, distinguish the Grand Prix name from the physical venue.

## Method and limitations

The raw CSV checks are reproducible with `python scripts/run_analysis.py`. The report measures are documented in `powerbi/dax/measures.dax`. Counts may differ depending on whether a measure counts result rows, distinct race events or season-standing records; the definition should always be stated. The Python audit is a second check against the source files, not a substitute for the Power BI model itself.
