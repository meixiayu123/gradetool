"""成绩统计的核心逻辑。

这里只做纯计算，不涉及任何输入输出，方便单独测试。
"""

# 等级划分：(下限, 等级, 绩点)
GRADE_SCALE = (
    (90.0, "A", 4.0),
    (80.0, "B", 3.0),
    (70.0, "C", 2.0),
    (60.0, "D", 1.0),
)


def parse_scores(text):
    """把一段文本解析成分数列表。

    支持空格、逗号、换行混合分隔，例如 "90, 85 70\\n100"。
    空字符串返回空列表；无法解析成数字的内容会被忽略。
    """
    scores = []
    for piece in text.replace(",", " ").split():
        try:
            scores.append(float(piece))
        except ValueError:
            continue
    return scores


def count(scores):
    """返回分数的个数。"""
    return len(scores)


def mean(scores):
    """返回平均分；空列表返回 0.0。"""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def median(scores):
    """返回中位数；空列表返回 0.0。"""
    if not scores:
        return 0.0
    ordered = sorted(scores)
    return ordered[len(ordered) // 2]


def spread(scores):
    """返回 (最低分, 最高分)；空列表返回 (0.0, 0.0)。"""
    if not scores:
        return 0.0, 0.0
    return min(scores), max(scores)


def std_dev(scores):
    """返回总体标准差；空列表返回 0.0。"""
    if not scores:
        return 0.0
    avg = mean(scores)
    variance = sum((x - avg) ** 2 for x in scores) / len(scores)
    return variance ** 0.5


def letter_of(score):
    """返回单个分数对应的等级，低于 60 分记作 F。"""
    for floor, letter, _ in GRADE_SCALE:
        if score >= floor:
            return letter
    return "F"


def point_of(score):
    """返回单个分数对应的绩点，低于 60 分记作 0.0。"""
    for floor, _, point in GRADE_SCALE:
        if score >= floor:
            return point
    return 0.0


def pass_rate(scores, pass_line=60.0):
    """返回及格率；空列表返回 0.0。

    pass_line 是及格线，默认 60 分，允许按课程难度调整。
    """
    if not scores:
        return 0.0
    passed = [x for x in scores if x >= pass_line]
    return len(passed) / len(scores)


def gpa(scores):
    """返回平均绩点；空列表返回 0.0。"""
    if not scores:
        return 0.0
    return sum(point_of(x) for x in scores) / len(scores)


def grade_distribution(scores):
    """返回各等级的人数，按 A、B、C、D、F 顺序给出，缺失的等级记 0。"""
    buckets = {letter: 0 for _, letter, _ in GRADE_SCALE}
    buckets["F"] = 0
    for score in scores:
        buckets[letter_of(score)] += 1
    return buckets


def grade_summary(scores):
    """把及格率、平均绩点和等级分布打包起来，供输出层使用。"""
    return {
        "pass_rate": pass_rate(scores),
        "gpa": gpa(scores),
        "grades": grade_distribution(scores),
    }


def summarize(scores, pass_line=60.0, with_grade=True):
    """把各项统计结果打包成一个字典，供输出层使用。"""
    low, high = spread(scores)
    stats = {
        "count": count(scores),
        "mean": mean(scores),
        "median": median(scores),
        "min": low,
        "max": high,
        "std": std_dev(scores),
    }
    if with_grade:
        stats.update(grade_summary(scores))
        stats["pass_line"] = pass_line
    return stats
