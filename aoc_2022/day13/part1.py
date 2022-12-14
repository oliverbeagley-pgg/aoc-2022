from __future__ import annotations

import argparse
import itertools
import os
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

ListAlike = int | list["ListAlike"]


def compare(left: ListAlike, right: ListAlike) -> int:
    match left, right:

        case int(left), int(right):
            return left - right

        case int(left), list(right):
            left = [left]

        case list(left), int(right):
            right = [right]

    # As mypy doesn't recognise the type narrowing above :(
    assert isinstance(left, list)
    assert isinstance(right, list)

    for l_i, r_i in itertools.zip_longest(left, right, fillvalue=None):
        if l_i is None:
            return -1
        elif r_i is None:
            return 1

        comp = compare(l_i, r_i)
        if comp != 0:
            return comp
    else:
        return 0


def compute(input: str) -> int:
    pairs_s = input.split("\n\n")
    signals: list[list[ListAlike]] = [
        [eval(expr) for expr in pair.splitlines()] for pair in pairs_s
    ]

    idx_sum = 0
    for idx, (left, right) in enumerate(signals, 1):
        if compare(left, right) <= 0:
            idx_sum += idx

    return idx_sum


TEST_INPUT = """
    [1,1,3,1,1]
    [1,1,5,1,1]

    [[1],[2,3,4]]
    [[1],4]

    [9]
    [[8,7,6]]

    [[4,4],4,4]
    [[4,4],4,4,4]

    [7,7,7,7]
    [7,7,7]

    []
    [3]

    [[[]]]
    [[]]

    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [1,[2,[3,[4,[5,6,0]]]],8,9]
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 13),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
