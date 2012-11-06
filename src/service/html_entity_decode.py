#!/usr/bin/env python
# -*- coding: utf-8 -*-

import htmlentitydefs
import re


entity_re = re.compile(r'&(%s|#(\d{1,5}|[xX]([\da-fA-F]{1,4})));' % '|'.join(
    htmlentitydefs.name2codepoint.keys()))


def html_entity_decode(s, encoding='ascii'):
    """
    Convert all HTML entities to their applicable characters.

    Python implementation of http://pl.php.net/html_entity_decode

    Unicode object test:
    >>> html_entity_decode(u'test: &Theta;')
    u'test: \\u0398'

    UTF-8 string test:
    >>> html_entity_decode('test: &Theta;', encoding='utf-8')
    'test: \\xce\\x98'

    Default (ascii) string test:
    >>> html_entity_decode('test: &Theta;')
    'test: &#920;'

    Test equal entities:
    >>> print 62, hex(62), chr(62), unichr(62)
    62 0x3e > >
    >>> html_entity_decode(u'&gt;') == html_entity_decode('&gt;') == \
        html_entity_decode('&gt;', encoding='utf-8') == \
        html_entity_decode(u'&#62;') == html_entity_decode('&#62;') == \
        html_entity_decode('&#62;', encoding='utf-8') == \
        html_entity_decode(u'&#x3e;') == html_entity_decode('&#x3e;') == \
        html_entity_decode('&#x3e;', encoding='utf-8')
    True

    Testing all numeric entities (decimal and hexadecimal) for unicode:
    >>> for i in xrange(0x10000):
    ...     assert unichr(i) == html_entity_decode(u'&#%d;' % i) == \
                   html_entity_decode(u'&#x%s;' % hex(i)[2:])
    ...

    Testing all named (X)HTML entities for unicode:
    >>> for key, value in htmlentitydefs.name2codepoint.iteritems():
    ...     assert unichr(value) == html_entity_decode(u'&%s;' % key)
    ...

    Unknown entity test:
    >>> html_entity_decode('&unknown;')
    '&unknown;'
    >>> html_entity_decode('&#99999;')
    '&#99999;'

    Wrong argument test:
    >>> html_entity_decode([])
    Traceback (most recent call last):
        ...
    TypeError: argument 1: expected string, list found
    """

    if not isinstance(s, basestring):
        raise TypeError('argument 1: expected string, %s found' \
                        % s.__class__.__name__)

    def entity_2_unichr(matchobj):
        g1, g2, g3 = matchobj.groups()
        if g3 is not None:
            codepoint = int(g3, 16)
        elif g2 is not None:
            codepoint = int(g2)
        else:
            codepoint = htmlentitydefs.name2codepoint[g1]
        return unichr(codepoint)

    if isinstance(s, unicode):
        entity_2_chr = entity_2_unichr
    else:
        entity_2_chr = lambda o: entity_2_unichr(o).encode(encoding,
                                                           'xmlcharrefreplace')
    def silent_entity_replace(matchobj):
        try:
            return entity_2_chr(matchobj)
        except ValueError:
            return matchobj.group(0)

    return entity_re.sub(silent_entity_replace, s)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()