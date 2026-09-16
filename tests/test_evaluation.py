import unittest

from cocgec.evaluation import exact_match, parse_prediction, to_fcgec_submission


class EvaluationTests(unittest.TestCase):
    def test_parse_prediction(self):
        self.assertEqual(parse_prediction("原句。", "没有语病"), "原句。")
        self.assertEqual(parse_prediction("病句。", "正确的句子：改句。"), "改句。")
        self.assertEqual(
            parse_prediction("病句。", "分析文字\n正确的句子：改句。\n补充解释"),
            "改句。",
        )

    def test_exact_match_checks_lengths(self):
        with self.assertRaises(ValueError):
            exact_match([], ["extra"])

    def test_submission_is_deterministic(self):
        gold = [{"id": "x", "sentence": "病句。"}]
        expected = {
            "x": {"error_flag": 1, "error_type": "IWO", "correction": "改句。"}
        }
        self.assertEqual(to_fcgec_submission(gold, ["改句。"], ["IWO"]), expected)

    def test_submission_refuses_fabricated_types(self):
        with self.assertRaises(ValueError):
            to_fcgec_submission([{"sentence": "病句。"}], ["改句。"])


if __name__ == "__main__":
    unittest.main()
