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
    dsk  = 'TimeSeriesDescription'
    dxk  = 'Year'
    dyk  = 'DataValue'
    duk  = 'CL_UNIT'
    argp = argparse.ArgumentParser(description='get BEA IntlServTrade data')

    argp.add_argument('--DatasetName', default='IntlServTrade',
                      help=argparse.SUPPRESS)
    argp.add_argument('--TypeOfService', required=True, help='type of service')
    argp.add_argument('--TradeDirection', help='trade direction')
    argp.add_argument('--Affiliation', help='affiliation')
    argp.add_argument('--AreaOrCountry', help='area or country')
    argp.add_argument('--Year', required=True,
                      help='year YYYY or ALL')

    argp.add_argument('--format', default=dfmt,
                      choices=['json', 'XML'],
                      help='query result format(%s)' % dfmt)

    argp.add_argument('--csvfn', \
         help='name of file to store dataset CSV result')
    argp.add_argument('--csvzipfn', \
             help='name of zip file to store dataset CSV results')


    argp.add_argument('--splitkey', default=dsk,
        help='table column name(%s) to use to split the plots' % dsk)
    argp.add_argument('--xkey', default=dxk,
        help='table column name(%s) to use to plot the data' % dxk)
    argp.add_argument('--ykey', default=dyk,
        help='table column name(%s) to use to plot the data'% dyk)
    argp.add_argument('--unitskey', default=duk,
        help='table column name(%s) to use to label the data' % duk)
    argp.add_argument('--htmlfn', \
        help='name of file to store dataset HTML result')

    args=argp.parse_args()

    BN = beaqueryq.BEAQueryQ()
    d = BN.getIntlServTradedata(args)
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
