# Business Requirements

## Background

The project is an F1 performance report for someone who needs to compare drivers and constructors across seasons. The aim is to make the key measures easy to interpret and to avoid comparing unlike data without explaining the limitation.

## Questions the report should answer

1. Which drivers and constructors have the most wins in the selected period?
2. How has points performance changed over time?
3. Which constructors had the highest share of race wins within a season?
4. How do starting position and finishing position compare?
5. How do explicit DNFs and other non-classified results vary over time?
6. What can we learn from qualifying results, fastest laps and pit-stop records?
7. Which Grand Prix names have been held at more than one circuit?
8. Which comparisons need a caveat because source coverage or sporting rules changed over time?

## Main report users

- A team or driver analyst comparing performance.
- A broadcaster or sports-media analyst looking for trends and storylines.
- A manager who wants a quick season or constructor summary.

## Expected report pages

- Executive overview
- Season and championship trends
- Circuits and geography
- Driver and constructor comparison
- Qualifying and race-day performance
- Reliability and unusual race outcomes

## KPIs and definitions

| KPI | Definition used in this project | Note |
|---|---|---|
| Total Wins | Distinct race IDs where the selected driver or constructor has a winning row | Distinct race events avoid double counting repeated winning rows for the same entity |
| Total Points | Sum of points in the filtered race-result records | Raw totals are not directly comparable across all scoring eras |
| Win Rate | Total Wins divided by result rows in the current context | The denominator is result records; it should not be described as a clean start rate without a start definition |
| Explicit DNF Rate | Rows with `positionText = DNF` divided by result rows | Literal source status |
| Blank Finish Position Rate | Rows where numeric `positionNumber` is blank divided by result rows | Broader than DNF |
| Average Position Change | Average of grid position minus finish position when both are present | Positive means the driver gained places |

## Data and reporting requirements

- Preserve the supplied source data and keep cleanup steps reviewable.
- Keep event-level results separate from season-level standings.
- Use single-direction relationships from dimensions to facts where practical.
- Define time-intelligence behavior using a calendar table.
- Show the selected season or date range on report pages.
- Make limitations visible when a metric depends on incomplete or historically inconsistent data.
- Keep Python checks separate from Power BI validation; each one checks a different part of the workflow.
