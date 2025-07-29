from extratools_core.json import flatten


def test_flatten() -> None:
    d = {
        "a": 1,
        "b": [
            2,
            {
                "c": 3,
                "d": [4],
            },
        ],
    }

    assert flatten(d) == {
        "a": 1,
        "b[0]": 2,
        "b[1].c": 3,
        "b[1].d[0]": 4,
    }

    assert flatten([1]) == {
        "[0]": 1,
    }

    assert flatten(1) == {
        ".": 1,
    }
