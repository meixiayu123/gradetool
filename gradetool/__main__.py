"""gradetool 的命令行入口。

用法示例：
    python -m gradetool 90 85 70 100
    python -m gradetool --file scores.txt
    type scores.txt | python -m gradetool
    python -m gradetool --json 90 85 70
"""

import argparse
import json
import sys

from .core import parse_scores, summarize


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
        "=" * 24,
        "人数   : %d" % stats["count"],
        "平均分 : %.2f" % stats["mean"],
        "中位数 : %.2f" % stats["median"],
        "最低分 : %.2f" % stats["min"],
        "最高分 : %.2f" % stats["max"],
        "标准差 : %.2f" % stats["std"],
    ]
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="gradetool",
        description="统计一组分数的平均分、中位数、最高/最低分与标准差。",
    )
    parser.add_argument("scores", nargs="*", help="分数，可以写多个")
    parser.add_argument("-f", "--file", help="从文件读取分数（每行一个或用空格/逗号分隔）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    text = read_text(args)
    scores = parse_scores(text)
    stats = summarize(scores)

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
