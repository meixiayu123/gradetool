"""成绩统计的核心逻辑。

这里只做纯计算，不涉及任何输入输出，方便单独测试。
"""


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
    """返回中位数；空列表返回 0.0。

    约定：分数个数为偶数时，取中间两个数的平均值。
    """
    if not scores:
        return 0.0
    ordered = sorted(scores)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


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


def summarize(scores):
    """把各项统计结果打包成一个字典，供输出层使用。"""
    low, high = spread(scores)
    return {
        "count": count(scores),
        "mean": mean(scores),
        "median": median(scores),
        "min": low,
        "max": high,
        "std": std_dev(scores),
    }
