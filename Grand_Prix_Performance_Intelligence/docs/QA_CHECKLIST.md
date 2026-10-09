# Quality Checks and Results

I used two types of checks in this project: checks against the original CSV files, and checks inside the Power BI model.

## Checks run against the CSV files

These are reproducible from `scripts/run_analysis.py`.

| Check | Result | Status |
|---|---|---|
| Load the 12 expected CSV files | All 12 loaded | PASS |
| Race calendar IDs | 1,171 rows; `races.id` is unique | PASS |
| Result row count | 27,467 | PASS |
| Checked foreign keys from result/qualifying/pit-stop/fastest-lap tables | No orphan IDs in the tested relationships | PASS |
| `races.circuitId` references | No unmatched circuit IDs | PASS |
| `races.grandPrixId` references | No unmatched Grand Prix IDs | PASS |
| Candidate key `(raceId, driverId)` in race results | 95 extra rows over unique combinations | REVIEW — retained and documented |
| Candidate key `(raceId, driverId)` in qualifying | 1 extra row over unique combinations | REVIEW — retained and documented |
| Candidate key `(year, constructorId)` in constructor standings | 23 extra rows over unique combinations | REVIEW — retained and documented |
| Blank finish position vs explicit DNF | 10,897 blank positions; 8,756 explicit DNF rows | PASS — separate definitions |
| Pit-stop coverage | 1994–2026 in this snapshot | PASS — coverage gap documented |
| 2026 calendar coverage | 14 schedule rows have no result rows | REVIEW — partial source snapshot |

Detailed results are in `outputs/foreign_key_audit.csv`, `outputs/candidate_key_audit.csv`, `outputs/finish_status_distribution.csv` and `outputs/DATA_AUDIT_REPORT.md`.

## Power BI checks from the working session

- Reviewed column types and data quality in Power Query.
- Corrected a field-name reference issue involving `time_clean` and reviewed the resulting queries.
- Created a calendar table, added Year/Month/Quarter fields, sorted Month Name by Month Number and marked the calendar as a Date Table.
- Created active relationships with single-direction filtering.
- Created and checked the core KPI measures against the report filters and source values.
- Kept result-level rows separate from season standings and kept explicit DNF separate from blank finish position.

The screenshots in `assets/powerbi_screenshots/` show the model and relationship setup from the Power BI Desktop work session. The `.pbix` file itself is not included in this repository, so the model cannot be reopened from this package alone.

## KPI notes

- `Total Race Starts` is implemented as a row count in the measure library. Unless actual starts are filtered separately, the report label should be **Result Entries**.
- `Total Wins` counts distinct race IDs with `positionNumber = 1`, rather than raw winning rows.
- `Non-Classified Entry Rate` is based on a blank numeric finish position; `Explicit DNF Rate` uses `positionText = "DNF"`.
- Fourteen scheduled 2026 rows have no result rows in this source release. Don't use planned 2026 calendar events as if they all had complete results.
