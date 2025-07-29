#! /usr/bin/python

import os
import sys
import time
import types
import json
import itertools


#try:
#    from beaquery import beaqueryq
#except Exception as e:
#    import beaqueryq

import beaqueryq

class TestBQQ():

    def __init__(self):
        self.jsf = 'beahierarchy.json'

        self.BQQ = beaqueryq.BEAQueryQ()

    # dictionary to namespace
    def d2ns(self, qsd):
        """ d2ns(qsd)
        qsd - python dictionary
        convert dictionary to types.SimpleNamespace
        """
        args = types.SimpleNamespace()
        for k in qsd.keys():
            args.__dict__[k] = qsd[k]
        return args

    def dscp2ns(self, js, ds, dsp, p):
        qsd={}
        qsd['DatasetName'] = ds
        qsd['format'] = 'CSV'
        for i in range(len(dsp['Parameters'])):
            pn = [k for k in dsp['Parameters'][i].keys()][0]
            pv = p[i]
            qsd[pn] = pv
        return self.d2ns(qsd)

    def cp2parameters(self, js, ds, dsp):
        k0 = [k for k in dsp['Parameters'][0].keys()][0]
        k1 = [k for k in dsp['Parameters'][1].keys()][0]
        cp = itertools.product(dsp['Parameters'][0][k0],
                               dsp['Parameters'][1][k1])
        return cp

    def cp3parameters(self, js, ds, dsp):
        k0 = [k for k in dsp['Parameters'][0].keys()][0]
        k1 = [k for k in dsp['Parameters'][1].keys()][0]
        k2 = [k for k in dsp['Parameters'][2].keys()][0]
        cp = itertools.product(dsp['Parameters'][0][k0],
                               dsp['Parameters'][1][k1],
                               dsp['Parameters'][2][k2])
        return cp

    def cp4parameters(self, js, ds, dsp):
        k0 = [k for k in dsp['Parameters'][0].keys()][0]
        k1 = [k for k in dsp['Parameters'][1].keys()][0]
        k2 = [k for k in dsp['Parameters'][2].keys()][0]
        k3 = [k for k in dsp['Parameters'][3].keys()][0]
        cp = itertools.product(dsp['Parameters'][0][k0],
                               dsp['Parameters'][1][k1],
                               dsp['Parameters'][2][k2],
                               dsp['Parameters'][3][k3])
        return cp

    def cp5parameters(self, js, ds, dsp):
        k0 = [k for k in dsp['Parameters'][0].keys()][0]
        k1 = [k for k in dsp['Parameters'][1].keys()][0]
        k2 = [k for k in dsp['Parameters'][2].keys()][0]
        k3 = [k for k in dsp['Parameters'][3].keys()][0]
        k4 = [k for k in dsp['Parameters'][4].keys()][0]
        cp = itertools.product(dsp['Parameters'][0][k0],
                               dsp['Parameters'][1][k1],
                               dsp['Parameters'][2][k2],
                               dsp['Parameters'][3][k3],
                               dsp['Parameters'][4][k4])
        return cp

    def cp12parameters(self, js, ds, dsp):
        k0 = [k for k in dsp['Parameters'][0].keys()][0]
        k1 = [k for k in dsp['Parameters'][1].keys()][0]
        k2 = [k for k in dsp['Parameters'][2].keys()][0]
        k3 = [k for k in dsp['Parameters'][3].keys()][0]
        k4 = [k for k in dsp['Parameters'][4].keys()][0]
        k5 = [k for k in dsp['Parameters'][5].keys()][0]
        k6 = [k for k in dsp['Parameters'][6].keys()][0]
        k7 = [k for k in dsp['Parameters'][7].keys()][0]
        k8 = [k for k in dsp['Parameters'][8].keys()][0]
        k9 = [k for k in dsp['Parameters'][9].keys()][0]
        k10 = [k for k in dsp['Parameters'][10].keys()][0]
        k11 = [k for k in dsp['Parameters'][11].keys()][0]
        cp = itertools.product(dsp['Parameters'][0][k0],
                               dsp['Parameters'][1][k1],
                               dsp['Parameters'][2][k2],
                               dsp['Parameters'][3][k3],
                               dsp['Parameters'][4][k4],
                               dsp['Parameters'][5][k5],
                               dsp['Parameters'][6][k6],
                               dsp['Parameters'][7][k7],
                               dsp['Parameters'][8][k8],
                               dsp['Parameters'][9][k9],
                               dsp['Parameters'][10][k10],
                               dsp['Parameters'][11][k11])
        return cp

    def cpNparameters(self, js, ds, dsp):
        n = len(dsp['Parameters'])
        # try to control combinatorial explosion
        for i in range(n):
            k = [k for k in dsp['Parameters'][i].keys()][0]
            if len(dsp['Parameters'][i][k]) > 5:
                dsp['Parameters'][i][k] = dsp['Parameters'][i][k][-5:]
        if n == 2:
            return self.cp2parameters(js, ds, dsp)
        elif n ==3:
            return self.cp3parameters(js, ds, dsp)
        elif n == 4:
            return self.cp4parameters(js, ds, dsp)
        elif n == 5:
            return self.cp5parameters(js, ds, dsp)
        elif n == 12:
            return self.cp12parameters(js, ds, dsp)
        else:
            print('cpNparameters: %d parameters' % (n), file=sys.stderr)
            return None

    def collectdatasetparams(self, js, ds):
        dsp = {}
        dsp['DatasetName'] = ds
        dsp['Parameters'] = []
        for i in range(1, len(js[ds]['Parameter'])):
            pn = js[ds]['Parameter'][i][0]
            # TableID and TableName are duplicates for these datasets
            if ds in ['NIPA', 'NIUnderlyingDetail'] and pn == 'TableID':
                continue
            pvd = {}
            pvd[pn] = []
            mv=''
            av=''
            if len(js[ds]['Parameter'][i]) == 7:
                mv = js[ds]['Parameter'][i][-2]    # multiple values
                av = js[ds]['Parameter'][i][-1]    # all value
                if av != '':
                    pvd[pn].append(av)
            elif len(js[ds]['Parameter'][i]) <= 6:
                mv = js[ds]['Parameter'][i][-1]
            # Year is complicated for these datasets
            if ds in ['NIPA', 'NIUnderlyingDetail'] and pn == 'Year':
                dsp['Parameters'].append(pvd)
                continue
            if pn not in js[ds]['ParameterValue']: # XXX fix me
                print('%s no PV %s' % (ds, js[ds]['Parameter'][i]))
            else:
                for j in range(1, len(js[ds]['ParameterValue'][pn])):
                    pv = js[ds]['ParameterValue'][pn][j][0]
                    pvd[pn].append(pv)
            if mv != '' and av != '' and len(pvd[pn]) > 2:
                pvd[pn].append('%s,%s' % (pvd[pn][1], pvd[pn][2]))
            elif mv != '':
                pvd[pn].append('%s,%s' % (pvd[pn][0], pvd[pn][1]))
            dsp['Parameters'].append(pvd)
        return dsp

    def cpdatasetparameters(self, js, ds, dsp):
        cp = self.cpNparameters(js, ds, dsp)
        return cp

    def prmbqq(self, args):
        ds = args.DatasetName
        if ds == 'NIPA':
            return self.BQQ.NIPAParams(args)
        elif ds == 'NIUnderlyingDetail':
            return self.BQQ.NIUnderlyingDetailParams(args)
        elif ds == 'MNE':
            return self.BQQ.MNEParams(args)
        elif ds == 'FixedAssets':
            return self.BQQ.FixedAssetsParams(args)
        elif ds == 'ITA':
            return self.BQQ.ITAParams(args)
        elif ds == 'IIP':
            return self.BQQ.IIPParams(args)
        elif ds == 'InputOutput':
            return self.BQQ.InputOutputParams(args)
        elif ds == 'IntlServTrade':
            return self.BQQ.IntlServTradeParams(args)
        elif ds == 'IntlServSTA':
            return self.BQQ.IntlServSTAParams(args)
        elif ds == 'GDPbyIndustry':
            return self.BQQ.GDPbyIndustryParams(args)
        elif ds == 'Regional':
            return self.BQQ.RegionalParams(args)
        elif ds == 'UnderlyingGDPbyIndustry':
            return self.BQQ.UnderlyingGDPbyIndustryParams(args)
        else:
            print('prmbqq: %s' %(ds), file=sys.stderr)
            sys.exit()

    def callbqq(self, args):
        ds = args.DatasetName
        if ds == 'NIPA':
            return self.BQQ.getNIPAdata(args)
        elif ds == 'NIUnderlyingDetail':
            return self.BQQ.getNIUnderlyingDetaildata(args)
        elif ds == 'MNE':
            return self.BQQ.getMNEdata(args)
        elif ds == 'FixedAssets':
            return self.BQQ.getFixedAssetsdata(args)
        elif ds == 'ITA':
            return self.BQQ.getITAdata(args)
        elif ds == 'IIP':
            return self.BQQ.getIIPdata(args)
        elif ds == 'InputOutput':
            return self.BQQ.getInputOutputdata(args)
        elif ds == 'IntlServTrade':
            return self.BQQ.getIntlServTradedata(args)
        elif ds == 'IntlServSTA':
            return self.BQQ.getIntlServSTAdata(args)
        elif ds == 'GDPbyIndustry':
            return self.BQQ.getGDPbyIndustrydata(args)
        elif ds == 'Regional':
            return self.BQQ.getRegionaldata(args)
        elif ds == 'UnderlyingGDPbyIndustry':
            return self.BQQ.getUnderlyingGDPbyIndustrydata(args)
        else:
            print('callbqq: %s' %(ds), file=sys.stderr)
            sys.exit()

    def testdatasets(self, jsf):
        with open(jsf) as jfp:
            js = json.load(jfp)
            dsa = js['Datasets']
            for i in range(1, len(dsa)):
                print(dsa[i])
                ds = dsa[i][0]
                if ds == 'APIDatasetMetaData':
                    continue
                dsp = self.collectdatasetparams(js, ds)
                cp = self.cpdatasetparameters(js, ds, dsp)
                if cp == None:
                    print('testdatasets: %s no cp' % (ds))
                    return
                cpa = list(cp)
                for p in cpa:
                    # print(p)
                    args = self.dscp2ns(js, ds, dsp, p)
                    #try:
                    #    prm = self.prmbqq(args)
                    #except Exception as e:
                    #    print('%s %s %e' % (ds, e, p))
                    try:
                        csv = self.callbqq(args)
                        time.sleep(0.5)
                    except Exception as e:
                        print('%s %s %e' % (ds, e, args))


def main():
    TB = TestBQQ()
    TB.testdatasets(TB.jsf)

if __name__ == '__main__':
    main()
