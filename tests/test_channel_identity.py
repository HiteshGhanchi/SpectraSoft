import unittest

from core.analysis.channel_identity import (
    channel_display_name,
    channel_result_key,
    normalized_channel_rows,
)
from core.analysis.analysis_worker import AnalysisWorker


class ChannelIdentityTests(unittest.TestCase):
    def test_ar_number_is_the_stable_result_identity(self):
        entry = {"ar_no": 7, "itg": "12", "ele": "FE", "name": ""}

        self.assertEqual(channel_result_key(entry), "AR:7")
        self.assertEqual(channel_display_name(entry), "FE")

    def test_same_element_on_two_analytical_rows_gets_two_keys(self):
        rows = normalized_channel_rows(
            [
                {"itg": "3", "ele": "FE", "seq": "1"},
                {"itg": "8", "ele": "FE", "seq": "2"},
            ]
        )

        self.assertEqual([channel_result_key(row) for row in rows], ["AR:1", "AR:2"])
        self.assertEqual([channel_display_name(row) for row in rows], ["FE", "FE"])

    def test_ise_ratio_resolves_reference_by_itg_without_collapsing_ar_rows(self):
        worker = AnalysisWorker(group_id=1)
        worker._group_data = {
            "page_03_channel": [
                {"ar_no": 1, "itg": "3", "ele": "FE", "ise_ref": 8},
                {"ar_no": 2, "itg": "8", "ele": "FE", "ise_ref": 0},
            ]
        }

        result = worker._apply_ise_ratio({"AR:1": 100, "AR:2": 200})

        self.assertAlmostEqual(result["AR:1"], 50.0)
        self.assertAlmostEqual(result["AR:2"], 200 / 4095)

    def test_channel_results_expose_value_with_ar_and_itg_metadata(self):
        worker = AnalysisWorker(group_id=1)

        records = worker._channel_results(
            [
                {"ar_no": 1, "itg": "3", "ele": "FE", "name": "IRON"},
                {"ar_no": 2, "itg": "8", "ele": "FE", "name": "IRON"},
            ],
            {"AR:1": 100, "AR:2": 200},
            {"AR:1": 0.1, "AR:2": 0.2},
        )

        self.assertEqual([record["ar_no"] for record in records], [1, 2])
        self.assertEqual([record["itg"] for record in records], ["3", "8"])
        self.assertEqual([record["intensity"] for record in records], [0.1, 0.2])


if __name__ == "__main__":
    unittest.main()
