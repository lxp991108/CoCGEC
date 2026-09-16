import unittest

from cocgec.instructions import build_two_stage

RECORDS = [
    {
        "id": str(index),
        "sentence": f"病句{index}",
        "corrected_sentence": [f"改句{index}a", f"改句{index}b"],
        "error_flag": 1,
        "error_type": "语序不当",
        "error_range": f"病句{index}",
    }
    for index in range(10)
]


class InstructionTests(unittest.TestCase):
    def test_reproducible_and_expected_size(self):
        first = build_two_stage(RECORDS, seed=7)
        second = build_two_stage(RECORDS, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 12)  # 9 correction + 1 * 3 CoTasks

    def test_ratio_validation(self):
        with self.assertRaises(ValueError):
            build_two_stage(RECORDS, stage_two_ratio=1.1)

    def test_stage_two_uses_paper_floor_rule(self):
        records = RECORDS + [{**RECORDS[0], "id": "extra"}]
        result = build_two_stage(records, stage_two_ratio=0.1, seed=7)
        self.assertEqual(len(result), 13)  # 10 correction + floor(1.1) * 3


if __name__ == "__main__":
    unittest.main()
