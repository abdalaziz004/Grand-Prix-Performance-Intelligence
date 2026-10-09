# DAX Measure Catalog

The DAX definitions are stored in [`powerbi/dax/measures.dax`](../powerbi/dax/measures.dax). The comments beside the measures describe the definition and the way the result should be read.

| Measure | What it calculates | How to read it |
|---|---|---|
| `Total Race Starts` | Count of result rows in the current filter context | Because this is a row count, use “Result Entries” as the visible label unless actual starts are filtered separately |
| `Total Wins` | Distinct race IDs with `positionNumber = 1` | Counts race events for the selected driver or constructor, rather than raw winning rows |
| `Total Championship Points` | Sum of points from result rows | Interpret historical totals with the scoring-system caveat |
| `Distinct Drivers` | Distinct driver IDs represented in result rows | 860 in this snapshot; the driver directory contains 917 rows |
| `Win Rate %` | Wins divided by result entries in the selected context | The denominator is visible in the measure definition and should be explained in the report |
| `Non-Classified Entry Rate` | Rows where `positionNumber` is blank divided by result rows | Broader than explicit DNF |
| `Explicit DNF Rate` | Rows whose status text is exactly `DNF` divided by result rows | Narrower literal DNF definition |
| `Podium Count` | Result rows with finishing position 1, 2 or 3 | Blank positions are excluded |
| `Average Grid-to-Finish Position Change` | Average of grid position minus finish position | Positive results mean positions gained |
| `Prior Season Wins` | Wins for the prior matching date period | Requires `Dim_Date` to be set up as the date table |
| `Wins YoY % Change` | Change in wins versus the prior period | Blank where the prior-period value is unavailable |
| `Running Total Championship Points` | Points accumulated up to the current date | Keeps driver and constructor context while removing date filters from the cumulative calculation |
| `Rank by Total Wins` | Dynamic driver rank | Responds to the report's selections |
| `Rank Constructor by Total Wins` | Dynamic constructor rank | Responds to the report's selections |
| `Top 10 Driver Flag` | 1 for drivers ranked in the top 10 | Use as a visual-level filter |
| `Constructor Points Contribution %` | Selected constructor points divided by all constructor points in the same context | Keeps other selected filters in place |
| `Reporting Era` | Working year buckets for comparisons | These are reporting buckets, not a statement of exact official regulations |
| `Dynamic Report Title` | Title using selected constructor and year span | Useful when the report is filtered |
| `Qualifying-to-Race Conversion Index` | Grid-to-finish movement normalized by classified field size | Only includes rows with a valid grid and finish position |
| `Anomalous Race Flag` | Flags a race with a blank-position rate more than two population standard deviations above the historic mean | An analytical flag for investigation, not proof of a cause |
| `Longest Constructor Championship Win Streak` | Longest sequence of consecutive championship-winning years | Requires one constructor in the selected context |
| `Points Above Average Teammate` | Selected driver season points minus the average for other drivers who raced for the same constructor and season | With mid-season substitutions, the definition averages the other drivers represented for that constructor/year |
| `Grand Slam Count` / `Grand Slam Rate` | Grand Slam records and their share of distinct wins | Check the `grandSlam` source definition and selected entity before interpreting the rate |

## Supporting measures

The file also includes measures for race events with results, race events with winning results, drivers/constructors in the directory, average pit-stop time and average pit stops per result entry.

## Formatting

- Counts: whole numbers with thousands separators.
- Points: one or two decimals where needed.
- Rates and shares: percentage, normally one or two decimal places.
- Duration: show a unit such as seconds; don't display raw milliseconds without a label.
- Flags: label as Yes/No in a report instead of showing unexplained 0/1 values.
