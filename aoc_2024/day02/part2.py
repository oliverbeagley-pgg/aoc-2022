import argparse
from itertools import pairwise
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    reports = [[int(x) for x in line.split()] for line in puzzle_input.splitlines()]

    outcomes = [
        is_safe(report)
        or any(is_safe(report[:idx] + report[idx + 1 :]) for idx in range(len(report)))
        for report in reports
    ]

    return sum(1 for outcome in outcomes if outcome)


def is_safe(report: list[int]) -> bool:
    if report[0] == report[1]:
        return False

    sign = report[1] - report[0]
    upper_bound = 3

    outcome = False

    for left, right in pairwise(report):
        diff = right - left

        if (sign * diff <= 0) or (abs(diff) > upper_bound):
            break
    else:
        outcome = True

    return outcome


TEST_INPUT = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 4),
    ],
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, aoc_utils.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
