from extratools_core.iter import filter_by_others, filter_by_positions, is_sorted, remap


def test_is_sorted() -> None:
    assert is_sorted(range(10))
    assert not is_sorted(range(10), key=lambda x: -x)
    assert not is_sorted(range(10), reverse=True)

    assert not is_sorted(range(10, 0, -1))
    assert is_sorted(range(10, 0, -1), key=lambda x: -x)
    assert is_sorted(range(10, 0, -1), reverse=True)


def test_filter_by_positions() -> None:
    assert list(filter_by_positions(range(0, 10, 2), range(10, 20))) == list(range(10, 20, 2))

    assert list(filter_by_positions([], range(10))) == []


def test_filter_by_others() -> None:
    assert list(filter_by_others(lambda x, y: x > y, range(10))) == [9]

    assert list(filter_by_others(lambda x, y: x not in y, ["a", "ab", "b", "bc"])) == ["ab", "bc"]


def test_remap() -> None:
    m = {}

    # 1 to 5 are new items here
    assert list(remap(range(5, 0, -1), m)) == list(range(5))
    assert m == {
        5: 0,
        4: 1,
        3: 2,
        2: 3,
        1: 4,
    }

    # 1 to 5 are known items here
    assert list(remap(range(5, 0, -1), m)) == list(range(5))
    assert len(m) == 5
    # 1 to 5 are known items here
    assert list(remap(range(1, 6), m)) == list(range(4, -1, -1))
    assert len(m) == 5

    # 0 is new item here
    assert list(remap(range(5), m)) == list(range(5, 0, -1))
    assert m == {
        5: 0,
        4: 1,
        3: 2,
        2: 3,
        1: 4,
        0: 5,
    }
