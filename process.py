# coding: utf-8
import os
import sys
import re

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
            recd_page.append(recd_elem)
    proc_univ_name(recd_page)
    return recd_page


def proc_univ_name():
    # TODO
    """docstring for proc_univ_name"""
    
