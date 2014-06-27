# coding: utf-8
import os
import sys
import re
from copy import copy

GRE_pat = re.compile('\d{3}/\d{3}/\d\.\d{2}')
GPA_pat = re.compile('Undergrad GPA</strong>: \d\.\d{2}')


def proc_substr(substr):
    assert isinstance(substr, 'str')
    univ_name = substr[:substr.find('<\td>')]
    gre = GRE_pat.findall(substr)
    gpa = GPA_pat.findall(substr)
    assert gre and gpa
    # TODO, process the univ_name
    return univ_name, ','.join([gre[0], gpa[0][-4:]])  # key-value format


def proc_page(page_str):
    recd_page = []
    start_pos_f = page_str.find('instcol') + 1  # After 'Institution'
    start_pos_f = page_str.find('instcol', start_pos_f) + 9  # First University
    while 1:
        start_pos_b = page_str.find('instcol', start_pos_f)
        if start_pos_b is -1:
            break
        substr = page_str[start_pos_f: start_pos_b]
        start_pos_f = start_pos_b + 9
        try:
            recd_elem = proc_substr(substr)
        except:
            #print 'Not enough info acquire'
            pass
        else:
            recd_page.append(recd_elem) # PAGE ZHIJIAN !! TODO
    proc_univ_name(recd_page)
    return recd_page


def proc_univ_name(rec):
    rec_proc = dict()
    rec_ = copy(rec)
    rec__ = [] # in return
    for rec_elem in rec_:
        matches = [x for x in rec_ if is_same_univ(x[0], rec_elem[0])] # find_if
        map(lambda x: rec_.remove(x), matches) # remove processed records
        if len(matches) == 1:
            # No other univs
            pass
        else:
            # other univs
            matches = [reduce((lamdba x, y: x[0], x[1] + '\n' + y[1]), matches)]
        assert len(matches) == 1
        rec__.extend(matches)
    return rec__


def is_same_univ(key1, key2):
    # TODO, form a large table
    return key1 == key2
