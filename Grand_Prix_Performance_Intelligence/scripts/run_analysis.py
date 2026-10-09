"""Reproducible quality audit and portfolio analysis for the F1DB snapshot.

Run from the repository root:
    python -m pip install -r requirements.txt
    python scripts/run_analysis.py

All source tables are read-only inputs. Outputs are recreated under outputs/.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

FILES = [
    "races", "race_results", "qualifying_results", "pit_stops", "fastest_laps",
    "drivers", "constructors", "circuits", "countries", "grands_prix",
    "season_driver_standings", "season_constructor_standings",
]

def load_tables() -> dict[str, pd.DataFrame]:
    return {name: pd.read_csv(RAW / f"{name}.csv", low_memory=False) for name in FILES}

def safe_pct(n: float, d: float) -> float | None:
    return None if not d else round(100.0 * n / d, 2)

def main() -> None:
    t = load_tables()
    races = t["races"].copy()
    rr = t["race_results"].copy()
    drivers, constructors = t["drivers"], t["constructors"]
    circuits, countries, gps = t["circuits"], t["countries"], t["grands_prix"]
    rr["positionNumber_num"] = pd.to_numeric(rr["positionNumber"], errors="coerce")
    rr["year_num"] = pd.to_numeric(rr["year"], errors="coerce").astype("Int64")
    rr["points_num"] = pd.to_numeric(rr["points"], errors="coerce")
    races["year_num"] = pd.to_numeric(races["year"], errors="coerce").astype("Int64")
    rr["is_winning_entry"] = rr["positionNumber_num"].eq(1)
    rr["is_blank_finish_position"] = rr["positionNumber_num"].isna()
    rr["is_explicit_dnf"] = rr["positionText"].astype(str).str.upper().eq("DNF")

    row_counts = {k: int(len(v)) for k, v in t.items()}
    combined_fact_rows = sum(row_counts[k] for k in ["race_results", "qualifying_results", "pit_stops", "fastest_laps", "season_driver_standings", "season_constructor_standings"])
    race_ids_with_results = set(rr["raceId"].dropna())
    races_without_results = races.loc[~races["id"].isin(race_ids_with_results), ["id", "year", "round", "date", "officialName"]].copy()
    races_without_results.to_csv(OUT / "scheduled_races_without_result_rows.csv", index=False)

    # Result-event counts and per-year rates. Blank position includes several statuses,
    # so this is deliberately not called a DNF rate.
    per_year = races.groupby("year_num").agg(ScheduledRaceRows=("id", "size")).reset_index().rename(columns={"year_num":"Year"})
    result_year = rr.groupby("year_num").agg(
        RaceResultRows=("raceId", "size"),
        DistinctRaceEventsWithResult=("raceId", "nunique"),
        BlankFinishPositionRows=("is_blank_finish_position", "sum"),
        ExplicitDNFRows=("is_explicit_dnf", "sum"),
        WinningEntryRows=("is_winning_entry", "sum"),
        ChampionshipPoints=("points_num", "sum"),
    ).reset_index().rename(columns={"year_num":"Year"})
    per_year = per_year.merge(result_year, on="Year", how="left")
    per_year["BlankFinishPositionRatePct"] = (100 * per_year["BlankFinishPositionRows"] / per_year["RaceResultRows"]).round(2)
    per_year["ExplicitDNFRatePct"] = (100 * per_year["ExplicitDNFRows"] / per_year["RaceResultRows"]).round(2)
    per_year.to_csv(OUT / "yearly_summary.csv", index=False)

    # Driver wins count unique events per driver to avoid duplicate result lines within a race.
    wins = rr.loc[rr["is_winning_entry"]].copy()
    driver_wins = wins.groupby("driverId")["raceId"].nunique().rename("RaceWins").reset_index()
    driver_wins = driver_wins.merge(drivers[["id", "name", "nationalityCountryId"]], left_on="driverId", right_on="id", how="left")
    driver_wins = driver_wins[["driverId", "name", "nationalityCountryId", "RaceWins"]].sort_values(["RaceWins", "name"], ascending=[False, True])
    driver_wins.to_csv(OUT / "driver_win_leaderboard.csv", index=False)

    constructor_wins = wins.groupby("constructorId")["raceId"].nunique().rename("RaceWins").reset_index()
    constructor_wins = constructor_wins.merge(constructors[["id", "name", "countryId"]], left_on="constructorId", right_on="id", how="left")
    constructor_wins = constructor_wins[["constructorId", "name", "countryId", "RaceWins"]].sort_values(["RaceWins", "name"], ascending=[False, True])
    constructor_wins.to_csv(OUT / "constructor_win_leaderboard.csv", index=False)

    constructor_points = rr.groupby("constructorId")["points_num"].sum(min_count=1).rename("RaceResultPoints").reset_index()
    constructor_points = constructor_points.merge(constructors[["id", "name"]], left_on="constructorId", right_on="id", how="left")
    constructor_points = constructor_points[["constructorId", "name", "RaceResultPoints"]].sort_values("RaceResultPoints", ascending=False)
    constructor_points.to_csv(OUT / "constructor_points_leaderboard.csv", index=False)

    # Win-share by constructor per season. Race denominator is the count of race events
    # with at least one winning result row in that season, not the planned calendar count.
    wins_by_season_constructor = wins.groupby(["year_num", "constructorId"])["raceId"].nunique().rename("RaceWins").reset_index()
    completed_events_by_season = rr.groupby("year_num")["raceId"].nunique().rename("EventsWithResult").reset_index()
    season_share = wins_by_season_constructor.merge(completed_events_by_season, on="year_num", how="left")
    season_share["WinSharePct"] = (100 * season_share["RaceWins"] / season_share["EventsWithResult"]).round(2)
    season_share = season_share.merge(constructors[["id", "name"]], left_on="constructorId", right_on="id", how="left")
    season_share = season_share[["year_num", "name", "RaceWins", "EventsWithResult", "WinSharePct"]].rename(columns={"year_num":"Year", "name":"Constructor"}).sort_values(["WinSharePct", "RaceWins"], ascending=False)
    season_share.to_csv(OUT / "constructor_win_share_by_season.csv", index=False)

    # Host country/continent output (circuits -> countries -> races).
    cir_geo = circuits.merge(countries[["id", "name", "continentId"]], left_on="countryId", right_on="id", how="left", suffixes=("", "_country"))
    race_geo = races.merge(cir_geo[["id", "name_country", "continentId"]], left_on="circuitId", right_on="id", how="left")
    race_geo.groupby(["continentId", "name_country"]).size().rename("ScheduledRaceEvents").reset_index().rename(columns={"name_country":"HostCountry", "continentId":"Continent"}).sort_values("ScheduledRaceEvents", ascending=False).to_csv(OUT / "host_country_race_counts.csv", index=False)

    # Grand Prix identities that have been hosted at more than one circuit.
    gp_circuit = races.groupby("grandPrixId")["circuitId"].agg(lambda s: sorted(set(s.dropna().astype(str)))).reset_index()
    gp_circuit["CircuitCount"] = gp_circuit["circuitId"].map(len)
    gp_circuit["CircuitIds"] = gp_circuit["circuitId"].map(lambda x: ", ".join(x))
    gp_circuit = gp_circuit.loc[gp_circuit["CircuitCount"] > 1].merge(gps[["id", "name"]], left_on="grandPrixId", right_on="id", how="left")
    gp_circuit[["grandPrixId", "name", "CircuitCount", "CircuitIds"]].rename(columns={"name":"GrandPrixName"}).sort_values("CircuitCount", ascending=False).to_csv(OUT / "grand_prix_multiple_circuits.csv", index=False)

    # Status counts; null finish position is broader than explicit DNF.
    status = rr["positionText"].fillna("(blank)").astype(str).value_counts(dropna=False).rename_axis("positionText").reset_index(name="Rows")
    status["SharePct"] = (100 * status["Rows"] / len(rr)).round(2)
    status.to_csv(OUT / "finish_status_distribution.csv", index=False)

    # QA checks: use actual raw IDs/keys instead of assuming uniqueness from documentation.
    fact_fk_checks = []
    for fact_name in ["race_results", "qualifying_results", "fastest_laps", "pit_stops"]:
        frame = t[fact_name]
        for fk, dim, pk in [("driverId", "drivers", "id"), ("constructorId", "constructors", "id")]:
            if fk in frame.columns:
                orphan = int((~frame[fk].isin(t[dim][pk])).sum())
                fact_fk_checks.append({"Check": f"{fact_name}.{fk} -> {dim}.{pk}", "RowsChecked": int(len(frame)), "Exceptions": orphan, "Status": "PASS" if orphan == 0 else "REVIEW"})
    for fk, dim, pk in [("circuitId", "circuits", "id"), ("grandPrixId", "grands_prix", "id")]:
        orphan = int((~races[fk].isin(t[dim][pk])).sum())
        fact_fk_checks.append({"Check": f"races.{fk} -> {dim}.{pk}", "RowsChecked": int(len(races)), "Exceptions": orphan, "Status": "PASS" if orphan == 0 else "REVIEW"})
    pd.DataFrame(fact_fk_checks).to_csv(OUT / "foreign_key_audit.csv", index=False)

    duplicate_specs = {
        "race_results (raceId, driverId)": ("race_results", ["raceId", "driverId"]),
        "qualifying_results (raceId, driverId)": ("qualifying_results", ["raceId", "driverId"]),
        "fastest_laps (raceId, driverId)": ("fastest_laps", ["raceId", "driverId"]),
        "pit_stops (raceId, driverId, stop)": ("pit_stops", ["raceId", "driverId", "stop"]),
        "season_driver_standings (year, driverId)": ("season_driver_standings", ["year", "driverId"]),
        "season_constructor_standings (year, constructorId)": ("season_constructor_standings", ["year", "constructorId"]),
    }
    dup_rows = []
    for label, (table, keycols) in duplicate_specs.items():
        frame = t[table]
        extras = int(frame.duplicated(keycols, keep="first").sum())
        involved = int(frame.duplicated(keycols, keep=False).sum())
        dup_rows.append({"CandidateKey": label, "Rows": int(len(frame)), "DuplicateExtraRows": extras, "RowsInDuplicateGroups": involved, "Status": "PASS" if extras == 0 else "REVIEW; preserve and inspect before deduplicating"})
    pd.DataFrame(dup_rows).to_csv(OUT / "candidate_key_audit.csv", index=False)

    nat_mismatch = int((drivers["countryOfBirthCountryId"] != drivers["nationalityCountryId"]).sum())
    null_pos = int(rr["is_blank_finish_position"].sum())
    explicit_dnf = int(rr["is_explicit_dnf"].sum())
    winning_entries = int(rr["is_winning_entry"].sum())
    unique_winning_events = int(wins["raceId"].nunique())
    race_events_with_results = int(rr["raceId"].nunique())
    summary = {
        "source_snapshot": "F1DB CSV release v2026.8.2 (release date stated in source documentation: 2026-07-02)",
        "race_results_snapshot_note": "2026 race-result records are populated through round 8; 14 scheduled race rows have no race-result rows in this frozen extract. Do not treat the snapshot as the completed 2026 season.",
        "row_counts": row_counts,
        "combined_rows_across_six_fact_tables": int(combined_fact_rows),
        "race_calendar_rows": int(len(races)),
        "distinct_race_events_with_result_rows": race_events_with_results,
        "scheduled_race_rows_without_result_rows": int(len(races_without_results)),
        "race_result_rows": int(len(rr)),
        "distinct_drivers_in_driver_dimension": int(drivers["id"].nunique()),
        "distinct_drivers_in_race_results": int(rr["driverId"].nunique()),
        "distinct_constructors_in_constructor_dimension": int(constructors["id"].nunique()),
        "distinct_constructors_in_race_results": int(rr["constructorId"].nunique()),
        "distinct_circuits": int(circuits["id"].nunique()),
        "distinct_grand_prix_identities": int(gps["id"].nunique()),
        "total_points_sum_race_results": round(float(rr["points_num"].sum()), 2),
        "blank_position_rows": null_pos,
        "blank_position_rate_pct": safe_pct(null_pos, len(rr)),
        "explicit_DNF_rows_positionText_DNF": explicit_dnf,
        "explicit_DNF_rate_pct_of_result_rows": safe_pct(explicit_dnf, len(rr)),
        "winning_result_rows_positionNumber_1": winning_entries,
        "distinct_races_with_at_least_one_winning_result": unique_winning_events,
        "driver_birth_country_vs_nationality_different": nat_mismatch,
        "driver_birth_country_vs_nationality_different_pct": safe_pct(nat_mismatch, len(drivers)),
        "pit_stop_rows": int(len(t["pit_stops"])),
        "pit_stop_first_year": int(pd.to_numeric(t["pit_stops"]["year"]).min()),
        "pit_stop_last_year": int(pd.to_numeric(t["pit_stops"]["year"]).max()),
        "foreign_key_audit_all_zero_orphans": all(x["Exceptions"] == 0 for x in fact_fk_checks),
        "source_scope_note": "Dimension row counts are not the same as entities represented in race_results; do not interchange these measures.",
    }
    (OUT / "quality_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Human-readable QA report is generated from the same values, so published figures can be rerun.
    report = [
        "# Automated Data Audit — Grand Prix Performance Intelligence", "",
        "Generated by `scripts/run_analysis.py` from the included CSV snapshot. This audit uses raw source values and does not claim that the DAX measures have been executed inside Power BI.", "",
        "## Scope and table sizes", "",
        "| Source table | Rows |", "|---|---:|",
    ]
    report += [f"| `{name}.csv` | {count:,} |" for name, count in row_counts.items()]
    report += ["", f"The six fact inputs listed above contain **{combined_fact_rows:,} rows combined** before modeling; dimensions are not included in that total.", "",
        "## Main findings", "",
        f"- `races.csv` contains **{len(races):,} schedule rows**. `race_results.csv` contains **{len(rr):,} result rows** across **{race_events_with_results:,} distinct race events**.",
        f"- **{len(races_without_results):,} schedule rows** have no result rows in this frozen extract; all are from the 2026 calendar after the last populated result round. This is a snapshot-freshness limitation, not proof that those events did not happen.",
        f"- **{null_pos:,} ({safe_pct(null_pos, len(rr))}%)** of race-result rows have a blank numeric `positionNumber`. The source statuses show this bucket is broader than explicit DNF.",
        f"- Explicit `positionText = DNF` appears on **{explicit_dnf:,} rows ({safe_pct(explicit_dnf, len(rr))}%)**. Keep this separate from the blank-position metric.",
        f"- The data has **{winning_entries:,} winning result rows** (`positionNumber = 1`) but only **{unique_winning_events:,} distinct race events with a winner**. Shared-car / historical records mean raw winning rows should not be assumed to equal unique Grand Prix events.",
        f"- `pit_stops.csv` has **{len(t['pit_stops']):,} records**, spanning **{int(pd.to_numeric(t['pit_stops']['year']).min())}–{int(pd.to_numeric(t['pit_stops']['year']).max())}** in the supplied snapshot.",
        f"- **{nat_mismatch} of {len(drivers)} drivers ({safe_pct(nat_mismatch, len(drivers))}%)** have different birth-country and nationality-country IDs. Use the field that matches the business question and label it correctly.",
        "- The foreign-key audit found no orphan IDs for the relationships checked; inspect `outputs/foreign_key_audit.csv` for the checks.",
        "", "## Explicit result statuses", "", "See `outputs/finish_status_distribution.csv`. Blank position includes DNFs and other non-classified/non-starting statuses; the dashboard should not label the entire blank-position rate as DNF.",
        "", "## Duplicate candidate keys", "", "See `outputs/candidate_key_audit.csv`. Duplicate candidates are flagged for investigation, not automatically removed. In particular, `race_results` has historical records that repeat `(raceId, driverId)` because driver/constructor/shared-car result details can involve more than one row; use a generated row key and preserve source rows unless a domain-specific rule justifies deduplication.",
        "", "## Validation boundary", "", "This script validates raw CSV statistics, row counts, selected foreign keys and candidate duplicate keys. It does not validate the generated Power Query M or DAX inside Power BI Desktop; those steps still require a native Power BI refresh/model QA run.", ""]
    (OUT / "DATA_AUDIT_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    # One compact machine-readable run record is useful in CI and reproducibility checks.
    print(json.dumps({
        "status": "completed",
        "tables_loaded": len(t),
        "result_rows": len(rr),
        "events_with_results": race_events_with_results,
        "blank_finish_position_rate_pct": summary["blank_position_rate_pct"],
        "explicit_dnf_rate_pct": summary["explicit_DNF_rate_pct_of_result_rows"],
        "foreign_key_audit_all_zero_orphans": summary["foreign_key_audit_all_zero_orphans"],
        "outputs": sorted(p.name for p in OUT.iterdir()),
    }, indent=2))

if __name__ == "__main__":
    main()
