# coding: utf-8
import os
import sys
import re
from copy import copy

GRE_pat = re.compile('\d{3}/\d{3}/\d\.\d{2}')
GPA_pat = re.compile('Undergrad GPA</strong>: \d\.\d{2}')


def proc_substr(substr):
    assert isinstance(substr, str)
    univ_name = substr[:substr.find('</td>')]
    gre = GRE_pat.findall(substr)
    gpa = GPA_pat.findall(substr)
    assert gre and gpa
    isacc = bool(substr.find('class=\"dAccepted\">Accepted') != -1)
    isrej = bool(substr.find('class=\"dRejected\">Rejected') != -1)
    assert isacc or isrej
    assert isacc ^ isrej  # xor
    apl_res = 1 if isacc else 0
    # key-value format
    return univ_name, ','.join([gre[0], gpa[0][-4:], str(apl_res)])


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
            recd_page.append(recd_elem)
    recd_page = proc_univ_name(recd_page)
    return recd_page


def proc_univ_name(rec):
    rec_ = copy(rec)
    rec__ = []  # in return
    for rec_elem in rec_:
        matches = [x for x in rec_ if is_same_univ(x[0], rec_elem[0])]
        # TODO, efficiency consideration.
        #map(lambda x: rec_.remove(x), matches) # remove processed records
        if len(matches) == 1:
            # No other univs
            pass
        else:
            # other univs
            matches = [reduce((lambda x, y: (x[0], x[1] + '\n' + y[1])),
                              matches)]
        assert len(matches) == 1
        rec__.extend(matches)
    return rec__


def is_same_univ(key1, key2):
    # TODO, form a large table
    return key1 == key2
