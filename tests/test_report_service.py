import csv
import io
import unittest
from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup
from core.persistence.result_repository import file_analysis_result
from core.analysis.report_service import (
    ReportFilters,
    analytical_frequency,
    build_histogram,
    daily_report,
    export_results_csv,
    filter_results,
    result_detail,
    stability_report,
    summarize_values,
    x_r_report,
)


class ReportServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        group = AnalyticalGroup(name="STEEL")
        self.session.add(group)
        self.session.commit()
        self.group_id = group.id
        self.results = []
        for index, (sample, job, value, when, product) in enumerate(
            [
                ("A-1", "X", 10.0, datetime(2026, 1, 1, 8), "P-1"),
                ("A-1", "Y", 12.0, datetime(2026, 1, 1, 9), "P-1"),
                ("B-1", "X", 14.0, datetime(2026, 1, 2, 8), "P-2"),
                ("C-1", "X", 16.0, datetime(2026, 1, 3, 8), "P-2"),
            ]
        ):
            result = file_analysis_result(
                self.session,
                self.group_id,
                job,
                sample,
                [{"FE": value - 1}, {"FE": value + 1}],
                {"FE": value},
                {"FE": value},
                {"FE": "OK"},
                {"product_name": product, "method": {"curve": "v1"}},
            )
            result.occurred_at = when
            self.results.append(result)
        self.session.commit()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_filters_results_by_date_sample_and_job(self):
        filters = ReportFilters(
            start=datetime(2026, 1, 1),
            end=datetime(2026, 1, 2, 23, 59, 59),
            sample_name="A-1",
            job="x",
        )
        filtered = filter_results(self.results, filters)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].final_concentrations["FE"], 10.0)

    def test_daily_modes_group_by_expected_identity(self):
        self.assertEqual([row["key"] for row in daily_report(self.results, "group")], ["2026-01-01", "2026-01-02", "2026-01-03"])
        self.assertEqual([row["key"] for row in daily_report(self.results, "product")], ["P-1", "P-2"])
        self.assertEqual([row["key"] for row in daily_report(self.results, "sample")], ["A-1", "B-1", "C-1"])

    def test_statistics_and_histogram_only_calculate_capability_indices_with_valid_limits(self):
        summary = summarize_values([10, 12, 14, 16], lower_limit=8, upper_limit=18)
        self.assertEqual(summary["count"], 4)
        self.assertAlmostEqual(summary["average"], 13.0)
        self.assertIsNotNone(summary["cp"])
        self.assertIsNotNone(summary["cpk"])
        unavailable = summarize_values([10, 12, 14, 16])
        self.assertIsNone(unavailable["cp"])
        self.assertIsNone(unavailable["cpk"])
        histogram = build_histogram([10, 12, 14, 16], lower_limit=8, upper_limit=18, bins=5)
        self.assertEqual(sum(histogram["counts"]), 4)
        self.assertEqual(histogram["under_limit"], 0)
        self.assertEqual(histogram["over_limit"], 0)

    def test_xr_stability_frequency_and_detail_are_real_data(self):
        xr = x_r_report(self.results, "FE")
        self.assertEqual(len(xr["points"]), 4)
        self.assertEqual(xr["points"][0]["count"], 2)
        self.assertEqual(xr["points"][0]["xbar"], 10)
        self.assertEqual(xr["points"][0]["range"], 2)
        stability = stability_report(self.results, "FE")
        self.assertEqual(stability["count"], 4)
        self.assertEqual(stability["maximum"], 16.0)
        self.assertAlmostEqual(stability["average"], 13.0)
        frequency = analytical_frequency(self.results)
        self.assertEqual(frequency["total"], 4)
        self.assertEqual(frequency["by_job"], {"X": 3, "Y": 1})
        detail = result_detail(self.results[0])
        self.assertEqual(detail["burns"][0]["FE"], 9.0)
        self.assertEqual(detail["method_snapshot"]["method"]["curve"], "v1")
        self.assertEqual(detail["flags"]["FE"], "OK")

    def test_csv_export_contains_burn_and_method_detail(self):
        content = export_results_csv(self.results[:1], include_details=True)
        rows = list(csv.DictReader(io.StringIO(content)))
        self.assertEqual(rows[0]["sample_name"], "A-1")
        self.assertIn('"FE": 9.0', rows[0]["burns"])
        self.assertIn("curve", rows[0]["method_snapshot"])

    def test_reporting_day_uses_seven_am_boundary_and_inclusive_end_date(self):
        self.results[0].occurred_at = datetime(2026, 1, 2, 6, 59)
        self.results[1].occurred_at = datetime(2026, 1, 2, 7)
        selected = filter_results(self.results, ReportFilters(start=date(2026, 1, 1), end=date(2026, 1, 1)))
        self.assertEqual([row.id for row in selected], [self.results[0].id])
        self.assertEqual(daily_report(selected)[0]["day"], "2026-01-01")
        with self.assertRaises(ValueError):
            filter_results(self.results, ReportFilters(start=date(2026, 1, 3), end=date(2026, 1, 1)))

    def test_missing_nonfinite_and_single_values_are_not_fabricated(self):
        self.results[0].final_concentrations = {}
        self.results[1].final_concentrations = {"FE": "bad"}
        self.results[2].final_concentrations = {"FE": float("nan")}
        report = stability_report(self.results, "FE")
        self.assertEqual(report["count"], 1)
        self.assertEqual(report["points"][0]["result"].id, self.results[3].id)
        self.assertIsNone(report["stddev"])
        self.assertIsNone(summarize_values([1, 1], 0, 2)["cp"])
        self.assertEqual(summarize_values([12, 14], 0, 10)["cpk"], 0)
        self.assertEqual(summarize_values([1, 2, 3])["stddev"], 1)
        for limits in [(2, 1), (None, 1), (0, float("inf"))]:
            with self.assertRaises(ValueError):
                summarize_values([1, 2], *limits)

    def test_histogram_includes_all_tails_and_handles_constant_and_empty_data(self):
        histogram = build_histogram([-1, 0, 1, 2, 3, "bad", float("inf")], 0, 2, bins=3)
        self.assertEqual(sum(histogram["counts"]), 5)
        self.assertEqual(histogram["under_limit"], 1)
        self.assertEqual(histogram["over_limit"], 1)
        self.assertEqual(sum(build_histogram([2, 2])["counts"]), 2)
        self.assertEqual(sum(build_histogram([])["counts"]), 0)

    def test_xr_does_not_invent_range_for_single_burn_or_combine_methods(self):
        self.results[0].burns = [{"FE": 10}]
        report = x_r_report(self.results, "FE")
        self.assertIsNone(report["points"][0]["range"])
        self.assertNotEqual(report["points"][0]["series"], report["points"][1]["series"])
        self.assertEqual(report["points"][0]["result"].id, self.results[0].id)


if __name__ == "__main__":
    unittest.main()
