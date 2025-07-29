#! env python
#

import argparse
import os
import sys
import webbrowser

try:
    from beaquery import beaqueryq
except Exception as e:
    import beaqueryq

def main():
    dfmt = 'json'
    ddir = '/tmp'
    argp = argparse.ArgumentParser(description='display BEA data model')

    argp.add_argument('--format', default=dfmt,
                      choices=['json', 'XML'],
        help='requested BEA result format(%s)' % dfmt)

    argp.add_argument('--directory', default='/tmp',
        help='where to store the generated html')

    args=argp.parse_args()

    BN = beaqueryq.BEAQueryQ()

    hd = BN.hierarchy(args.format)
    htm = BN.hierarchyhtml(hd)
    BN.showhtml('%s/hierarchy.html' % args.directory, htm)

if __name__ == '__main__':
    main()
