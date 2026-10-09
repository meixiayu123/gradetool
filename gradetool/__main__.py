"""gradetool 的命令行入口。

用法示例：
    python -m gradetool 90 85 70 100
    python -m gradetool --file scores.txt
    type scores.txt | python -m gradetool
    python -m gradetool --pass-line 70 90 85 70
    python -m gradetool --json 90 85 70
"""

import argparse
import json
import sys

from .core import parse_scores, summarize

GRADE_ORDER = ("A", "B", "C", "D", "F")


def read_text(args):
    """按优先级决定从哪里读取原始分数文本：命令行 > 文件 > 标准输入。"""
    if args.scores:
        return " ".join(args.scores)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            return fh.read()
    return sys.stdin.read()


def render_text(stats):
    """默认的表格化输出。"""
    lines = [
        "成绩统计结果",
        "=" * 28,
        "人数   : %d" % stats["count"],
        "平均分 : %.2f" % stats["mean"],
        "中位数 : %.2f" % stats["median"],
        "最低分 : %.2f" % stats["min"],
        "最高分 : %.2f" % stats["max"],
        "标准差 : %.2f" % stats["std"],
    ]
    if "pass_rate" in stats:
        lines.append("-" * 28)
        lines.append("及格线 : %.0f" % stats["pass_line"])
        lines.append("及格率 : %.1f%%" % (stats["pass_rate"] * 100))
        lines.append("平均绩点 : %.2f" % stats["gpa"])
        detail = "  ".join(
            "%s:%d" % (letter, stats["grades"][letter]) for letter in GRADE_ORDER
        )
        lines.append("等级分布 : " + detail)
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="gradetool",
        description="统计一组分数的平均分、中位数、最高/最低分与标准差。",
    )
    parser.add_argument("scores", nargs="*", help="分数，可以写多个")
    parser.add_argument("-f", "--file", help="从文件读取分数（每行一个或用空格/逗号分隔）")
    parser.add_argument(
        "--pass-line",
        type=float,
        default=60.0,
        help="及格线，默认 60 分",
    )
    parser.add_argument(
        "--no-grade",
        action="store_true",
        help="只看基础统计，不输出及格率与等级分布",
    )
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    text = read_text(args)
    scores = parse_scores(text)
    stats = summarize(scores, pass_line=args.pass_line, with_grade=not args.no_grade)

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(render_text(stats))

    if not scores:
        print("提示：没有解析到任何分数。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
