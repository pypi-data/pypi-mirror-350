from extratools_core.dict import invert, invert_safe, inverted_index


def test_invert() -> None:
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    assert invert({"a": 1, "b": 1}) == {1: "b"}


def test_invert_safe() -> None:
    assert invert_safe({"a": 1, "b": 1}) == {1: ["a", "b"]}


def test_inverted_index() -> None:
    assert inverted_index([
        "abc",
        "abcdefabc",
        "defghi",
    ]) == {
        "a": [(0, [0]), (1, [0, 6])],
        "b": [(0, [1]), (1, [1, 7])],
        "c": [(0, [2]), (1, [2, 8])],
        "d": [(1, [3]), (2, [0])],
        "e": [(1, [4]), (2, [1])],
        "f": [(1, [5]), (2, [2])],
        "g": [(2, [3])],
        "h": [(2, [4])],
        "i": [(2, [5])],
    }
