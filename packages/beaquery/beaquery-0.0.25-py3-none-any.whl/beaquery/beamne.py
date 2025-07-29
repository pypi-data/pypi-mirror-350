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
    dsk  = 'SeriesName'
    dxk  = 'Year'
    dyk  = 'DataValue'
    duk  = 'TableScale'
    argp = argparse.ArgumentParser(description='get BEA MNE data')

    argp.add_argument('--DatasetName', default='MNE',
                      help=argparse.SUPPRESS)
    argp.add_argument('--SeriesID', help='MNE series id')
    argp.add_argument('--DirectionOfInvestment', required=True, help='direction of investment')
    argp.add_argument('--Classification', required=True, help='classification')
    argp.add_argument('--Country', help='country')
    argp.add_argument('--Industry', help='industry')
    argp.add_argument('--Year', required=True,
                      help='year YYYY or all')

    argp.add_argument('--format', default=dfmt,
                      choices=['json', 'XML'],
                      help='query result format(%s)'% dfmt)

    argp.add_argument('--csvfn', \
         help='name of file to store dataset CSV result')
    argp.add_argument('--csvzipfn', \
             help='name of zip file to store dataset CSV results')


    argp.add_argument('--splitkey', default=dsk,
        help='table column name(%s) to use to split the plots' % dsk)
    argp.add_argument('--xkey', default=dxk,
        help='table column name(%s) to use to plot the data' % dxk)
    argp.add_argument('--ykey', default=dyk,
        help='table column name(%s) to use to plot the data' % dyk)
    argp.add_argument('--unitskey', default=duk,
        help='table column name(%s) to to y label the plot' % duk)
    argp.add_argument('--htmlfn', \
        help='name of file to store dataset HTML result')

    args=argp.parse_args()

    BN = beaqueryq.BEAQueryQ()
    d = BN.getMNEdata(args)
    if d == None or type(d) == type({}) and 'Data' not in d.keys():
        print('%s: no data' % os.path.basename(__file__), file=sys.stderr)
    else:
        if args.csvfn != None:
            BN.store2csv(d, args.csvfn)
        elif args.csvzipfn:
            zfn = BN.d2csvzipfile(d, args)
        elif args.htmlfn != None:
            h = BN.d2html(d, args)
            with open(args.htmlfn, 'w') as fp:
                print(h, file=fp)
            webbrowser.open('file://%s' % args.htmlfn)
        else:
            BN.print2csv(d)


if __name__ == '__main__':
    main()
