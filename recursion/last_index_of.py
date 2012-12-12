def last_index_of(item, arr):
    """Return last index at which item occurs in arr
    >>> last_index_of(5, [1, 2, 4, 6, 5, 2, 7])
    4
    >>> last_index_of(5, [1, 2, 4, 6, 2, 7])
    -1
    >>> last_index_of(5, [1, 2, 5, 4, 6, 5, 2, 7])
    5
    """
    i = len(arr) - 1
    if i == 0:
        return -1
    if arr[i] == item:
        return i
    return last_index_of(item, arr[:i])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
