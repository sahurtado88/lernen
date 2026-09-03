#!/usr/bin/env python3
"""
Tests unitarios para dora.py.
Mockean la GitHub API — no requieren token ni conexión a internet.

Ejecutar:
    cd DORA
    python -m pytest tests/test_metrics.py -v
    # o sin pytest:
    python tests/test_metrics.py
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import dora
from tests.fixtures import (
    WORKFLOW_RUNS, MERGED_PRS, PR_COMMITS, INCIDENTS, EXPECTED, days_ago
)

CFG = {
    "github_token": "ghp_fake_token",
    "owner":        "test-org",
    "repo":         "test-repo",
    "production_workflows": ["deploy prod", "despliegue prod", "despliegue automatizado"],
    "incident_label": "incident",
    "days": 90,
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_since(days=90):
    return datetime.now(timezone.utc) - timedelta(days=days)


# ─── dora_level ───────────────────────────────────────────────────────────────

class TestDoraLevel(unittest.TestCase):

    def test_df_elite(self):
        level, color = dora.dora_level("df", 10)
        self.assertEqual(level, "Elite")
        self.assertEqual(color, "#22c55e")

    def test_df_high(self):
        level, _ = dora.dora_level("df", 3)
        self.assertEqual(level, "High")

    def test_df_medium(self):
        level, _ = dora.dora_level("df", 0.5)
        self.assertEqual(level, "Medium")

    def test_df_low(self):
        level, _ = dora.dora_level("df", 0.1)
        self.assertEqual(level, "Low")

    def test_lt_elite(self):
        level, _ = dora.dora_level("lt", 0.5)
        self.assertEqual(level, "Elite")

    def test_lt_high(self):
        level, _ = dora.dora_level("lt", 12)
        self.assertEqual(level, "High")

    def test_lt_medium(self):
        level, _ = dora.dora_level("lt", 72)
        self.assertEqual(level, "Medium")

    def test_lt_low(self):
        level, _ = dora.dora_level("lt", 300)
        self.assertEqual(level, "Low")

    def test_mttr_elite(self):
        level, _ = dora.dora_level("mttr", 0.75)
        self.assertEqual(level, "Elite")

    def test_cfr_elite(self):
        level, _ = dora.dora_level("cfr", 3)
        self.assertEqual(level, "Elite")

    def test_cfr_medium(self):
        level, _ = dora.dora_level("cfr", 12)
        self.assertEqual(level, "Medium")

    def test_cfr_low(self):
        level, _ = dora.dora_level("cfr", 20)
        self.assertEqual(level, "Low")


# ─── fmt_hours ────────────────────────────────────────────────────────────────

class TestFmtHours(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(dora.fmt_hours(0), "N/A")

    def test_minutes(self):
        self.assertEqual(dora.fmt_hours(0.5), "30m")

    def test_hours(self):
        self.assertEqual(dora.fmt_hours(6), "6.0h")

    def test_days(self):
        self.assertEqual(dora.fmt_hours(48), "2.0d")


# ─── Deployment Frequency ─────────────────────────────────────────────────────

class TestDeploymentFrequency(unittest.TestCase):

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=[])
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_total_deploys(self, *_):
        m = dora.calculate(CFG)
        self.assertEqual(m["df"]["total"], EXPECTED["df_total"])

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=[])
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_avg_per_week(self, *_):
        m = dora.calculate(CFG)
        self.assertAlmostEqual(m["df"]["avg_per_week"], EXPECTED["df_avg_per_week_approx"], delta=0.1)

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=[])
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_level_high(self, *_):
        m = dora.calculate(CFG)
        level, _ = dora.dora_level("df", m["df"]["avg_per_week"])
        self.assertEqual(level, EXPECTED["df_level"])

    @patch("dora.fetch_workflow_runs", return_value=[])
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=[])
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_zero_deploys(self, *_):
        m = dora.calculate(CFG)
        self.assertEqual(m["df"]["total"], 0)
        self.assertEqual(m["df"]["avg_per_week"], 0.0)


# ─── MTTR ─────────────────────────────────────────────────────────────────────

class TestMTTR(unittest.TestCase):

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_avg_mttr(self, *_):
        m = dora.calculate(CFG)
        self.assertAlmostEqual(m["mttr"]["avg_hours"], EXPECTED["mttr_avg_hours_approx"], delta=1)

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_resolved_count(self, *_):
        m = dora.calculate(CFG)
        self.assertEqual(m["mttr"]["resolved"], 2)
        self.assertEqual(m["mttr"]["total"], 2)

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=[])
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_no_incidents(self, *_):
        m = dora.calculate(CFG)
        self.assertEqual(m["mttr"]["avg_hours"], 0)
        self.assertEqual(m["mttr"]["total"], 0)


# ─── Change Failure Rate ──────────────────────────────────────────────────────

class TestCFR(unittest.TestCase):

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_cfr_calculation(self, *_):
        m = dora.calculate(CFG)
        self.assertAlmostEqual(m["cfr"]["rate"], EXPECTED["cfr_rate_approx"], delta=0.5)

    @patch("dora.fetch_workflow_runs", return_value=[])
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_cfr_no_deploys(self, *_):
        m = dora.calculate(CFG)
        self.assertEqual(m["cfr"]["rate"], 0)

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=[])
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_cfr_no_incidents(self, *_):
        m = dora.calculate(CFG)
        self.assertEqual(m["cfr"]["rate"], 0.0)
        self.assertEqual(m["cfr"]["incidents"], 0)


# ─── HTML generation ──────────────────────────────────────────────────────────

class TestHTMLGeneration(unittest.TestCase):

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=MERGED_PRS)
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", side_effect=lambda cfg, n: datetime.fromisoformat(
        PR_COMMITS.get(n, days_ago(10)).replace("Z", "+00:00")
    ))
    def test_html_contains_repo(self, *_):
        m = dora.calculate(CFG)
        html = dora.build_html(m)
        self.assertIn("test-org/test-repo", html)

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_html_contains_all_metrics(self, *_):
        m = dora.calculate(CFG)
        html = dora.build_html(m)
        for section in ["Deployment Frequency", "Lead Time", "MTTR", "Change Failure Rate"]:
            self.assertIn(section, html)

    @patch("dora.fetch_workflow_runs", return_value=WORKFLOW_RUNS)
    @patch("dora.fetch_merged_prs",    return_value=[])
    @patch("dora.fetch_incidents",     return_value=INCIDENTS)
    @patch("dora.fetch_pr_first_commit", return_value=None)
    def test_html_is_valid_structure(self, *_):
        m = dora.calculate(CFG)
        html = dora.build_html(m)
        self.assertTrue(html.strip().startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", html)
        self.assertIn("chart.js", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
