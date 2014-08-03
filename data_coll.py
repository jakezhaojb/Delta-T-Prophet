#! /usr/bin/env python
# coding : utf-8

import os
import sys

INPUT_PATH = 'dataset/CS.gradcafe'
INPUT_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), INPUT_PATH)
OUTPUT_PATH = '233'


def main():
    global INPUT_PATH, OUTPUT_PATH  # Still that strange bug! Why not defined before referenced?? Strange indeed TODO

    # INPUT PATH process
    assert os.path.isdir(INPUT_PATH)
    if not INPUT_PATH.endswith('/'):
        INPUT_PATH += '/'
    if not OUTPUT_PATH.endswith('.csv'):
        print 'We recommend csv file as output storage.'

    # OUTPUT PATH process
    if os.path.isfile(OUTPUT_PATH):
        while 1:
            print 'Would you like to overwrite file: %s [Y/n]' % OUTPUT_PATH
            ans = raw_input()
            if ans == 'Y':
                print 'Will overwrite it.'
                break
            elif ans == 'n':
                print 'Give up overwriting.'
                sys.exit(1)
            else:
                continue
    # Start.
    print "Start collection."
    files_path = os.listdir(INPUT_PATH)
    files_path = filter(lambda x: not x.startswith('.'), files_path)
    output_file = open(OUTPUT_PATH, 'w')
    for file_elem in files_path:
        file_elem_abspath = os.path.join(INPUT_PATH, file_elem)
        if not os.path.isfile(file_elem_abspath):
            continue
        input_file = open(file_elem_abspath, 'r')
        ln = input_file.readlines()
        ln = map(lambda x: file_elem + ',' + x, ln)
        output_file.writelines(ln)
        input_file.close()
    output_file.close()
    print 'done.'


if __name__ == '__main__':
    main()
    
