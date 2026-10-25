import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup, AnalysisResult
from core.persistence.result_repository import (
    file_analysis_result,
    list_analysis_results,
    summarize_results,
)


class ResultRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        group = AnalyticalGroup(name="STEEL")
        self.session.add(group)
        self.session.commit()
        self.group_id = group.id

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_files_complete_result_with_method_snapshot(self):
        result = file_analysis_result(
            self.session,
            self.group_id,
            "X",
            "SAMPLE-1",
            [{"FE": 10.0, "C": 2.0}, {"FE": 11.0, "C": 2.1}],
            {"FE": 10.5, "C": 2.05},
            {"FE": 10.5, "C": 2.05},
            {"FE": "OK", "C": "OK"},
            {"page_05_wc": {"FE": {"a": 0, "b": 0, "c": 1, "d": 0}}},
        )

        self.assertEqual(result.job, "X")
        self.assertEqual(result.sample_name, "SAMPLE-1")
        self.assertEqual(len(list_analysis_results(self.session, self.group_id)), 1)
        self.assertEqual(result.method_snapshot["page_05_wc"]["FE"]["c"], 1)

    def test_summary_calculates_count_average_and_range(self):
        for sample, value in [("A", 10.0), ("B", 14.0)]:
            file_analysis_result(
                self.session,
                self.group_id,
                "X",
                sample,
                [{"FE": value}],
                {"FE": value},
                {"FE": value},
                {},
                {},
            )

        summary = summarize_results(self.session, self.group_id, "FE")
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["average"], 12.0)
        self.assertEqual(summary["range"], 4.0)


if __name__ == "__main__":
    unittest.main()
