from extratools_core.set import add_to_set


def test_add_to_set() -> None:
    s = set()

    assert add_to_set(s, 1)
    assert 1 in s

    assert not add_to_set(s, 1)
    assert 1 in s
