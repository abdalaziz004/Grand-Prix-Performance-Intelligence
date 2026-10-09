# Report Pages

The report is organized around six questions. Each page uses the same source snapshot, with the available year, driver, constructor and circuit filters applied where they make sense.

## 1. Executive Overview

**Question:** What does performance look like in the selected period?

- KPI cards for result entries, race events, wins, blank-position rate and explicit DNF rate.
- Trend line for wins by year.
- Bar chart of constructors by distinct winning race events.
- A callout for the strongest constructor season by win share.

## 2. Championship Trends

**Question:** How did results change over time?

- Wins and win share by season.
- Driver and constructor performance trends.
- Points trend with a note about historic scoring changes.
- Year/date selection using the date table.

## 3. Circuits & Geography

**Question:** Where have races been held, and how often did events move between circuits?

- Circuit map using latitude and longitude.
- Race-event counts by host country and continent.
- Grand Prix identity compared with the physical circuit.

## 4. Driver & Constructor Comparison

**Question:** Who has the strongest results in the selected period?

- Driver and constructor win rankings.
- Running points total.
- Constructor points contribution.
- Driver versus teammate comparison and championship-win streak where the selected context supports those measures.

## 5. Qualifying & Race-Day

**Question:** How well did a driver convert a starting position into a finishing position?

- Grid position compared with final position.
- Average positions gained or lost.
- Qualifying-to-race conversion index for records with both positions available.
- A note that qualifying formats and available data vary across eras.

## 6. Reliability & Race Outcomes

**Question:** How often did drivers fail to record a numeric finishing position, and what does the source say about the reason?

- Explicit DNF rate and blank-position rate shown separately.
- Distribution of source status labels by year or period.
- Races with unusually high blank-position rates.
- Pit-stop analysis limited to years covered by the file.
- Note about incomplete 2026 data.

## Report-wide choices

- Keep the selected year or date range visible.
- Keep driver, constructor and circuit filters consistent where the metric's grain allows it.
- Use `Dim_Date` for time intelligence.
- Keep race-level results and season standings in separate fact tables.
- State whether a KPI counts rows, distinct race events or distinct drivers.
