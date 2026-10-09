# Build Notes

These notes record the main steps and decisions from working on the project in Power BI Desktop.

## Import and profiling

I started with the 12 CSV files in `data/raw/`. Before writing measures, I checked the available columns, data types, empty fields and row counts. Power Query's column quality and distribution views helped identify columns that needed attention.

## Fixing query errors

One issue was a query step referring to a field called `time_clean` when that field was not available under that name in the current query. I checked the Applied Steps and the formula bar instead of treating the error as a problem with the source file itself. I also reviewed a small group of error rows and empty columns during cleanup, then checked the resulting tables again.

The lesson was that Power Query errors can come from the order of transformations or from a changed column name; deleting error rows should not be the first reaction before checking why they appeared.

## Date table

I created a calendar table from the minimum and maximum dates in `races[date]`. It includes Year, Month Number, Month Name, Quarter and Year-Month. Month Name was sorted by Month Number so visuals do not sort month names alphabetically. The date table was marked as a Date Table for time-intelligence measures.

## Relationships

I set up 14 active relationships between the race results, qualifying results, races, circuits, Grand Prix, drivers, constructors and standings tables. I used single-direction filtering rather than turning on bidirectional filtering just to make a visual respond. The relationship view and Manage Relationships dialog are included under `assets/powerbi_screenshots/`.

The final query pack groups the transformations into staging, dimensions and facts. That organization makes it easier to see each query's role and to rebuild the model consistently.

## KPI definitions

I kept explicit DNF separate from blank finish positions. The source has several outcomes, including non-starts and other non-classified states, so the empty numeric finishing position is not a reliable synonym for DNF.

For race wins, the analysis counts distinct race IDs per driver or constructor to avoid duplicate result rows inflating the number of winning events. The source-row count remains available separately for QA.

## Checks

The included Python script re-creates the source-table counts, win leaderboards, constructor win share by season, status distribution, candidate-key checks and selected foreign-key checks. This is a second check against the CSV files; it does not execute DAX or replace checking the visuals in Power BI.
