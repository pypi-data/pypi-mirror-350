def first_not_none[T](*args: T | None) -> T | None:
    for arg in args:
        if arg is not None:
            return arg
    return None
