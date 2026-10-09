# Business Questions and Evidence-Based Answers

I used these questions to decide what the report should answer and to prepare for a project walkthrough. The answers below come from the included CSV snapshot and the analysis script; each answer includes the definition or caveat that matters for interpreting it.

| Business question | Snapshot answer | Business interpretation / caveat |
|---|---|---|
| 1. Which driver has the most distinct race wins? | Lewis Hamilton — 106 | Derived from result rows where `positionNumber = 1`, counted by distinct race ID per driver. |
| 2. Who is second in distinct race wins? | Michael Schumacher — 91 | Same definition as above. |
| 3. Where does Max Verstappen rank in the snapshot? | 71 distinct winning race events | Results are limited to the frozen F1DB release, not a live leaderboard. |
| 4. Which constructor has the most distinct winning race events? | Ferrari — 249 | Constructor entity IDs are counted as modeled by F1DB; don't infer modern brand lineage. |
| 5. Who follows Ferrari? | McLaren — 203 | Same distinct-race definition. |
| 6. Which constructor-season has the strongest win share? | Red Bull, 2023 — 21/22 = 95.45% | Race-event win share, normalized by event count in result records. |
| 7. How many result records are present? | 27,467 | Result records are not synonymous with confirmed actual starts. |
| 8. How many distinct events have race results? | 1,157 | 14 additional calendar rows have no result rows in the snapshot. |
| 9. Is every blank finish position a DNF? | No — 10,897 blanks vs. 8,756 literal DNF labels | Keep both metrics separate. |
| 10. What share of rows are explicitly marked DNF? | 31.88% | The denominator is all result rows in the snapshot. |
| 11. What share have a blank numeric position? | 39.67% | This includes multiple non-classified / non-starting statuses. |
| 12. Does the model have obvious orphan IDs? | None in the checked fact-to-dimension ID relationships | See `outputs/foreign_key_audit.csv`; this is not a claim that all business rules are error-free. |
| 13. Are event and driver keys always unique? | No — 95 extra rows repeat the candidate `(raceId, driverId)` key in `race_results` | Preserve rows until source semantics justify a specific deduplication rule. |
| 14. Does qualifying results have a candidate key exception? | One extra row repeats `(raceId, driverId)` | Review the specific case before using the key as unique. |
| 15. Are constructor standings unique per season/team? | 23 extra rows repeat `(year, constructorId)` | Preserve and inspect; use `Dim_Season` plus `Dim_Constructors` relationships and distinct-year logic for streaks. |
| 16. From which year does pit-stop data appear? | 1994 in this snapshot | Earlier years are not zero-stop seasons; timing coverage is absent. |
| 17. How many drivers are in the directory? | 917 | Directory size differs from 860 IDs appearing in race results. |
| 18. How many constructors appear in race results? | 186 | Directory has 187 constructor rows. |
| 19. Are birthplace and nationality identical? | No — 61 driver records differ (6.65%) | Pick the dimension that matches the question and name the chart field accordingly. |
| 20. Can a Grand Prix identity use multiple venues? | Yes — France maps to 7 circuit IDs in this snapshot | Keep Grand Prix identity and circuit as separate dimensions. |
| 21. How many circuit IDs map to the United States GP identity? | 6 | In this release's `races.csv`; the event name is not a venue key. |
| 22. How many calendar race rows are assigned to Italy's circuits? | 110 | This counts schedule rows in `races.csv`, not exclusively race results populated in the fact. |
| 23. Was 2023 a dominant season for Red Bull? | Yes — 21 of 22 distinct events with results (95.45%) | Use the ratio rather than total points alone for historical dominance. |
| 24. Can total points be compared directly across 1950–2026? | No | Points and bonus rules changed; show period context and use a validated scoring-era definition or within-era ratios. |
| 25. Is the 2026 season complete in this package? | No — results are populated through round 8; 14 calendar rows have no result rows | Refresh the dataset before any current-season report. |
