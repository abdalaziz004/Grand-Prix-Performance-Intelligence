# Power Query Files

The `.pq` files contain the query definitions used to prepare the F1DB tables for the model. Each file is a separate query to add through **Transform data → Advanced Editor** in Power BI Desktop.

## Setup order

1. Create a Text parameter named `pDataFolder` and set it to the full path of `data/raw/`.
2. Add the `Staging_*.pq` queries. Turn off Enable load for these source-shaped tables.
3. Add the helper functions: `fxParseDurationMilliseconds`, `fxRetirementCategory` and `fxNullableBoolean`.
4. Add the `Dim_*.pq` queries.
5. Add the `Fact_*.pq` queries and the two `QA_SourceProvidedTotals_*.pq` queries.
6. Use the table and column names in `docs/DATA_MODEL.md` when setting up relationships and DAX.

## Query groups

- `Staging_*.pq`: source files with minimal type handling.
- `fx*.pq`: reusable functions for duration strings, retirement labels and nullable Boolean values.
- `Dim_*.pq`: date, race, driver, constructor, circuit, Grand Prix and season dimensions.
- `Fact_*.pq`: race results, qualifying, fastest laps, pit stops and season standings.
- `QA_SourceProvidedTotals_*.pq`: reference queries for checks, not report visuals.

## Duration fields

The source has millisecond fields such as `timeMillis`, `q1Millis`, `gapMillis` and `intervalMillis`. Those are preferred for calculations when available. Raw duration text is kept for checking and display. A gap such as `+1 Lap` is not an elapsed time, so the parser leaves it blank instead of converting it into a duration.
