def my_sum(a):
    """
    >>> my_sum([1,2,3,4,5])
    15
    >>> my_sum([])
    0
    """
    length = len(a)
    if length is 0:
        return 0
    elif length is 1:
        return a[0]
    length -= 1;
    return a[length] + my_sum(a[:length])


if __name__ == '__main__':
    import doctest
    doctest.testmod()
