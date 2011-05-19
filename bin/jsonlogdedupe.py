#!/usr/bin/env python

import json

def compare(x, y, ignore=[]):
    a = x.copy()
    b = y.copy()
    for k in ignore:
        a.pop(k, None)
        b.pop(k, None)
    return a==b


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options...] <file>")
    parser.add_option('-i', '--ignore-key', action='append', type='string', help='ignore this key when comparing json lines')
    (options, args) = parser.parse_args()

    logfile = args[0]
    ignore = options.ignore_key

    f = file(logfile, 'r')
    l = f.next()
    print l,

    x = json.loads(l)
    y = None
    for l in f:
        y = json.loads(l)
        dupe = compare(x, y, ignore)
        if not dupe:
            print l,
        x = y





