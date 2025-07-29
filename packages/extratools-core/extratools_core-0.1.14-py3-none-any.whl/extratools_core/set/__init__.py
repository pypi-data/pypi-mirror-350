def add_to_set[T](s: set[T], x: T) -> bool:
    if x in s:
        return False

    s.add(x)
    return True
