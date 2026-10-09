# Project Walkthrough — Interview Notes

## A 60-second explanation

I built a Formula 1 performance analysis project in Power BI. I started with 12 CSV tables from F1DB, reviewed the data in Power Query, fixed type and query issues, and set up relationships between the result, driver, constructor, race and circuit tables. I created a date table and DAX measures for wins, points, podiums, position changes and non-classified results. I also checked the raw-data counts and selected findings with Python. The main focus was not just displaying KPIs, but making sure their definitions were correct—for example, a blank finishing position is not the same thing as an explicit DNF.

## What was the business goal?

To compare driver and constructor performance over time and make it easier to investigate race wins, points, qualifying performance, circuits and reliability-related outcomes.

## Why did you use Power Query?

The source was spread across CSV files and did not arrive in a report-ready format. I used Power Query to set types, handle errors and empty columns, create reporting tables, and make the preparation steps repeatable.

## Why create a date table?

I needed consistent year, month and quarter fields and a proper date table for time-intelligence measures. I sorted Month Name by Month Number to keep the calendar in chronological order.

## What was one data-quality issue?

A blank numeric finish position does not automatically mean DNF. The source labels 8,756 records as `DNF`, while 10,897 result rows have a blank `positionNumber`. I kept those definitions separate instead of using the blank count as a DNF count.

## Why not delete duplicate-looking rows?

A repeated candidate key does not automatically mean the record is wrong. F1 history has cases such as shared-car results, and some tables have more than one row for a race and driver. I flagged those combinations and used row counts or distinct race IDs depending on the question instead of deleting data without checking its meaning.

## How did you check the results?

I ran the Python audit included in this repository. It checks table counts, selected foreign-key relationships, possible duplicate keys, status distributions and win-share results. Those checks do not execute DAX; they provide an independent comparison against the original CSVs.

## Why is Red Bull 2023 highlighted?

The supplied snapshot has Red Bull winning 21 of 22 race events in 2023. The win share is 21 divided by 22, or 95.45%. It is a clear example of a result that can be explained directly from the data. It describes dominance in that season; it does not, by itself, explain why the team was dominant.

## What are the limitations?

The files are a fixed F1DB snapshot rather than a live feed. The 2026 schedule is present, but result data is incomplete after round 8 in this release. Pit-stop data starts in 1994, and points systems and race formats changed over time.

## If they ask to see the PBIX

The `.pbix` file is not included in this repository. I kept the Power Query transformations, DAX measures, model diagram, analysis outputs and screenshots here; the interactive file would need to be shared separately if a reviewer asks to open it.
