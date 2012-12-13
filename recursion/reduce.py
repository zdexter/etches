def reduce(func, arr):
    """ Left-fold over arr using func, but don't use loops.
    >>> reduce(lambda x, y: x + y, [1,17,2,3,4,5,29])
    61
    >>> reduce(lambda x, y: x + y, [1,2,3,4,5])
    15
    >>> reduce(lambda x, y: x / y, [10,5,2])
    1
    >>> reduce(lambda x, y: x + y, [])
    []
    """
    if len(arr) == 0:
        return []
    if len(arr) == 1:
        return arr[0]
    arr[1] = func(arr[0], arr[1])
    return reduce(func, arr[1:])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
