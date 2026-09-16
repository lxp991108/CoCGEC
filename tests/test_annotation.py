import unittest

from cocgec.annotation import (
    annotate_record,
    char_error_range,
    clause_error_range,
    error_range,
    word_error_range,
)


class AnnotationTests(unittest.TestCase):
    def test_char_level(self):
        source = "我们及时解决和发现问题。"
        reference = "我们及时发现和解决问题。"
        self.assertEqual(char_error_range(source, [reference]), "解决和发现")

    def test_word_level_with_injected_tokenizer(self):
        source = "这个地区的雨季很特别，90%都集中在七八两个月。"
        reference = "这个地区的雨季很特别，90%的雨季都集中在七八两个月。"
        tokens = ["这个", "地区", "的", "雨季", "很", "特别", "，", "90%", "都", "集中", "在", "七八", "两个", "月", "。"]
        self.assertEqual(
            word_error_range(source, [reference], tokenizer=lambda _: tokens), "90%都"
        )

    def test_clause_level(self):
        source = "前半句正确，主要原因是负担重、活动少造成的。"
        reference = "前半句正确，主要原因是负担重、活动少。"
        self.assertEqual(
            clause_error_range(source, [reference]), "主要原因是负担重、活动少造成的"
        )

    def test_auto_mapping_and_no_error(self):
        source = "我们及时解决和发现问题。"
        reference = "我们及时发现和解决问题。"
        self.assertEqual(error_range(source, [reference], "语序不当"), "我们及时解决和发现问题")
        record = {
            "sentence": "正确句子。",
            "corrected_sentence": ["正确句子。"],
            "error_flag": 0,
            "error_type": "没有语病",
        }
        self.assertNotIn("error_range", annotate_record(record))

    def test_identical_references_do_not_crash(self):
        self.assertEqual(char_error_range("正确句子。", ["正确句子。"]), "")


if __name__ == "__main__":
    unittest.main()
