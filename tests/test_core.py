"""gradetool 的单元测试。

运行方式：python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gradetool.core import (  # noqa: E402
    count,
    gpa,
    grade_distribution,
    letter_of,
    mean,
    median,
    parse_scores,
    pass_rate,
    point_of,
    spread,
    std_dev,
    summarize,
)


class ParseScoresTest(unittest.TestCase):
    def test_accepts_mixed_separators(self):
        self.assertEqual(parse_scores("90, 85 70\n100"), [90.0, 85.0, 70.0, 100.0])

    def test_empty_input_gives_empty_list(self):
        self.assertEqual(parse_scores("   \n  "), [])

    def test_ignores_non_numeric_tokens(self):
        self.assertEqual(parse_scores("90 缺考 85"), [90.0, 85.0])

    def test_accepts_decimals(self):
        self.assertEqual(parse_scores("88.5 91.25"), [88.5, 91.25])


class StatisticsTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count([1, 2, 3]), 3)
        self.assertEqual(count([]), 0)

    def test_mean(self):
        self.assertAlmostEqual(mean([90, 80, 70]), 80.0)

    def test_mean_of_empty_list_is_zero(self):
        self.assertAlmostEqual(mean([]), 0.0)

    def test_median_of_odd_list(self):
        self.assertAlmostEqual(median([3, 1, 2]), 2.0)

    def test_median_ignores_input_order(self):
        self.assertAlmostEqual(median([100, 70, 90, 85]), median([70, 85, 90, 100]))

    def test_median_of_even_list_takes_average_of_two_middle(self):
        self.assertAlmostEqual(median([70, 85, 90, 100]), 87.5)
        self.assertAlmostEqual(median([60, 80]), 70.0)

    def test_spread(self):
        self.assertEqual(spread([90, 60, 75]), (60, 90))

    def test_std_dev_matches_hand_calculation(self):
        # 均值 3，偏差平方和 8，总体方差 8/3，标准差约 1.632993
        self.assertAlmostEqual(std_dev([1, 3, 5]), (8 / 3) ** 0.5)

    def test_summarize_keys(self):
        stats = summarize([90, 80])
        for key in ("count", "mean", "median", "min", "max", "std"):
            self.assertIn(key, stats)


class PassRateTest(unittest.TestCase):
    def test_all_passed(self):
        self.assertAlmostEqual(pass_rate([90, 80, 60]), 1.0)

    def test_half_passed(self):
        self.assertAlmostEqual(pass_rate([90, 80, 50, 40]), 0.5)

    def test_boundary_score_counts_as_passed(self):
        self.assertAlmostEqual(pass_rate([60, 59]), 0.5)

    def test_empty_list_is_zero(self):
        self.assertAlmostEqual(pass_rate([]), 0.0)

    def test_custom_pass_line(self):
        self.assertAlmostEqual(pass_rate([90, 80, 70], pass_line=75), 2 / 3)


class GradeTest(unittest.TestCase):
    def test_letter_boundaries(self):
        self.assertEqual(letter_of(90), "A")
        self.assertEqual(letter_of(89.9), "B")
        self.assertEqual(letter_of(80), "B")
        self.assertEqual(letter_of(70), "C")
        self.assertEqual(letter_of(60), "D")
        self.assertEqual(letter_of(59.9), "F")
        self.assertEqual(letter_of(0), "F")

    def test_point_boundaries(self):
        self.assertAlmostEqual(point_of(95), 4.0)
        self.assertAlmostEqual(point_of(85), 3.0)
        self.assertAlmostEqual(point_of(65), 1.0)
        self.assertAlmostEqual(point_of(30), 0.0)

    def test_gpa_average(self):
        # 95→4.0，85→3.0，平均 3.5
        self.assertAlmostEqual(gpa([95, 85]), 3.5)

    def test_gpa_of_empty_list_is_zero(self):
        self.assertAlmostEqual(gpa([]), 0.0)

    def test_distribution_counts_every_grade(self):
        buckets = grade_distribution([95, 92, 85, 75, 65, 50])
        self.assertEqual(buckets["A"], 2)
        self.assertEqual(buckets["B"], 1)
        self.assertEqual(buckets["C"], 1)
        self.assertEqual(buckets["D"], 1)
        self.assertEqual(buckets["F"], 1)

    def test_distribution_keeps_zero_buckets(self):
        buckets = grade_distribution([95])
        self.assertEqual(buckets["F"], 0)
        self.assertEqual(len(buckets), 5)


class SummarizeTest(unittest.TestCase):
    def test_includes_grade_fields_by_default(self):
        stats = summarize([95, 85, 65])
        self.assertIn("pass_rate", stats)
        self.assertIn("gpa", stats)
        self.assertIn("grades", stats)
        self.assertAlmostEqual(stats["pass_line"], 60.0)

    def test_can_turn_grade_fields_off(self):
        stats = summarize([95, 85], with_grade=False)
        self.assertNotIn("pass_rate", stats)
        self.assertNotIn("gpa", stats)

    def test_custom_pass_line_is_reported(self):
        stats = summarize([95, 85, 65], pass_line=80)
        self.assertAlmostEqual(stats["pass_line"], 80.0)
        self.assertAlmostEqual(stats["pass_rate"], 2 / 3)

    def test_custom_pass_line_affects_distribution_summary(self):
        # 及格线提到 80 后，80 分以下都不算及格，这个用例可以防止 pass_line 被中途丢掉
        stats = summarize([95, 85, 75, 65], pass_line=80)
        self.assertAlmostEqual(stats["pass_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
