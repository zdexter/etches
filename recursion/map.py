def map(func, arr):
    """Return the result of applying func to every argument in arr
    >>> map(lambda x: x + 3, [1,2,4,3,5])
    [4, 5, 7, 6, 8]
    >>> map(lambda x: 2**x, [0,1,2,3,4])
    [1, 2, 4, 8, 16]
    """
    if len(arr) == 0:
        return []
    arr[0] = func(arr[0])
    return [arr[0]] + map(func, arr[1:])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
