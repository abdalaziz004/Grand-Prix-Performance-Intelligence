# Transformation and Data-Quality Decision Log

## Decisions

| Area | Decision | Why it matters | Validation / caveat |
|---|---|---|---|
| Source tables | Keep the 12 source CSVs unchanged under `data/raw/` | Reproducibility and traceability | Python audit reads, but does not mutate, source files |
| Staging | Separate source-shaped `Staging_*` queries | Keeps source ingestion distinct from business logic | Disable staging load in Power BI |
| Keys | Add a generated row index to each event/season fact | Some source candidate natural keys repeat | Preserve source records; don't use the generated index to erase business-level duplicates |
| Result positions | Convert numeric-looking `positionNumber` values to numeric, with non-numeric/blank values remaining null | Enables sorting, finish-position and null-status measures | Keep `positionText` as the original status label |
| Non-classification | Keep `IsBlankFinishPosition` and literal `positionText = DNF` as separate definitions | Blank positions include DNQ, DNS, DNPQ, NC, DSQ and other statuses | Report both blank-position rate and explicit DNF rate |
| Durations | Prefer source-provided `*Millis` fields where available; retain original text | Raw fields include clock strings and lap-gap text | `fxParseDurationMilliseconds` is a fallback; inspect odd strings and nulls before using it for KPIs |
| Boolean-like values | Use a nullable Boolean parser | Avoid interpreting unknown / blank as false without evidence | Review each boolean-looking column before final refresh |
| Retirement text | Add a broad, rule-based category while retaining `reasonRetired` | Reduces visual noise without losing raw evidence | Category rules are heuristic; don't present them as official incident classifications |
| Field-size normalization | Count distinct driver IDs with classified finish positions per race and merge as `ClassifiedFieldSize` | Normalizes grid-to-finish position movement to field size | Source shared-car records mean driver/event grain needs attention |
| Driver nationality | Merge country names from `nationalityCountryId`, retaining the key | Lets the dashboard label nationality explicitly | 61 of 917 driver directory rows differ between birth country and nationality |
| Constructor country | Merge source country label into constructor dimension | Useful for segmentation without using an ambiguous country relationship | Constructor nationality is not the same concept as driver nationality |
| Circuit geography | Merge host country/continent and retain coordinates | Supports maps and circuit-level breakdowns | Circuit identity is not Grand Prix identity |
| Grand Prix identity | Keep `Dim_GrandPrix` separate from `Dim_Circuits` | One named Grand Prix can move between venues | France maps to seven circuit IDs in this snapshot |
| Date table | Build a contiguous date dimension spanning min/max event dates | Enables standard DAX time intelligence | Mark `Dim_Date[Date]` as the model Date Table; sort MonthName by MonthNumber |
| Career totals in dimensions | Keep source `total*` totals in QA-only queries, not reporting dimensions | Avoids mixing source summaries with fact-derived metrics | Reconcile totals by entity and document shared-car/aggregation differences |
| Season standings | Keep separate season-grain facts | Prevents fact-to-fact fan traps and duplicated sums | Relate through `Dim_Season`; do not merge into race-result fact |
| 2026 coverage | Do not impute missing result rows for scheduled 2026 rounds | The frozen release is not complete for current-season reporting | Refresh source before publishing current-season results |

## Why the Power Query duration function returns milliseconds

A numeric millisecond value is easier to aggregate, compare and validate than a `duration` object. The source already provides fields such as `timeMillis`, `q1Millis`, `q2Millis`, `q3Millis`, `gapMillis` and `intervalMillis` in relevant tables. Where the source has a lap-gap such as `+1 Lap`, the parser returns null because it isn't an elapsed duration. Raw text remains available for display and audit.

## Why duplicate rows are not dropped automatically

Source duplicate checks reveal 95 extra rows for the candidate key `(raceId, driverId)` in race results, one in qualifying results and 23 for `(year, constructorId)` in constructor standings. The files include historical shared-car and team/result edge cases. A silent `Table.Distinct` step could remove legitimate history; retain and review source rows, and use explicit row IDs for model identity.
