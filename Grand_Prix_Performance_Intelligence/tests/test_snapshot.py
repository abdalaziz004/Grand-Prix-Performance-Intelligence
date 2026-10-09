"""Smoke tests for the frozen CSV snapshot and generated portfolio outputs."""
from pathlib import Path
import json
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = json.loads((OUT / "quality_summary.json").read_text(encoding="utf-8"))

    def test_expected_source_scope(self):
        self.assertEqual(len(self.summary["row_counts"]), 12)
        self.assertEqual(self.summary["row_counts"]["race_results"], 27467)
        self.assertEqual(self.summary["race_calendar_rows"], 1171)
        self.assertEqual(self.summary["distinct_race_events_with_result_rows"], 1157)

    def test_finish_status_definitions_are_separate(self):
        self.assertAlmostEqual(self.summary["blank_position_rate_pct"], 39.67, places=2)
        self.assertAlmostEqual(self.summary["explicit_DNF_rate_pct_of_result_rows"], 31.88, places=2)
        self.assertNotEqual(self.summary["blank_position_rows"], self.summary["explicit_DNF_rows_positionText_DNF"])

    def test_reference_relationships_have_no_orphans(self):
        audit = pd.read_csv(OUT / "foreign_key_audit.csv")
        self.assertTrue((audit["Exceptions"] == 0).all())
        self.assertTrue(self.summary["foreign_key_audit_all_zero_orphans"])

    def test_dominant_2023_constructor_share(self):
        df = pd.read_csv(OUT / "constructor_win_share_by_season.csv")
        row = df[(df["Year"] == 2023) & (df["Constructor"] == "Red Bull")]
        self.assertEqual(len(row), 1)
        self.assertEqual(int(row.iloc[0]["RaceWins"]), 21)
        self.assertEqual(int(row.iloc[0]["EventsWithResult"]), 22)
        self.assertAlmostEqual(float(row.iloc[0]["WinSharePct"]), 95.45, places=2)

    def test_missing_2026_result_rows_are_documented(self):
        missing = pd.read_csv(OUT / "scheduled_races_without_result_rows.csv")
        self.assertEqual(len(missing), 14)
        self.assertTrue((missing["year"] == 2026).all())

if __name__ == "__main__":
    unittest.main(verbosity=2)
