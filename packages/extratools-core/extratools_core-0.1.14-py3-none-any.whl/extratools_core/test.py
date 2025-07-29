from collections.abc import Callable, MutableMapping
from typing import Any


def expect_exception(error_cls: type[Exception], f: Callable[[], Any]) -> None:
    try:
        f()
    except error_cls:
        return

    raise AssertionError


def is_proper_mutable_mapping[KT, VT](
    cls: type[MutableMapping[KT, VT]],
    *,
    key_cls: type[KT],
    value_cls: type[VT],
) -> None:
    m: MutableMapping[KT, VT] = cls()

    assert isinstance(m, MutableMapping)

    assert len(m) == 0

    assert list(m.keys()) == []
    assert list(m.values()) == []
    assert list(m.items()) == []

    key: KT = key_cls()
    value: VT = value_cls()
    assert key not in m

    m[key] = value
    assert key in m
    assert len(m) == 1
    assert m[key] == value
    assert m.get(key) == value

    assert list(m.keys()) == [key]
    assert list(m.values()) == [value]
    assert list(m.items()) == [(key, value)]

    # No duplication
    m[key] = value
    assert len(m) == 1

    del m[key]
    assert key not in m
    assert len(m) == 0
    expect_exception(KeyError, lambda: m[key])
    assert m.get(key) is None
    assert m.get(key, value) == value

    assert m.setdefault(key, value) == value
    assert key in m
    assert len(m) == 1
    assert m[key] == value

    assert m.pop(key) == value
    assert key not in m
    assert len(m) == 0
    # `pop`` is special here that it would raise `KeyError` if `default` is not specified.
    expect_exception(KeyError, lambda: m.pop(key))
    assert m.pop(key, None) is None
    assert m.pop(key, value) == value
