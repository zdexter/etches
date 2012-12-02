def permute(the_str):
    """Return all permutations of the input string.
    """
    perms = []
    if len(the_str) == 1:
        return the_str
    for i in range(len(the_str)):
        c = the_str[i]
        for p in permute(the_str[:i] + the_str[i+1:]):
            perms.append(c + p)
    return perms

def powerset(the_str):
    """Generate a powerset, minus the empty set.
        Yields 2^(len(the_str)-1) results.
    """
    pairs = [(2**index, char) for index, char in enumerate(the_str)]
    for index in xrange(1, 2**len(the_str)):
        yield ''.join(char for mask, char in pairs if mask & index)

def all_possible_words(the_str):
    """Return all unique strings that can be constructed
        from one or more letters of the input string,
        using the character at any one position at most once.
    """
    words = []
    for s in powerset(the_str):
        words.append(p for p in permute(s))
    return words

if __name__ == '__main__':
    import time
    test_strings = ['abcdefg']
    for string in test_strings:
        print 'test string {} has length {}'.format(string, len(string))

        start_time = time.time()
        all_possible_words(string)
        print '     all_possible_words took {} seconds'.format(
                time.time() - start_time)
