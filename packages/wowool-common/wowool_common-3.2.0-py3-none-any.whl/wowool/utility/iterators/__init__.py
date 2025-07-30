def iterate_prv_nxt(my_list):
    """
    create a iterator that returns.
    prev, current and the  next
    """
    prv, cur, nxt = None, iter(my_list), iter(my_list)
    next(nxt, None)
    idx = 0

    while True:
        try:
            if prv:
                yield idx, next(prv), next(cur), next(nxt, None)
            else:
                yield idx, None, next(cur), next(nxt, None)
                prv = iter(my_list)
            idx += 1
        except StopIteration:
            break


def iterate_nxt(my_list):
    """
    create a iterator that returns.
    current and the  next
    """
    cur, nxt = iter(my_list), iter(my_list)
    next(nxt, None)
    idx = 0

    while True:
        try:
            yield idx, next(cur), next(nxt, None)
            idx += 1
        except StopIteration:
            break


def iterate_prv(my_list):
    """
    create a iterator that returns.
    prev, current and the  next
    """
    (
        prv,
        cur,
    ) = None, iter(my_list)

    idx = 0
    while True:
        try:
            if prv:
                yield idx, next(prv), next(cur)
            else:
                yield idx, None, next(cur)
                prv = iter(my_list)
            idx += 1
        except StopIteration:
            break
