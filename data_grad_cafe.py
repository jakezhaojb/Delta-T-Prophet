#! /usr/bin/env python
# coding: utf-8

import os
import sys
import urllib2
import re
from dpark import DparkContext

HOST = 'http://thegradcafe.com/survey/index.php?q='
OUTPUT = '' # TODO
SUB = ''
LEVEL = ''
START_PAGE = 1
END_PAGE = 100


def proc_glob():
    """Process global objects"""
    assert HOST.find('http://thegradcafe.com/survey/index.php?q=') is 0
    # OUTPUT
    if os.path.isdir(OUTPUT) or os.path.isfile(OUTPUT):
        while 1:
            print 'Are you sure to rewrite %s?[Y/n]' % OUTPUT
            key = raw_input()
            if key is 'Y':
                print 'Start crawling.'
                os.remove(OUTPUT)
                break
            elif key is 'n':
                print 'Stop crawling.'
                sys.exit(1)
            else:
                pass
    OUTPUT = OUTPUT if OUTPUT.endswith('/') else OUTPUT + '/'
    # SUB TODO
    assert SUB in ['CS', 'EE', 'CE', 'cs', 'ee', 'ce']
    if SUB is 'CS' or 'cs':
        SUB = 'computer+science'
        print 'Crawling Computer Science.'
    elif SUB is 'EE' or 'ee':
        SUB = 'electrical+engineering'
        print 'Crawling Electrical Engineering.'
    else:
        SUB = 'computer+engineering'
        print 'Crawling Computer Engineering.'
    # LEVEL
    #assert LEVEL in ['MS', 'ms', 'PhD', 'PHD', 'phd']
    if LEVEL in ['MS', 'ms']:
        print 'Crawling MS programs.'
    elif LEVEL in ['PhD', 'PHD', 'phd']:
        print 'Crawling PhD programs.'
    else:
        sys.exit(-1)
    # PAGE
    try:
        assert START_PAGE <= END_PAGE
        assert isinstance(STRAT_PAGE, int)
        assert isinstance(END_PAGE, int)
    except:
        print 'Pages setting failed.'
        START_PAGE = 1
        END_PAGE = -1
    
    
def main():
    proc_glob()
    for i in range(START_PAGE, END_PAGE):
        print 'Procesing page %i' % i
        host = HOST + SUB + '&=a&o=&p=' + str(i)
        cont = urllib2.urlopen(host).read()
        # TODO time control
        start_pos = cont.find('instcol')
        start_pos = cont.find('instcol', start_pos)
        start_pos += 9
        # start point of first university
    

if __name__ == '__main__':
    main()
