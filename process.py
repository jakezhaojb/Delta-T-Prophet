# coding: utf-8
import os
import sys
import re
from copy import copy

GRE_pat = re.compile('\d{3}/\d{3}/\d\.\d{2}')
GPA_pat = re.compile('Undergrad GPA</strong>: \d\.\d{2}')
TERM_pat = re.compile('([FS]\d\d)')
DEBUG = False


def proc_substr(substr):
    # TODO the following regex is too ugly, optimize it!
    assert isinstance(substr, str)
    if DEBUG:
        import pdb; pdb.set_trace()
        print substr
    # university name
    univ_name = substr[:substr.find('</td>')]
    # level applied
    level = 'MS' if 'Masters' in substr[:substr.find('class=\"d')] else 'PhD'
    # term applied
    term_rec = re.findall(TERM_pat, substr)[0]
    # time notified
    substr_time = substr[substr.find('via'): substr.find('<a class="extinfo"')]
    time_rec = substr_time.split()[-2:]
    time_rec = '/'.join(time_rec)
    # GRE general
    gre = GRE_pat.findall(substr)
    # GPA
    gpa = GPA_pat.findall(substr)
    assert gre and gpa
    # Accepted or Declined
    isacc = bool(substr.find('class=\"dAccepted\">Accepted') != -1)
    isrej = bool(substr.find('class=\"dRejected\">Rejected') != -1)
    assert isacc or isrej
    assert isacc ^ isrej  # xor
    apl_res = 1 if isacc else 0
    # key-value format
    return univ_name, ','.join([gre[0], gpa[0][-4:], level,
                                term_rec, time_rec, str(apl_res)])


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
        # TODO, efficiency?
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
    if is_same_string(key1, key2):
        return True
    # brackets
    pat_bracket = re.compile('\([\w\ ]*\)')
    key1 = re.sub(pat_bracket, '', key1)
    key2 = re.sub(pat_bracket, '', key2)
    if is_same_string(key1, key2):
        return True
    # symbols
    pat_symbol = re.compile('[^\w\ ]')
    key1 = re.sub(pat_symbol, '', key1)
    key2 = re.sub(pat_symbol, '', key2)
    if is_same_string(key1, key2):
        return True
    # junk words, like: of, at ...
    jword = ['university', 'of', 'at']
    for jword_elem in jword:
        _jword_elem = '\\b' + jword_elem + '\\b'
        pat_jword = re.compile(_jword_elem)
        key1 = key1.lower()
        key2 = key2.lower()
        key1 = re.sub(pat_jword, '', key1)
        key2 = re.sub(pat_jword, '', key2)
    if is_same_string(key1, key2):
        return True
    # all-else
    return False


def is_same_string(str1, str2):
    assert isinstance(str1, str) and isinstance(str2, str)
    if str1 == str2:
        return True
    else:
        str1_ = str1.split()
        str2_ = str2.split()
        str1__ = ''.join(str1_)
        str2__ = ''.join(str2_)
        return str1__.lower() == str2__.lower()
