"""
Bit stuffing stuffs bits add the end of frame boundaries.
'De-stuffing' detects and removes stuffed bits.
"""

def stuff(bit_str, frame_boundary=5):
    """
    Escapes every (frame_boundary+1)-th bit, if that bit is a 1.
     This breaks the data up into fixed-length frames.
    >>> stuff("10101011011111011111100")
    '1010101101111100111110100'
    >>> stuff("1111111")
    '11111011'
    """
    consecutive_ones = 0
    for i in xrange(len(bit_str)):
        c = bit_str[i]
        if c == '1':
            consecutive_ones += 1
        else:
            consecutive_ones = 0
        if consecutive_ones == 5:
            bit_str = bit_str[:i+1] + "0" + bit_str[i+1:]
            # Optimization (TODO): Can skip i+1th iteration if we reset consecutive_ones here
    return bit_str

def destuff(bit_str, frame_boundary=5):
    """
    Unescape every (frame_boundary minus 1)th
    >>> destuff("1010101101111100111110100")
    '10101011011111011111100'
    >>> destuff("11111011")
    '1111111'
    """
    consecutive_ones = 0
    for i in xrange(len(bit_str)):
        try:
            c = bit_str[i]
        except:
            # TODO: Structure this control flow
            break
        if c == '1':
            consecutive_ones += 1
        else:
            consecutive_ones = 0
        if consecutive_ones == frame_boundary:
            bit_str = bit_str[:i+1] + bit_str[i+2:] # Up to current pos, exclusive, plus rest

    return bit_str

if __name__ == '__main__':
    import doctest
    doctest.testmod()
