#!/usr/bin/env python

"""
Working through Parser Combinators Made Simple
Source: http://sigusr2.net/2011/Apr/18/parser-combinators-made-simple.html
This code uses higher-order functions to build a JSON parser out of smaller parsers.
I think parser combinators are elegant.

Paradigm: Return None if parser failed. Else, return (parsed string, unparsed string).
"""

def anychar(strn):
    """Match any char if the input string has at least one char.

    >>> anychar('a')
    ('a', '')
    >>> anychar('abc')
    ('a', 'bc')
    >>> anychar('')
    """
    if strn == "":
        return None
    return (strn[0], strn[1:])

# All methods below return parser functions.

def chartest(pred):
    """Match first char of input string against predicate.
    >>> chartest(lambda x: x == 'a')('abc')
    ('a', 'bc')
    >>> chartest(lambda x: x == 'd')('abc')
    >>> chartest(lambda x: x == 'b')('abc')
    """
    def _(strn):
        c = anychar(strn)
        if c and pred(c[0]):
            return (c[0], c[1])
        return None
    return _ # Return a function so we can combinate later on!

def matchchr(targetchr):
    """Help out chartest by generating a predicate
        given an input character.
    """
    return chartest(lambda x: x == targetchr)

def oneof(target):
    """See if any char in target is in the
        input string. If so, consume char.
    >>> oneof('abc')('b')
    ('b', '')
    >>> oneof('abc')('d')
    >>> oneof('abc')('')
    """
    chars = set([x for x in target])
    return chartest(lambda x: x in chars)

alpha = oneof('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
loweralpha = oneof('abcdefghijklmnopqrstuvwxyz')
upperalpha = oneof('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
digit = oneof('0123456789')
hexdigit = oneof('0123456789abcdefABCDEF')
whitespace = oneof(' \t\n\r')

def matchstr(target):
    """Match a token by recursively consuming
        the first char in target.

       If every char matches, return a tuple with the
        token.
       If at any point during recursion, a char doesn't match,
        return None.

       >>> matchstr('abc')('abcdef')
       ('abc', 'def')
       >>> matchstr('')('abc')
       ('', 'abc')
       >>> matchstr('abc')('b')
    """
    if not target:
        return lambda strn: ("", strn)
    def _(strn):
        c = matchchr(target[0])(strn) # Consume first char
        if c:
            cs = matchstr(target[1:])(c[1])
            if cs:
                # Tack on matched char (this block runs if not base case)
                return (c[0] + cs[0], cs[1])
        # Since the base case actually returns something, we only
        #  get here if there's no match at all.
        return None
    return _

def optional(parserfn):
    """Return func that returns
        match if there is one, or input string if not.

       >>> optional(matchstr('while'))('while True:')
       ('while', ' True:')
       >>> optional(matchstr('nacho'))('burrito Taco:')
       ('', 'burrito Taco:')
    """
    def _(strn):
        c = parserfn(strn)
        if c:
            return c # Match
        return ('', strn) # Original input string
    return _

def repeat(parser):
    """Return func that matches input at least once.

    >>> repeat(matchstr('while'))('whilewhilewhileTrue:')
    ('whilewhilewhile', 'True:')
    >>> repeat(matchstr('nacho'))('whilewhilewhileTrue:')
    """
    def _(strn):
        c = parser(strn) # This is the 'at least once' part
        if c:
            cs = repeat0(parser)(c[1]) # Okay if no match
            # (1st + 2nd (if there) match, unconsumed chars)
            return (c[0] + cs[0], cs[1])
        return None
    return _

def repeat0(parser):
    # Equivalent to "optionally one or more"
    # This call always succeeds - the match is optional
    return optional(repeat(parser))

def alt(*parsers):
    """Try out each parser. If one matches next token, consume.
    >>> alt(matchstr('if'), matchstr('for'), matchstr('while'))('if')
    ('if', '')
    >>> alt(matchstr('nacho'), matchstr('burrito'))('burritotaco')
    ('burrito', 'taco')
    >>> alt(matchstr('while'))('while')
    ('while', '')
    >>> alt(matchstr('hey'))('cheesehey')
    >>> alt(matchstr('hey'))('cheese')
    """
    def _(strn):
        for p in parsers:
            result = p(strn)
            if result:
                return result
    return _

def sequence(*parsers):
    """Consume and match; if sequence is broken, return None.
        Else return tuple with the (parsed string, unparsed string).
       >>> sequence(matchstr('lol'), matchstr('copter'))('lolcopter')
       ('lolcopter', '')
       >>> sequence(matchstr('lol'), matchstr('copters'))('lolcoptersflying')
       ('lolcopters', 'flying')
       >>> sequence(matchstr('lol'), matchstr('coptering'))('lolcopterin')
    """
    def _(strn):
        parsed = ''
        rest = strn
        for p in parsers:
            result = p(rest)
            if result:
                rest = result[1]
                parsed += result[0]
            else:
                return None
        return (parsed, rest)
    return _

# JSON parser

def betweenchrs(parser, left="(", right=")"):
    """Try to use parser on value if argument to parser is in
        parens in value.
       >>> betweenchrs(matchstr('test'))('(test)string')
       ('(test)', 'string')
    """
    def _(strn):
        lres = matchchr(left)(strn)
        if lres:
            pres = parser(lres[1])
            if pres:
                rres = matchchr(right)(pres[1])
                if rres:
                    return (left + pres[0] + right, rres[1])
        return None
    return _

# The parser we pass should try to consume what's between left and right
betweenparens = lambda p: betweenchrs(p, left="(", right=")")
betweenbrackets = lambda p: betweenchrs(p, left="[", right="]")
betweencurlies = lambda p: betweenchrs(p, left="{", right="}")

def charorquoted(strn):
    """Error if we encounter an unescaped double quote.
        Else, consume backslash or double quote.
        Important: The first \ in \\ is merely Python escape sequence syntax.
       >>> charorquoted("s")
       ('s', '')
       >>> charorquoted('"')
    """
    c = anychar(strn)
    if c[0] == '"':
        return None
    elif c[0] == '\\':
        c2 = chartest(lambda x: x in ('\\', '"'))(c[1])
        if c2:
            return (c[0] + c2[0], c2[1])
    else:
        return c

def ignorews(p):
    """Strip whitespace until there's none left, then match.
        If we encounter more whitespace after match, strip.
        Either way, return (match, rest of string)
    """
    def _(strn):
        w = repeat0(whitespace)(strn)
        if w:
            pres = p(w[1])
            if pres:
                w2 = repeat0(whitespace)(pres[1])
                if w2:
                    return (pres[0], w2[1])
        return None
    return _

anint = sequence(optional(matchchr("-")), repeat(digit))
astring = betweenchrs(repeat0(charorquoted), left='"', right='"')
acolon = matchchr(':')
acomma = matchchr(',')

class Forward(object):
    def _init__(self):
        self.p = None
    def __call__(self, *args, **kwargs):
        return self.p(*args, **kwargs)
    def __ilshift__(self, p):
        """Override <<=
        """
        self.p = p
        return self

avalue = Forward()
akey = ignorews(alt(anint,astring))
akeyvaluepair = sequence(akey, acolon, avalue)

def commaseparated(parser):
    def _(strn):
        # Consume value, comma, ..., ...
        r = repeat0(sequence(parser, acomma))(strn)
        if r:
            r2 = parser(r[1]) # No comma after last item
            if r2:
                return (r[0] + r2[0], r2[1])
        elif r:
            return r
        return None
    return _

adict = betweencurlies(commaseparated(akeyvaluepair))
alist = betweenbrackets(commaseparated(avalue))

# Match if value is any one of the types in []
#  once whitespace has been stripped
avalue <<= alt(*map(ignorews, [adict, alist, anint, astring]))

json = alt(adict, alist)

def parse_json(strn):
    """
       >>> json('''{"hello": {1: "how are you?"}, "i is": "fine", "how": "are you?", 1: ["these", "values", "work", 2]}''')
       ('{"hello":{1:"how are you?"},"i is":"fine","how":"are you?",1:["these","values","work",2]}', '')
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()
