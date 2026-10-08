"""gradetool 的单元测试。

运行方式：python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gradetool.core import (  # noqa: E402
    count,
    mean,
    median,
    parse_scores,
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

    def test_spread(self):
        self.assertEqual(spread([90, 60, 75]), (60, 90))

    def test_std_dev_matches_hand_calculation(self):
        # 均值 3，偏差平方和 8，总体方差 8/3，标准差约 1.632993
        self.assertAlmostEqual(std_dev([1, 3, 5]), (8 / 3) ** 0.5)

    def test_summarize_keys(self):
        stats = summarize([90, 80])
        for key in ("count", "mean", "median", "min", "max", "std"):
            self.assertIn(key, stats)


if __name__ == "__main__":
    unittest.main()
