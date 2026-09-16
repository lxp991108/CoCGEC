import json
import unittest
from pathlib import Path

from cocgec.annotation import annotate_record

RELEASE_DATA = Path(__file__).parents[1] / "data" / "CoCGEC_train.json"


@unittest.skipUnless(RELEASE_DATA.exists(), "released CoCGEC data is not present")
class ReleaseCompatibilityTests(unittest.TestCase):
    def test_all_published_error_ranges(self):
        records = json.loads(RELEASE_DATA.read_text(encoding="utf-8"))
        error_records = [record for record in records if record["error_flag"] == 1]

        self.assertEqual(len(records), 36_266)
        self.assertEqual(len(error_records), 19_710)
        for record in error_records:
            with self.subTest(sentence=record["sentence"]):
                self.assertEqual(
                    annotate_record(record)["error_range"], record["error_range"]
                )
