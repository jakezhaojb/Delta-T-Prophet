#! /usr/bin/env python
# coding: utf-8

import os
import sys
import urllib2
import re
from dpark import DparkContext
from process import *

HOST = 'http://thegradcafe.com/survey/index.php?q='
OUTPUT = '/home/junbo/Delta_T/tmp'  # TODO
SUB = 'CS'
LEVEL = 'MS'
START_PAGE = 1
END_PAGE = 10
DPARK_USAGE = False


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
    if not os.path.isdir(OUTPUT):
        os.mkdir(OUTPUT)
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
        assert isinstance(START_PAGE, int)
        assert isinstance(END_PAGE, int)
    except:
        print 'Pages setting failed.'
        START_PAGE = 1
        END_PAGE = -1
    

def main_serial():
    proc_glob()  # TODO, strange BUG: UnboundLocalError: "local variable 'OUTPUT' referenced before assignment"
    recd = []
    num = 0
    for i in range(START_PAGE, END_PAGE):
        import pdb; pdb.set_trace()
        print 'Procesing page %i' % i
        host = HOST + SUB + '&=a&o=&p=' + str(i)
        cont = urllib2.urlopen(host).read()
        # TODO time control
        recd.extend(proc_page(cont))
        print 'Process page %i done.' % i
    proc_univ_name(recd) # union same keys across pages
    # file IO
    for recd_elem in recd:
        fn_out = open(OUTPUT + recd_elem[0], 'w')
        fn_out.write(recd_elem[1])
        fn_out.close()
        print 'Finish file %s' % fn_out.name
    print 'Done.'
    

def main_paralz():
    assert DPARK_USAGE # Use dpark to make some RDDs
    # TODO
    page = range(STRAT_PAGE, END_PAGE)
    dpark_ctx = DparkContext('mesos')
    #def map_iter(pg):
        # TODO


if __name__ == '__main__':
    if DPARK_USAGE:
        main_paralz()
    else:
        main_serial()
