from lcs2 import diff, diff_ranges, lcs, lcs_indices, lcs_length, lcs_weight

EPSILON = 1e-6


def test() -> None:
    a = 'Hello, world!'
    b = 'Foobar'

    assert lcs(a, b) == ['o', 'o', 'r']
    assert lcs_indices(a, b) == [(4, 1), (8, 2), (9, 5)]
    assert lcs_length(a, b) == 3

    assert diff(a, b) == [
        (['H', 'e', 'l', 'l'], ['F']),
        ([',', ' ', 'w'], []),
        ([], ['b', 'a']),
        (['l', 'd', '!'], []),
    ]
    assert diff_ranges(a, b) == [
        (range(0, 4), range(0, 1)),
        (range(5, 8), range(2, 2)),
        (range(9, 9), range(3, 5)),
        (range(10, 13), range(6, 6)),
    ]

    assert lcs('a', 'a') == ['a']
    assert lcs('a', 'b') == []
    assert lcs('', '') == []
    assert lcs(
        'aaa',
        'bbbb',
        lambda ca, cb: True,
    ) == lcs(
        'aaaa',
        'bbb',
        lambda ca, cb: True,
    ) == ['a', 'a', 'a']
    assert lcs(
        'aaa',
        'bbbb',
        lambda ca, cb: True,
        True,
    ) == lcs(
        'aaaa',
        'bbb',
        lambda ca, cb: True,
        True,
    ) == ['b', 'b', 'b']

    assert lcs(
        'xXOoyxXOo',
        'xozxo',
        weight=lambda ca, cb: 1 if ca.lower() == cb.lower() else 0,
    ) == lcs(
        'xozxo',
        'xXOoyxXOo',
        weight=lambda ca, cb: 1 if ca.lower() == cb.lower() else 0,
        take_b=True,
    ) == ['X', 'O', 'X', 'O']

    assert lcs_weight(
        'xxxoo',
        'ooxxx',
        weight=lambda ca, cb: {'x': 1, 'o': 2}[ca] if ca == cb else 0,
    ) == 4

    assert 3.3 - EPSILON < lcs_weight(
        'xxxoo',
        'ooxxx',
        weight=lambda ca, cb: {'x': 1.1, 'o': 1.6}[ca] if ca == cb else 0,
    ) < 3.3 + EPSILON

    print('All tests passed!')


test()
