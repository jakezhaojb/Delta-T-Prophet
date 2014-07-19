#! /usr/bin/env python
# coding: utf-8

import os
import sys
import urllib2
import re
from dpark import DparkContext
from process import *
import shutil

HOST = 'http://thegradcafe.com/survey/index.php?q='
OUTPUT = '/home/junbo/Delta_T/tmp'
SUB = 'CS'
LEVEL = 'MS'
START_PAGE = 1
END_PAGE = 700
DPARK_ON = False


def proc_glob():
    """Process global objects"""
    global OUTPUT, SUB, LEVEL, START_PAGE, END_PAGE
    assert HOST.find('http://thegradcafe.com/survey/index.php?q=') is 0
    # OUTPUT
    if os.path.isdir(OUTPUT) or os.path.isfile(OUTPUT):
        while 1:
            print 'Are you sure to rewrite %s?[Y/n]' % OUTPUT
            key = raw_input()
            if key is 'Y':
                print 'Start crawling.'
                shutil.rmtree(OUTPUT)
                break
            elif key is 'n':
                print 'Stop crawling.'
                sys.exit(1)
            else:
                pass
    OUTPUT = OUTPUT if OUTPUT.endswith('/') else OUTPUT + '/'
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
    

def main():
    if DPARK_ON:
        print 'Using dpark to speed up.'
        page = range(STRAT_PAGE, END_PAGE)
        dpark_ctx = DparkContext('mesos')
        # TODO


    else:
        # TODO, LEVEL AND TIME
        proc_glob()  # TODO, strange BUG: UnboundLocalError: "local variable 'OUTPUT' referenced before assignment"
        recd = []
        num = 0
        for i in range(START_PAGE, END_PAGE):
            print 'Procesing page %i' % i
            host = HOST + SUB + '&=a&o=&p=' + str(i)
            cont = urllib2.urlopen(host).read()
            # TODO time control
            recd.extend(proc_page(cont))
            print 'Process page %i done.' % i
        recd = proc_univ_name(recd)  # union same keys across pages
        # file IO
        for recd_elem in recd:
            fn_out = open(OUTPUT + recd_elem[0], 'w')
            fn_out.write(recd_elem[1])
            fn_out.write('\n')
            fn_out.close()
            print 'Finish file %s' % fn_out.name

    print 'Done.'

if __name__ == '__main__':
    main()
