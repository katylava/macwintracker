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
    parser.add_option('-f', '--print-first', action='store_true', dest='match_first', default=True, help='output only the first line of a series of duplicates')
    parser.add_option('-l', '--print-last', action='store_false', dest='match_first', help='output only the last line of a series of duplicates')
    (options, args) = parser.parse_args()

    logfile = args[0]
    ignore = options.ignore_key

    f = file(logfile, 'r')
    xline = f.next()
    if options.match_first:
        print xline,

    xjson = json.loads(xline)
    yjson = None
    for yline in f:
        try:
            yjson = json.loads(yline)
        except ValueError:
            # skip lines with json errors
            pass
        else:
            dupe = compare(xjson, yjson, ignore)
            if not dupe:
                if options.match_first:
                    print yline,
                else:
                    print xline,
            xjson = yjson
            xline = yline





