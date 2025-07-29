from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
import math
from typing import Callable, cast, Iterable

__all__ = [
    'diff',
    'diff_ranges',
    'lcs',
    'lcs_indices',
    'lcs_length',
    'lcs_weight',
]


class Pattern(StrEnum):
    EMPTY_EMPTY = 'empty_empty'
    EMPTY_FILLED = 'empty_filled'
    FILLED_EMPTY = 'filled_empty'
    FILLED_FILLED = 'filled_filled'


@dataclass
class Step:
    indices: tuple[int, int]
    pattern: Pattern


@dataclass
class Data:
    weight: int | float = 0
    groups: int = 0
    step: Step | None = None

    @staticmethod
    def impossible() -> Data:
        return Data(weight=-math.inf)

    def add_weight(self, weight: int | float) -> Data:
        return Data(
            weight=self.weight + weight,
            groups=self.groups,
            step=self.step,
        )

    def add_groups(self, groups: int) -> Data:
        return Data(
            weight=self.weight,
            groups=self.groups + groups,
            step=self.step,
        )

    def set_step(self, step: Step) -> Data:
        return Data(
            weight=self.weight,
            groups=self.groups,
            step=step,
        )

    def sort_key(self) -> tuple[int | float, int]:
        return self.weight, -self.groups

    @staticmethod
    def best(*args: Data) -> Data:
        return max(args, key=lambda cell: cell.sort_key())


@dataclass
class Cell:
    patterns: dict[Pattern, Data] = field(default_factory=lambda: {
        Pattern.EMPTY_EMPTY: Data(),
        Pattern.EMPTY_FILLED: Data.impossible(),
        Pattern.FILLED_EMPTY: Data.impossible(),
        Pattern.FILLED_FILLED: Data.impossible(),
    })

    def best(self) -> Data:
        return Data.best(*self.patterns.values())


def default_weight[TA, TB](a: TA, b: TB) -> int:
    return 1 if a == b else 0


def compute_matrix[TA, TB](a: list[TA], b: list[TB], weight: Callable[[TA, TB], int | float]) -> list[list[Cell]]:
    m: list[list[Cell]] = [[Cell() for _ in range(len(b) + 1)]]
    for ai in range(1, len(a) + 1):
        row = [Cell()]
        m.append(row)
        for bi in range(1, len(b) + 1):
            top_left = ai - 1, bi - 1
            top_left_cell = m[ai - 1][bi - 1]
            row.append(Cell({
                Pattern.EMPTY_EMPTY: top_left_cell.best(),
                Pattern.EMPTY_FILLED: Data.best(
                    m[ai - 1][bi].patterns[Pattern.EMPTY_FILLED],
                    m[ai - 1][bi].patterns[Pattern.FILLED_FILLED],
                ),
                Pattern.FILLED_EMPTY: Data.best(
                    m[ai][bi - 1].patterns[Pattern.FILLED_EMPTY],
                    m[ai][bi - 1].patterns[Pattern.FILLED_FILLED],
                ),
                Pattern.FILLED_FILLED: (
                    Data.best(
                        (top_left_cell.patterns[Pattern.EMPTY_EMPTY].add_groups(2)
                            .set_step(Step(top_left, Pattern.EMPTY_EMPTY))),
                        (top_left_cell.patterns[Pattern.EMPTY_FILLED].add_groups(1)
                            .set_step(Step(top_left, Pattern.EMPTY_FILLED))),
                        (top_left_cell.patterns[Pattern.FILLED_EMPTY].add_groups(1)
                            .set_step(Step(top_left, Pattern.FILLED_EMPTY))),
                        (top_left_cell.patterns[Pattern.FILLED_FILLED]
                            .set_step(Step(top_left, Pattern.FILLED_FILLED))),
                    ).add_weight(w)
                    if (w := weight(a[ai - 1], b[bi - 1])) > 0
                    else Data.impossible()
                ),
            }))
    return m


def lcs_weight_lists[TA, TB](a: list[TA], b: list[TB], weight: Callable[[TA, TB], int | float]) -> int | float:
    return compute_matrix(a, b, weight)[len(a)][len(b)].best().weight


def lcs_weight[TA, TB](a: Iterable[TA], b: Iterable[TB], weight: Callable[[TA, TB], int | float]) -> int | float:
    """Compute the weight of the optimal weighted common subsequence between two sequences."""
    return lcs_weight_lists(list(a), list(b), weight)


def lcs_length[TA, TB](a: Iterable[TA], b: Iterable[TB]) -> int:
    """Compute the length of the longest common subsequence between two sequences."""
    return cast(int, lcs_weight(a, b, default_weight))


def lcs_indices_lists[TA, TB](
        a: list[TA],
        b: list[TB],
        weight: Callable[[TA, TB], int | float] | None,
) -> list[tuple[int, int]]:
    m = compute_matrix(a, b, weight or default_weight)
    steps: list[tuple[int, int]] = []
    step = m[len(a)][len(b)].best().step
    while step:
        steps.append(step.indices)
        ai, bi = step.indices
        step = m[ai][bi].patterns[step.pattern].step
    return list(reversed(steps))


def lcs_indices[TA, TB](
        a: Iterable[TA],
        b: Iterable[TB],
        weight: Callable[[TA, TB], int | float] | None = None,
) -> list[tuple[int, int]]:
    """
    Compute the indices of the longest (or optimal weighted) common subsequence between two sequences.
    The indices are returned as a list of tuples, where each tuple contains the index from the first sequence
    and the corresponding index from the second sequence.
    `weight` is a function that assigns a weight to a potential match between two elements: return a positive value to
    allow the match, or a non-positive value to disallow it. If omitted, only identical elements are matched (classical
    LCS).
    """
    return lcs_indices_lists(list(a), list(b), weight)


def lcs_lists[TA, TB](
        a: list[TA],
        b: list[TB],
        weight: Callable[[TA, TB], int | float] | None,
        take_b: bool,
) -> list[TA] | list[TB]:
    return [b[bi] if take_b else a[ai] for ai, bi in lcs_indices(a, b, weight)]


def lcs[TA, TB](
        a: Iterable[TA],
        b: Iterable[TB],
        weight: Callable[[TA, TB], int | float] | None = None,
        take_b: bool = False,
) -> list[TA] | list[TB]:
    """
    Compute the longest (or optimal weighted) common subsequence between two sequences.
    `weight` is a function that assigns a weight to a potential match between two elements: return a positive value to
    allow the match, or a non-positive value to disallow it. If omitted, only identical elements are matched (classical
    LCS).
    If `take_b` is True, the elements are taken from the second sequence; otherwise, from the first.
    """
    return lcs_lists(list(a), list(b), weight, take_b)


def diff_ranges_lists[TA, TB](
        a: list[TA],
        b: list[TB],
        weight: Callable[[TA, TB], int | float] | None,
) -> list[tuple[range, range]]:
    ranges: list[tuple[range, range]] = []
    a_pos, b_pos = 0, 0
    for ai, bi in lcs_indices_lists(a, b, weight) + [(len(a), len(b))]:
        if ai > a_pos or bi > b_pos:
            ranges.append((range(a_pos, ai), range(b_pos, bi)))
        a_pos = ai + 1
        b_pos = bi + 1
    return ranges


def diff_ranges[TA, TB](
        a: Iterable[TA],
        b: Iterable[TB],
        weight: Callable[[TA, TB], int | float] | None = None,
) -> list[tuple[range, range]]:
    """
    Compute the ranges of differences between two sequences.
    The ranges are returned as a list of tuples, where each tuple contains two ranges:
    the first corresponds to the first sequence, and the second corresponds to the second sequence.
    `weight` is a function that assigns a weight to a potential match between two elements: return a positive value to
    allow the match, or a non-positive value to disallow it. If omitted, only identical elements are matched (classical
    LCS).
    """
    return diff_ranges_lists(list(a), list(b), weight)


def diff_lists[TA, TB](
        a: list[TA],
        b: list[TB],
        weight: Callable[[TA, TB], int | float] | None,
) -> list[tuple[list[TA], list[TB]]]:
    return [([a[i] for i in a_range], [b[i] for i in b_range])
            for a_range, b_range in diff_ranges_lists(a, b, weight)]


def diff[TA, TB](
        a: Iterable[TA],
        b: Iterable[TB],
        weight: Callable[[TA, TB], int | float] | None = None,
) -> list[tuple[list[TA], list[TB]]]:
    """
    Compute the differences between two sequences.
    The differences are returned as a list of tuples, where each tuple contains two lists:
    the first list corresponds to the first sequence, and the second list corresponds to the second sequence.
    `weight` is a function that assigns a weight to a potential match between two elements: return a positive value to
    allow the match, or a non-positive value to disallow it. If omitted, only identical elements are matched (classical
    LCS).
    """
    return diff_lists(list(a), list(b), weight)
