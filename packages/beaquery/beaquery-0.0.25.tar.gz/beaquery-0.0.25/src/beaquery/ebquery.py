
import os
import sys
import time
import urllib.request
from functools import partial

class _EBURLQuery():

    def __init__(self):
        self.chunksize =4294967296 # 4M

    def query(self, url):
        """query(url) - query a url

         retrieve contents of a URL with exponential backoff
         url - url of file to retrieve
        """
        ntries = 5
        tries = 0
        pause = 2
        if not url:
            print('query: nothing to do', file=sys.stderr)
            sys.exit(0)

        while True:
            try:
                req = urllib.request.Request(url)
            except Exception as e:
                print('query request %s failed %s' % (url, e), file=sys.stderr)
                if 'Not Found' in e.reason:
                    return None
                if 'Forbidden' in e.reason:
                    return None
            try:
                resp = urllib.request.urlopen(req)
            except Exception as e:
                print('query urlopen %s failed %s' % (url, e), file=sys.stderr)
                if 'Not Found' in e.reason:
                    return None
                if 'Forbidden' in e.reason:
                    return None
                if tries < ntries:
                    print('retrying in %d seconds' % (pause),
                        file=sys.stderr)
                    time.sleep(pause)
                    tries = tries + 1
                    pause = pause * 2
                    continue
                #sys.exit(1)
            return resp

    def storequery(self, qresp, file):
        """storequery(qresp, file) - store the query response in a file

        resp - the query response
        file   - filename that will hold the query response
        """
        if not qresp: 
            print('storequery: no content', file=sys.stderr)
            sys.exit(1)
        if not file:
            print('storequery: no output filename', file=sys.stderr)
            sys.exit(1)
        of = os.path.abspath(file)
        # some downloads can be somewhat large
        with open(of, 'wb') as f:
            parts = iter(partial(qresp.read, self.chunksize), b'')
            for c in parts:
                f.write(c)
            #if c: f.write(c)
            f.flush()
            os.fsync(f.fileno() )
            return

