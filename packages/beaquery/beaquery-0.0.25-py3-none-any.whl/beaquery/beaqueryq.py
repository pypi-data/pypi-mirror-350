#! env python
#
import argparse
import glob
import json
import os
import re
import sys
import time
import webbrowser
import xml
import xml.etree.ElementTree as ET
import zipfile

import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

try:
    from beaquery import ebquery
except Exception as e:
    import ebquery


class BEAQueryQ():
    def __init__(self):

        self.bsurl = 'https://apps.bea.gov/api/signup/'
        if 'BEA_API_KEY' in os.environ:
                self.api_key = os.environ['BEA_API_KEY']
        else:
            print('BEA api_key required: %s' % (self.bsurl), file=sys.stderr)
            print('assign this key to BEA_API_KEY env variable',
                              file=sys.stderr)
            sys.exit()

        self.bdurl = 'https://apps.bea.gov/api/data/'
        self.burl = '%s?&UserID=%s' % (self.bdurl, self.api_key)

        self.trurl = 'https://apps.bea.gov/national/Release/TXT/TablesRegister.txt'

        self.uq = ebquery._EBURLQuery()

        self.args = None
        self.zipdir = '/tmp/BEA'

    def getNIPAregister(self):
        """ getNIPAregister()
        retrieve and return the register of BEA NIPA tables
        """
        resp = self.uq.query(self.trurl)
        if resp == None:
            print('getNIPAregister: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        return rstr

    # not using TableID Parameter
    def NIPAParams(self, args):
        if args.Frequency == None or args.Year == None:
            print('NIPAParams: Frequency and Year required', file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableName=%s&'
                  'ShowMillions=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('NIPA', args.TableName, args.ShowMillions,
                  args.Frequency, args.Year,
                  args.format) )
        return params

    def NIUnderlyingDetailParams(self, args):
        if args.Frequency == None or args.Year == None:
            print('NIUnderlyingDetailParams: Frequency and Year required',
                   file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableName=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('NIUnderlyingDetail', args.TableName, args.Frequency,
                  args.Year,
                  args.format) )
        return params


    def MNEParams(self, args):
        if args.DirectionOfInvestment == None or args.Classification == None or args.Year == None:
            print('MNEParameters: DirectionOfInvestment,'
                  'Classification,and Year required', file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'SeriesID=%s&'
                  'DirectionOfInvestment=%s&'
                  'Classification=%s&'
                  'Country=%s&'
                  'Industry=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('MNE', args.SeriesID, args.DirectionOfInvestment,
                  args.Classification, args.Country,
                  args.Industry, args.Year, args.format) )
        return params

    def FixedAssetsParams(self, args):
        if args.TableName == None or args.Year == None:
            print('FixedAssetsParameters TableName and Year required',
                  file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableName=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('FixedAssets', args.TableName, args.Year, args.format) )
        return params

    def ITAParams(self, args):
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'Indicator=%s&'
                  'AreaOrCountry=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('ITA', args.Indicator, args.AreaOrCountry, args.Frequency,
                  args.Year,
                  args.format) )
        return params

    def IIPParams(self, args):
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TypeOfInvestment=%s&'
                  'Component=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('IIP', args.TypeOfInvestment, args.Component, args.Frequency, args.Year,
                  args.format) )
        return params

    def InputOutputParams(self, args):
        if args.TableID == None or args.Year == None:
            print('InputOutputParameters TableID and Year required',
                  file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableID=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('InputOutput', args.TableID, args.Year, args.format) )
        return params

    def IntlServTradeParams(self, args):
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TypeOfService=%s&'
                  'TradeDirection=%s&'
                  'Affiliation=%s&'
                  'AreaOrCountry=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('IntlServTrade', args.TypeOfService,
                  args.TradeDirection, args.Affiliation,
                  args.AreaOrCountry, args.Year, args.format) )
        return params

    def IntlServSTAParams(self, args):
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'Channel=%s&'
                  'Destination=%s&'
                  'Industry=%s&'
                  'AreaOrCountry=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('IntlServSTA', args.Channel, args.Destination, args.Industry,
                  args.AreaOrCountry, args.Year, args.format) )
        return params

    def GDPbyIndustryParams(self, args):
        if args.Frequency == None or args.Industry == None or args.TableID == None \
        or args.Year == None:
            print('GDPbyIndustryParameters Frequency, Industry,'
            'TableID, Year required', file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableID=%s&'
                  'Industry=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('GDPbyIndustry', args.TableID, args.Industry,
                  args.Frequency,
                  args.Year, args.format) )
        return params

    def RegionalParams(self, args):
        if args.GeoFips == None or args.TableName == None or args.LineCode == None:
            print('Regional GeoFips, LineCode, TableName required',
                  file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'GeoFIPS=%s&'
                  'TableName=%s&'
                  'LineCode=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('Regional', args.GeoFips, args.TableName,
                  args.LineCode,
                  args.Year,
                  args.format) )
        return params

    def UnderlyingGDPbyIndustryParams(self, args):
        if args.Frequency == None or args.Industry == None or args.TableID == None or \
           args.Year == None:
            print('UnderlyingGDPbyIndustryParameters TableID, Industry,'
                  'Frequency, Year required', file=sys.stderr)
            sys.exit()
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableID=%s&'
                  'Industry=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  ('UnderlyingGDPbyIndustry', args.TableID,
                  args.Industry,
                  args.Frequency, args.Year, args.format) )
        return params

# dict_keys(['TableName', 'SeriesCode', 'LineNumber', 'LineDescription', 'TimePeriod', 'METRIC_NAME', 'CL_UNIT', 'UNIT_MULT', 'DataValue', 'NoteRef'])
#
# {'TableName': 'FAAt101', 'SeriesCode': 'k1ttotl1es00', 'LineNumber': '2', 'LineDescription': 'Fixed assets', 'TimePeriod': '1926', 'METRIC_NAME': 'Current Dollars', 'CL_UNIT': 'Level', 'UNIT_MULT': '6', 'DataValue': '270,574', 'NoteRef': 'FAAt101'}

    def getNIPAdata(self, args):
        """ getNIPAdata(TableName, fq, yr, fmt)
        TableName - table name
        fq - frequency
        yr - year
        shm - show millions
        fmt - result format
        retrieve national income and product accounts data
        """
        params = self.NIPAParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('GetNIPAdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('GetNIPAdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getNIUnderlyingDetaildata(self, args):
        """ getNIUnderlyingDetaildata(TableName, fq, yr, fmt)
        TableName - table name
        fq - frequency
        yr - year
        fmt - result format
        retrieve national income underlying detail  data
        """
        params = self.NIUnderlyingDetailParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getNIUnderlyingDetaildata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getNIUnderlyingDetaildata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

# dict_keys(['Year', 'SeriesID', 'SeriesName', 'Row', 'ColumnGParent', 'ColumnParent', 'Column', 'RowCode', 'ColumnCode', 'ColumnParentCode', 'ColumnGParentCode', 'TableScale', 'DataValueUnformatted', 'TableColumnDisplayOrder', 'TableRowDisplayOrder', 'DataValue'])
# {'Year': '2012', 'SeriesID': '26', 'SeriesName': 'Debt Instruments Inflows', 'Row': 'Germany', 'ColumnGParent': 'None', 'ColumnParent': 'Manufacturing', 'Column': 'Total Manufacturing', 'RowCode': '308', 'ColumnCode': '3000', 'ColumnParentCode': '3000', 'ColumnGParentCode': '0', 'TableScale': 'Millions of Dollars', 'DataValueUnformatted': '-5422', 'TableColumnDisplayOrder': '2.00', 'TableRowDisplayOrder': '10.00', 'DataValue': '-5,422'}

    def getMNEdata(self, args):
        """ getMNEdata(doi, cl, ind, cnt, yr, fmt)
        sid - series id
        doi - direction of investment
        cl - classification
        ind - industry
        cnt - country
        yr  - yr
        fmt - result format
        return multinational enterprises data
        """
        params = self.MNEParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getMNEdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getMNEdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getFixedAssetsdata(self, args):
        """ getFixedAssetsdata()
        TableName - table name
        yr  - yr
        fmt - result format
        return fixed assets data
        """
        params = self.FixedAssetsParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getFixedAssetsdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getFixedAssetsdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getITAdata(self, args):
        """ getITAdata(ind, area, fq, yr, fmt)
        TableName - table name
        yr  - yr
        fmt - result format
        return international transactions accounts data
        """
        params = self.ITAParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getITAdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getITAdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getIIPdata(self, args):
        """ getIIPdata(ind, area, fq, yr, fmt)
        toi - type of investment
        cmp - component
        fq - frequency
        yr  - yr
        fmt - result format
        return international investment position data
        """
        params = self.IIPParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getIIPdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getIIPdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getInputOutputdata(self, args):
        """ getInputOutputdata(tid, yr, fmt)
        tid - table id
        yr- year
        fmt - result format
        return input output data
        """
        params = self.InputOutputParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getInputOutputtdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getInputOutputtdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getIntlServTradedata(self, args):
        """ getIntlServTradedata(ind, tos, td, aff, area, yr, fmt)
        tos - type of service
        td - trade direction
        aff - affiliation
        area - area or country
        yr  - yr
        fmt - result format
        return international service trade data
        """
        params = self.IntlServTradeParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getIntlServTradedata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getIntlServTradedata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getIntlServSTAdata(self, args):
        """ getIntlServSTAPdata( ch, dst, ind, area, yr, fmt)
        ch - channel
        dst - destination
        aff - affiliation
        ind - industry
        area - area or country
        yr  - yr
        fmt - result format
        return international services supplied through affiliates data
        """
        params = self.IntlServSTAParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getIntlServSTAdata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getIntlServSTAdata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getGDPbyIndustrydata(self, args):
        """ getGDPbyIndustrydata( ch, dst, ind, area, yr, fmt)
        tid = table id
        ind - industry 
        fq - frequency
        yr  - yr
        fmt - result format
        return gdp by industry data
        """
        params = self.GDPbyIndustryParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getGDPbyIndustrydata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getGDPbyIndustrydata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getRegionaldata(self, args):
        """ getRegionaldata(TableName, lc, fips, yr, fmt)
        TableName - table name
        lc - line code
        fips - geo fips code
        yr  - yr
        fmt - result format
        return regional data
        """
        params = self.RegionalParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getRegionaldata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getRegionaldata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def getUnderlyingGDPbyIndustrydata(self, args):
        """ getUnderlyingGDPbyIndustrydata(tid, ind, fq, yr, fmt)
        tid - table id
        ind - industry
        fq - frequency
        yr  - yr
        fmt - result format
        return underlying gdp by industry data
        """
        params = self.UnderlyingGDPbyIndustryParams(args)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('getRegionaldata: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        if rstr == None:
            print('getRegionaldata: no data', file=sys.stderr)
            return resp
        jsd = json.loads(rstr)
        if 'Results' not in jsd['BEAAPI'].keys():
            return None
        return jsd['BEAAPI']['Results']

    def makezipdir(self):
        """ makezipdir()
        create the directory to hold BEA zip files
        """
        zd = self.zipdir

        if os.path.exists(zd):
            if os.path.isdir(zd):
                return
            else:
                print('%s not a directory' % zd, file=sys.stderr)
                sys.exit()

        try:
            os.mkdir(zd)
        except Exception as e:
            print('makezipdir %s: %s' % (zd, e), file=sys.stderr)

    def clearzipfiles(self):
        """clearzipfiles()
        remove BEAzip files older than 1 week
        """
        tm = time.time()
        spd = 60 * 60 * 24
        spw = spd * 7
        bzfl = glob.glob('/tmp/BEA/BEA*.zip')
        if len(bzfl) == 0:
            return
        bzinfo = [(bnm, os.stat(bnm)) for bnm in bzfl]
        for bzn, bzs in bzinfo:
            if (tm - bzs) > spw:
                os.unlink(bzn)

    def loadzipfile(self, zfp, d, ds, dn, sk):
        """ loadzipfile(zfp, d, ds, dn, sk)
        zfp - zipfile file pointer
        d   - data
        ds  - dataset name
        dn  - qualifying parameter name
        sk  - split key
        """
        nms = {}
        dx=0
        if type(d) == type({}):
            aa = self.dd2aa(d, 'Data')
            if sk != None:
                asp = self.aasplit(aa, sk)
                for pk in asp['parts'].keys():
                    csv = self.aa2csv(asp['parts'][pk])
                    pk = re.sub("[,' :)(]", '', pk)
                    csvfn = '%s%s%s.csv' % (ds,dn,pk)
                    if csvfn in nms:
                        csvfn = '%s%s%s%d.csv' % (ds,dn,pk,dx)
                        dx += 1
                    zfp.writestr(csvfn, csv)
                    nms[csvfn]=1
            else:
                csv = self.aa2csv(aa)
                csvfn = '%s%s.csv' % (ds,dn)
                zfp.writestr(csvfn, csv)

        elif type(d) == type([]):
            for i in range(len(d)):
                aa = self.dd2aa(d[i], 'Data')
                if sk != None:
                    asp = self.aasplit(aa, sk)
                    for pk in asp['parts'].keys():
                        csv = self.aa2csv(asp['parts'][pk])
                        pk = re.sub("[,' :)(]", '', pk)
                        csvfn = '%s%s%s.csv' % (ds,dn,pk)
                        if csvfn in nms:
                            csvfn = '%s%s%s%d.csv' % (ds,dn,pk,dx)
                            dx += 1
                        zfp.writestr(csvfn, csv)
                        nms[csvfn]=1
                else:
                    csv = self.aa2csv(aa)
                    csvfn = '%s%s.csv' % (ds,dn)
                    zfp.writestr(csvfn, csv)

    def d2csvzipfile(self, d, args):
        """d2csvzipfile
        save csvfiles to a zipfile
        """

        self.makezipdir()
        self.clearzipfiles()

        ds = args.DatasetName
        dn = self.ds2dn(args)
        sk = args.splitkey
        if sk == None:
            sk = self.ds2sk(args)
        zfn = args.csvzipfn
        if zfn == None:
            zfn = '/tmp/BEA/BEA%s%s.zip' % (ds,dn)
        with zipfile.ZipFile(zfn, 'w', zipfile.ZIP_DEFLATED) as zfp:
            self.loadzipfile(zfp, d, ds, dn, sk)
            zfp.close()
            return zfn

    def dd2csv(self, jsd):
        """ dd2csv(jsd)
        jsd - results from BEA table query
        return csv text for table data
        """
        if 'Data' not in jsd.keys():
            print('dd2csv no Data key', file=sys.stderr)
            print(jsd, file=sys.stderr)
            return None
        aa = self.dd2aa(jsd, 'Data')
        csv = self.aa2csv(aa)
        return csv

    def store2csv(self, d, fn):
        """store2csv(d, fn)
        d - results from table query
        fn - where to store the csv data
        """
        if type(d) == type({}):
            csv = self.dd2csv(d)
            with open(fn, 'w') as fp:
                print(csv, file=fp)
        elif type(d) == type([]):
            if not fn.endswith('csv'):
                print('csv filename must end with ".csv"', file=sys.stderr)
            for i in range(len(d)):
                csv = self.dd2csv(d[i])
                nfn = fn.replace('.csv', '%d.csv' % i)
                with open(fn, 'w') as fp:
                    print(csv, file=fp)

    def print2csv(self, d):
        """print2csv(d)
        d - results of table query
        print csv result to stdout
        """
        if type(d) == type({}):
            csv = self.dd2csv(d)
            print(csv)
        elif type(d) == type([]):
            for i in range(len(d)):
                print('\n\n\n')
                csv = self.dd2csv(d[i])
                print(csv)

    def paa2plots(self, parts, xk, yk, uk, t):
        """ paa2plots(self, aa, x, y, sk, t)
        parts - plot aa parts
        xk - key to x axis data
        yk - key to y axis data
        uk - key to y axis units
        t - plot title
        return plot figure for data in parts
        """
        fig  = make_subplots(shared_yaxes=True, shared_xaxes=True)
        xi = yi = ui = None

        units = None
        for k in parts.keys():
            aa = parts[k]
            if xi == None:
                for i in range(len(aa[0])):
                    if aa[0][i] == xk:
                        xi = i
                    elif aa[0][i] == yk:
                        yi = i
                    elif aa[0][i] == uk:
                        ui = i
            if xi == None:
                print('paa2plots bad xkey %s' % xk, file=sys.stderr)
                sys.exit()
            if yi == None:
                print('paa2plots bad ykey %s' % yk, file=sys.stderr)
                sys.exit()

            if uk.endswith('?'):
                units = uk
            if units == None:
                if ui == None:
                    print('paa2plots bad unitskey %s' % uk, file=sys.stderr)
                    sys.exit()
                units = aa[1][ui]

            xa = []
            ya = []
            for i in range(1, len(aa)):
                xa.append(aa[i][xi])
                ya.append(aa[i][yi])
            fig.add_trace( go.Scatter(x=xa, y=ya, name=k))

        fig.update_layout(
            title=t,
            yaxis_title=units,
            xaxis_title='Date',
        )
        return fig


    def aa2plot(self, aa, xi, yi, ui, t):
        """ aa2plot(self, aa, x, y, t)
        aa - array of arrays
        xi - x index
        yi - y index
        ui - index to units
        t - plot title
        return plot figure
        """
        if xi == None:
            print('aa2plot bad xi %s' % xi, file=sys.stderr)
            sys.exit()
        if yi == None:
            print('aa2plot bad yi %s' % yi, file=sys.stderr)
            sys.exit()

        fig  = make_subplots(shared_yaxes=True, shared_xaxes=True)

        xa = []
        ya = []
        units = aa[1][ui]
        if aa[0][ui] == 'DataValue':
            units = 'Billions?'
        for i in range(len(aa)):
            xa.append(aa[i][xi])
            ya.append(aa[i][yi])

        fig.add_trace( go.Scatter(x=xa, y=ya, name=t))

        fig.update_layout(
            title=t,
            yaxis_title=units,
            xaxis_title='Date',
        )
        return fig

    def aa2table(self, cap, aa):
       """ aa2table(aa)

       convert array of arrays to an html table
       aa - array of arrays
       """
       tbla = []
       # table
       tbla.append('<table border="1">')
       # table header
       hdra = aa[0]
       hdr = '</th><th>'.join(hdra)
       tbla.append('<tr><th scope="col">%s</th></tr>' % (hdr) )
       cap = '<caption>%s</caption>' % cap
       tbla.append(cap)
       # table rows
       for i in range(1, len(aa) ):
           rowa = aa[i]
           for j in range(len(rowa)):
               if rowa[j] == None:
                   rowa[j] = ''
               elif type(rowa[j]) == type(1):
                   rowa[j] = '%d' % rowa[j]
           row = '</td><td>'.join(rowa)
           tbla.append('<tr><td>%s</td></tr>' % (row) )

       # close
       tbla.append('</table>')
       return tbla


    def x2aa(self, dss, jsk):
        """ x2dict(dss)
        dss - string containing XML
        convert string result to array of arrays
        """
        root = ET.fromstring(dss)
        keys = []
        aa = []
        for c in root:
            for gc in c:
                if c.tag == 'Results':
                    print(c.tag, c.attrib, gc.tag, gc.attrib)
                    if len(aa) == 0:
                        keys = [k for k in gc.attrib.keys()]
                        aa.append(keys)
                    a = []
                    for k in keys:
                        a.append(gc.attrib[k])
                    aa.append(a)
        return aa


    def dd2aa(self, dsd, jsk):
        """ dd2aa(dss)
        dss - string containing json
        convert string result to array of arrays
        """
        if type(dsd[jsk]) == type({}):
            keys = [k for k in dsd[jsk].keys()]
            aa = []
            aa.append(keys)
            a = []
            d = dsd[jsk]
            for k in keys:
                if k not in d:
                    a.append('')
                else:
                    a.append(d[k])
            aa.append(a)
            return aa
        elif type(dsd[jsk]) == type([]):
            keys = [k for k in dsd[jsk][0].keys()]
            aa = []
            for d in dsd[jsk]:
                if len(aa) == 0:
                    aa.append(keys)
                a = []
                for k in keys:
                    if k not in d:
                        a.append('')
                    else:
                        a.append(d[k])
                aa.append(a)
            return aa
        else:
            print('dd2aa type error', file=sys.stderr)
            return None

    def js2aa(self, dss, jsk):
        """ js2aa(dss)
        dss - string containing json
        convert string result to array of arrays
        """
        dsd = json.loads(dss)

        if type(dsd['BEAAPI']['Results'][jsk]) != type([]):
            keys = [k for k in dsd['BEAAPI']['Results'][jsk].keys()]
            aa = []
            aa.append(keys)
            a = []
            for k in keys:
                a.append(dsd['BEAAPI']['Results'][jsk][k])
            aa.append(a)
            return aa


        keys = [k for k in dsd['BEAAPI']['Results'][jsk][0].keys()]
        aa = []
        for d in dsd['BEAAPI']['Results'][jsk]:
            if len(aa) == 0:
                aa.append(keys)
            a = []
            for k in keys:
                if k not in d:
                    a.append('')
                else:
                    if d[k].endswith(' '):
                        d[k] = d[k][0:-1]
                    a.append(d[k])
            aa.append(a)
        return aa

    def aasplit(self, aa, k):
        """ aasplit(self, aa, k)
        aa - array of arrays
        k - split key
        return aa split on k
        """
        ai = None # index to split key
        asp = {}
        asp['parts'] = {}
        keys = aa[0]
        for i in range(len(aa[0])):
            if aa[0][i] == k:
                ai = i
                break
        if ai == None:
            print('aasplit no key %s' % k, file=sys.stderr)
            sys.exit()
        for j in range(1, len(aa)):
            if aa[j][ai] not in asp['parts']:
                asp['parts'][aa[j][ai]] = []
                asp['parts'][aa[j][ai]].append(keys)
            asp['parts'][aa[j][ai]].append(aa[j])

        return asp

    def ds2uk(self, args):
        """ds2uk(args)
        args - command arguments
        return y axis units key
        """
        if args.DatasetName in ['NIPA', 'NIUnderlyingDetail', 'FixedAssets']:
            uk = 'METRIC_NAME'
        elif args.DatasetName in ['InputOutput']:
            uk = 'ColType'
        elif args.DatasetName in ['GDPbyIndustry', 'UnderlyingGDPbyIndustry']:
            uk = 'Billions?'
        elif args.DatasetName in ['MNE']:
            uk = 'TableScale'
        elif args.DatasetName in ['IIP', 'Regional']:
            uk = 'CL_UNIT'
        elif args.DatasetName in ['ITA', 'IntlServTrade', 'IntlServSTA']:
            uk = 'CL_UNIT'
        else:
            return None
        return uk

    def ds2xk(self, args):
        """ds2xk(args)
        args - command arguments
        return x key
        """
        if args.DatasetName in ['NIPA', 'NIUnderlyingDetail', 'FixedAssets',
                            'Regional']:
            xk = 'TimePeriod'
        elif args.DatasetName in ['InputOutput']:
            xk = 'Year'
        elif args.DatasetName in ['GDPbyIndustry', 'UnderlyingGDPbyIndustry']:
            xk = 'Year'
        elif args.DatasetName in ['MNE']:
            xk = 'Year'
        elif args.DatasetName in ['IIP']:
            xk = 'Year'
        elif args.DatasetName in ['ITA', 'IntlServTrade', 'IntlServSTA']:
            xk = 'Year'
        else:
            return None
        return xk


    def ds2yk(self, args):
        """ds2yk(args)
        args - command arguments
        return y key
        """
        if args.DatasetName in ['NIPA', 'NIUnderlyingDetail', 'FixedAssets',
                            'Regional']:
            yk = 'DataValue'
        elif args.DatasetName in ['InputOutput']:
            yk = 'DataValue'
        elif args.DatasetName in ['GDPbyIndustry', 'UnderlyingGDPbyIndustry']:
            yk = 'DataValue'
        elif args.DatasetName in ['MNE']:
            yk = 'DataValue'
        elif args.DatasetName in ['IIP']:
            yk = 'DataValue'
        elif args.DatasetName in ['ITA', 'IntlServTrade', 'IntlServSTA']:
            yk = 'DataValue'
        else:
            return None
        return yk

    def ds2sk(self, args):
        """ds2sk(args)
        args - command arguments
        return split key
        """
        if args.DatasetName in ['NIPA', 'NIUnderlyingDetail', 'FixedAssets']:
            sk = 'SeriesCode'
        elif args.DatasetName in ['InputOutput']:
            sk = 'ColDescr'
        elif args.DatasetName in ['GDPbyIndustry', 'UnderlyingGDPbyIndustry']:
            sk = 'IndustrYDescription'
        elif args.DatasetName in ['MNE']:
            #sk = args.SeriesID
            sk = 'SeriesName'
        elif args.DatasetName in ['IIP']:
            sk = 'Component'
        elif args.DatasetName in ['ITA', 'IntlServTrade', 'IntlServSTA']:
            sk = 'TimeSeriesDescription'
        elif args.DatasetName in ['Regional']:
            sk = 'GeoName'
        else:
            return None
        return sk


    def ds2dn(self, args):
        """ds2dn(args)
        args - command arguments
        return qualifying parameter name for dataset
        """
        if args.DatasetName in ['NIPA', 'NIUnderlyingDetail', 'FixedAssets',
                            'Regional']:
            dn = args.TableName
        elif args.DatasetName in ['InputOutput', 'GDPbyIndustry',
                              'UnderlyingGDPbyIndustry']:
            dn = args.TableID
        elif args.DatasetName in ['MNE']:
            #dn = args.SeriesID
            dn = args.DirectionOfInvestment
        elif args.DatasetName in ['IIP']:
            dn = args.TypeOfInvestment
        elif args.DatasetName in ['ITA']:
            dn = args.Indicator
        elif args.DatasetName in ['IntlServTrade']:
            dn = args.TypeOfService
        elif args.DatasetName in ['IntlServSTA']:
            dn = args.Channel
        else:
            dn =  'Unkown'
        return dn

    def xiyiui(self, hdr, xk, yk, uk):
        """xiyiui(hdr, xk, yk, uk)
        hdr - aa header
        xk  - header value for plot x axis
        yk  - header value for plot y axis
        uk  - header value for y axis units
        """
        xi = yi = ui = None
        for i in range(len(hdr)):
            if hdr[i] == xk:
                xi = i
            elif hdr[i] == yk:
                yi = i
            elif hdr[i] == uk:
                ui = i
        # GDP datasets have no units data
        if ui == None:
            for i in range(len(hdr)):
                if hdr[i] == 'DataValue':
                    ui = i
                    break
        return xi, yi, ui

    def d2html(self, d, args):
        """d2html(d, ds, d, sk, xk, yk, uk)
        d - dictionary from table query
        fn - name of file to store html
        sk - split the data based on field name or None
        xk - key to x axis data
        yk - key to y axis data
        uk - key to y axis units
        """

        ds = args.DatasetName
        dn = self.ds2dn(args)
        sk = args.splitkey
        if sk == None:
            sk = self.ds2sk(args)
        xk = args.xkey
        if xk == None:
            xk = self.ds2xk(args)
        yk = args.ykey
        if yk == None:
            yk = self.ds2yk(args)
        uk = args.unitskey
        if uk == None:
            uk = self.ds2uk(args)

        htmla = []
        htmla.append('<html>')
        ttl = 'BEA Dataset %s Table %s' % (ds, dn)
        htmla.append('<head>')
        htmla.append('<title>%s</title>' % (ttl) )
        htmla.append('<script src="https://cdn.plot.ly/plotly-2.32.0.min.js" charset="utf-8"></script>')
        htmla.append('</head>')
        if type(d) == type({}):
            aa = self.dd2aa(d, 'Data')
            if sk != None:
                asp = self.aasplit(aa, sk)

                for pk in asp['parts'].keys():
                    xi, yi, ui = self.xiyiui(asp['parts'][pk][0], xk, yk, uk)
                    fig = self.aa2plot(asp['parts'][pk], xi, yi, ui, '%s %s' %
                          (ds, dn))
                    figjs = fig.to_json()
                    htmla.append('<div id="fig%s%s%s">' % (ds,dn,pk) )
                    htmla.append('<script>')
                    htmla.append('var figobj = %s;\n' % figjs)
                    htmla.append('Plotly.newPlot("fig%s%s%s", figobj.data, figobj.layout, {});' % (ds,dn,pk) )
                    htmla.append('</script>')
                    htmla.append('</div>')

                    pttl = '%s %s' % (ttl, pk)
                    ptbla = self.aa2table(pttl, asp['parts'][pk])
                    htmla.extend(ptbla)
            else:
                tbla = self.aa2table(ttl, aa)
                htmla.extend(tbla)
        elif type(d) == type([]):
            for i in range(len(d)):
                aa = self.dd2aa(d[i], 'Data')
                if sk != None:
                    asp = self.aasplit(aa, sk)

                    for pk in asp['parts'].keys():
                        xi, yi, ui = self.xiyiui(asp['parts'][pk][0],
                                      xk, yk, uk)
                        fig = self.aa2plot(asp['parts'][pk], xi, yi, ui, '%s %s' %
                                             (ds, dn))
                        figjs = fig.to_json()
                        htmla.append('<div id="fig%s%s%s">' % (ds,dn,pk) )
                        htmla.append('<script>')
                        htmla.append('var figobj = %s;\n' % figjs)
                        htmla.append('Plotly.newPlot("fig%s%s%s", figobj.data, figobj.layout, {});' % (ds,dn,pk) )
                        htmla.append('</script>')
                        htmla.append('</div>')

                        pttl = '%s %d %s' % (ttl, i, pk)
                        ptbla = self.aa2table(pttl, asp['parts'][pk])
                        htmla.extend(ptbla)
                else:
                    tbla = self.aa2table('%s %d' % (ttl, i), aa)
                    htmla.extend(tbla)
        htmla.append('</html>')
        return ''.join(htmla)


    def aa2csv(self, aa):
        """aa2csv(aa)
        aa - array of arrays
        return csv text rendition of aa
        """
        csva = []
        for a in aa:
            csva.append('"%s"' % '","'.join(a))
        return '\n'.join(csva)

    def dsparamvals(self, ds, param, fmt):
        """ dsparamvale(ds, param, fmt)
        ds - dataset name
        param - parameter name
        fmt - result format
        retrieve parameter values for BEA dataset parameter
        """
        params = ('&method=GetParameterValues&'
                  'Datasetname=%s&'
                  'ParameterName=%s&'
                  'ResultFormat=%s' % (ds, param, fmt))
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('dsparamvale: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        return rstr

    def dsparams(self, ds, fmt):
        """ dsparams(ds, fmt)
        ds - dataset name
        fmt - result format
        retrieve parameter list for a BEA dataset
        """
        params = ('&method=GetParameterList&'
                  'Datasetname=%s&'
                  'ResultFormat=%s' % (ds, fmt))
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('dsparams: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        return rstr

    def datasets(self, fmt):
        """ datasets(fmt)
        fmt - result format
        retrieve BEA datasets list
        """
        params = ('&method=GetDatasetList&'
                  'ResultFormat=%s' % fmt)
        url = self.burl + params
        resp = self.uq.query(url)
        if resp == None:
            print('datasets: no response', file=sys.stderr)
            return resp
        rstr = resp.read().decode('utf-8')
        return rstr

    def hierarchyhtml(self, hier):
        """ hierarchyhtml(hier)
        hier - dictionary of BEA data model
        return html page for BEA data model
        """
        htmla = []
        htmla.append('<html>')
        ttl = 'BEA Dataset Data Hierarchy'
        htmla.append('<head><h1>%s</h1></head>' % (ttl) )
        dsaa = hier['Datasets']
        tbl = self.aa2table('Datasets', dsaa)
        htmla.extend(tbl)
        for i in range(1, len(dsaa)):
            dsn = dsaa[i][0]
            paa = hier[dsn]['Parameter']
            tbl = self.aa2table('%s Parameters' % dsn, paa)
            htmla.extend(tbl)
            for j in range(1, len(paa)):
                pn = paa[j][0]
                pvaa = hier[dsn]['ParameterValue'][pn]
                tbl = self.aa2table('%s Parameter %s Values' % (dsn, pn), pvaa)
                htmla.extend(tbl)
        htmla.append('</html>')
        return ''.join(htmla)

    def showhtml(self, fn, html):
        with open(fn, 'w') as fp:
            fp.write(html)
        webbrowser.open('file://%s' % fn)

    def hierarchy(self, fmt):
        """ hierarchy(fmt)
        fmt - result format
        retrieve BEA data model
        """
        hier = {}
        dss = self.datasets(fmt)
        if fmt == 'json':
            dsaa = self.js2aa(dss, 'Dataset')
        else:
           dsaa = self.x2aa(dss, 'Dataset')
        hier['Datasets'] = dsaa
        for i in range(1, len(dsaa)):
            dsn = dsaa[i][0]
            hier[dsn] = {}
            pss = self.dsparams(dsn, fmt)
            if fmt == 'json':
                paa = self.js2aa(pss, 'Parameter')
            else:
                paa = self.x2aa(pss, 'Parameter')
            hier[dsn]['Parameter'] = paa
            hier[dsn]['ParameterValue'] = {}
            for j in range(1, len(paa)):
                pn = paa[j][0]
                psv = self.dsparamvals(dsn, pn, fmt)
                if fmt == 'json':
                    vaa = self.js2aa(psv, 'ParamValue')
                else:
                    vaa = self.x2aa(psv, 'ParamValue')
                hier[dsn]['ParameterValue'][pn] = vaa
        return hier

#
def main():
    argp = argparse.ArgumentParser(description='get BEA data')

    argp.add_argument('--DatasetName', choices=['NIPA', 'NIUnderlyingDetail', 'MNE',
                      'FixedAssets', 'ITA', 'IIP', 'InputOutput',
                      'IntlServTrade', 'IntlServSTA', 'GDPbyIndustry',
                      'Regional', 'UnderlyingGDPbyIndustry',
                      'APIDatasetMetaData'],
                      help='dataset name')

    argp.add_argument('--TableName', help='NIPA NIUnderlyingDetail '
                                      'FixedAssets Regional table name')
    argp.add_argument('--TableID', help='InputOutput GDPbyIndustry '
                                      'UnderlyingGDPbyIndustry table id')
    argp.add_argument('--SeriesID', help='MNE series id')

    argp.add_argument('--ShowMillions', default='N',
                      help='NIPA show millions')
    argp.add_argument('--Frequency',
                     help='frequency M, Q, A or comma separated list')
    argp.add_argument('--Year',
                      help='year YYYY  X or all')

    argp.add_argument('--DirectionOfInvestment',
                      choices = ['inward', 'outward', 'parent', 'state'],
                      help='MNE direction of investment ')
    argp.add_argument('--Classification', help='MNE classification')
    argp.add_argument('--Industry', help='MNE IntlServSTA GDPbyIndustry '
                                    'UnderlyingGDPbyIndustry Industry')
    argp.add_argument('--Country', help='MNE country')

    argp.add_argument('--Indicator', help='ITA indicator')
    argp.add_argument('--AreaOrCountry', help='ITA IntlServTrade IntlServSTA '
                                    'area or country')

    argp.add_argument('--TypeOfInvestment', help='IIP type of investment')
    argp.add_argument('--Component', help='IIP component')

    argp.add_argument('--TypeOfService', help='IntlServTrade type of service')
    argp.add_argument('--TradeDirection', help='IntlServTrade trade direction')
    argp.add_argument('--Affiliation', help='IntlServTrade affiliation')

    argp.add_argument('--Channel', help='IntlServSTA channel')
    argp.add_argument('--Destination', help='IntlServSTA destination')

    argp.add_argument('--GeoFips', help='Regional geo FIPS')
    argp.add_argument('--LineCode', help='Regional line code')

    argp.add_argument('--csvfn', \
         help='name of file to store dataset CSV result')
    argp.add_argument('--csvzipfn', \
         help='name of zip file to store dataset CSV results')

    argp.add_argument('--splitkey',
        help='table column name to use to split the table')
    argp.add_argument('--xkey',
        help='table column name to use to plot the data')
    argp.add_argument('--ykey', default='DataValue',
        help='table column name to use to plot the data')
    argp.add_argument('--unitskey',
        help='table column name to use to label the data')
    argp.add_argument('--htmlfn', \
        help='name of file to store dataset HTML result')

    argp.add_argument('--format', default='json',
                      choices=['json', 'XML'], help='query result format')

    argp.add_argument('--hierarchy',
                      action='store_true', default=False,
                      help='BEA data model ')
    argp.add_argument('--tableregister',
                      action='store_true', default=False,
                      help='get NIPA table register ')

    args=argp.parse_args()

    BN = BEAQueryQ()
    BN.args = args

    if args.tableregister:
       txt = BN.getNIPAregister()
       print(txt)
    elif args.TableName:
        d = None
        if args.DatasetName == None:
            print('dataset required to print dataset tables')
            argp.print_help()
            sys.exit()
        if args.DatasetName == 'NIPA':
            if args.Frequency == None or args.Year == None:
                argp.print_help()
                sys.exit()
            d = BN.getNIPAdata(args)
        elif args.DatasetName == 'NIUnderlyingDetail':
            d = BN.getNIUnderlyingDetaildata(args)
        elif args.DatasetName == 'FixedAssets':
            d = BN.getFixedAssetsdata(args)
        elif args.DatasetName == 'Regional':
            d = BN.getRegionaldata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.TableID:
        d = None
        if args.DatasetName =='InputOutput':
            d = BN.getInputOutputdata(args)
        elif args.DatasetName == 'GDPbyIndustry':
            d = BN.getGDPbyIndustrydata(args)
        elif args.DatasetName == 'UnderlyingGDPbyIndustry':
            d = BN.getUnderlyingGDPbyIndustrydata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.SeriesID:
        d = None
        if args.DatasetName == 'MNE':
            d = BN.getMNEdata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.TypeOfInvestment:
        d = None
        if args.DatasetName == 'IIP':
            d = BN.getIIPdata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.Indicator:
        d = None
        if args.DatasetName == 'ITA':
            d = BN.getITAdata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.TypeOfService:
        d = None
        if args.DatasetName == 'IntlServTrade':
            d = BN.getIntlServTradedata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.Channel:
        d = None
        if args.DatasetName == 'IntlServSTA':
            d = BN.getIntlServSTAdata(args)
        else:
            argp.print_help()
            sys.exit()
    elif args.hierarchy:
        hd = BN.hierarchy(args.format)
        htm = BN.hierarchyhtml(hd)
        BN.showhtml('/tmp/hierarchy.html', htm)
    else:
        argp.print_help()
        sys.exit()

    if d == None or type(d) == type({}) and 'Data' not in d.keys():
        print('beaqueryq: no data', file=sys.stderr)
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
