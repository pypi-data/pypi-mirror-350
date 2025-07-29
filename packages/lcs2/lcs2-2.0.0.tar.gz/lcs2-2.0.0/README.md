# lcs2
`lcs2` is a Python package that helps find the longest common—or optimal weighted—subsequence of a pair of sequences and compute their diff. Among all optimal subsequences, it returns the one with the fewest runs (i.e., contiguous segments) across the two sequences.

## Installation
```
pip install lcs2
```

## Reference
The package provides the following functions, where `weight[A, B] = Callable[[A, B], int | float]`.

If the `weight` function is provided, it should return positive values if and only if the two elements can be matched. If the `weight` function is omitted, the elements are considered equal if they are identical, and the classical LCS sequence is returned.

| Function      | Signature                                                                  | Result                                                      |
|:--------------|:---------------------------------------------------------------------------|:------------------------------------------------------------|
| `lcs`         | `Iterable[A], Iterable[B], weight[A, B]?, take_b? -> list[A] \| list[B]`   | Longest (or optimal weighted) common subsequence (LCS/OWCS) |
| `lcs_indices` | `Iterable[A], Iterable[B], weight[A, B]? -> list[tuple[int, int]]`         | Indices of the LCS/OWCS                                     |
| `lcs_length`  | `Iterable[A], Iterable[B] -> int`                                          | Length of the LCS                                           |
| `lcs_weight`  | `Iterable[A], Iterable[B], weight[A, B] -> int \| float`                   | Weight of the OWCS                                          |
| `diff`        | `Iterable[A], Iterable[B], weight[A, B]? -> list[tuple[list[A], list[B]]]` | Differing segments of the sequences based on the LCS/OWCS   |
| `diff_ranges` | `Iterable[A], Iterable[B], weight[A, B]? -> list[tuple[range, range]]`     | Ranges of indices of the differing segments                 |

## Sample Usage
```python
from lcs2 import diff, diff_ranges, lcs, lcs_indices, lcs_length, lcs_weight

a = 'Hello, world!'
b = 'Foobar'

print(lcs(a, b))  # ['o', 'o', 'r']
print(lcs_indices(a, b))  # [(4, 1), (8, 2), (9, 5)]
print(lcs_length(a, b))  # 3

print(diff(a, b))  # [(['H', 'e', 'l', 'l'], ['F']),
                   # ([',', ' ', 'w'], []),
                   # ([], ['b', 'a']),
                   # (['l', 'd', '!'], [])]
print(diff_ranges(a, b))  # [(range(0, 4), range(0, 1)),
                          # (range(5, 8), range(2, 2)),
                          # (range(9, 9), range(3, 5)),
                          # (range(10, 13), range(6, 6))]

print(lcs(
    'xo',
    'xXOo',
    weight=lambda ca, cb: 1 if ca.lower() == cb.lower() else 0,
    take_b=True,
))  # ['X', 'O']

print(lcs_weight(
    'xxxoo',
    'ooxxx',
    weight=lambda ca, cb: {'x': 1, 'o': 2}[ca] if ca == cb else 0,
))  # 4
```
