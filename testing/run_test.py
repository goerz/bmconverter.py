#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testing for bmconverter.py"""

import os
from bmconverter import *
import codecs
import sys

# TODO: Test bookmark tree modifications (adding, removing nodes, shifting pages, etc.)

def modificationtest():
    b = read_xml("pathological.in.xml")
    c = b.copy()
    for node in c:
        node.title = "COPY " + node.title
    for node in c:
        if node.level() > 2:
            node.delete()
    c.flush()
    c.shift_pagenumber(100)
    c.shift_pagenumber(-50)
    d = b + c
    write_csv(d, "out.csv")
    c = read_csv("out.csv")
    write_xml(c, "out.xml")
    stdout = sys.stdout
    stdin  = sys.stdin
    stderr = sys. stderr
    sys.stderr = sys.stdout = codecs.open("out.xml", 'a', 'utf-8')
    print "\n\n"
    d.long_debug()
    sys.stdout = stdout
    sys.stdin  = stdin
    sys.stderr = stderr


tests = [
    # XML Tests
    #  1
    {'commands' : [ 'bmconverter.py -m xml2xml normal.in.xml out.xml'],
     'expected' : 'normal.in.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.xml']},
    #  2
    {'commands' : [ 'bmconverter.py -m xml2xml pathological.in.xml out.xml'],
     'expected' : 'pathological.in.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.xml']},
    # CSV Tests
    #  3
    {'commands' : [ 'bmconverter.py -m xml2csv normal.in.xml out.csv'],
     'expected' : 'normal.csv',
     'out'      :  'out.csv',
     'cleanup'  :  []},
    #  4
    {'commands' : [ 'bmconverter.py -m csv2xml out.csv out.xml'],
     'expected' : 'normal.in.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.csv', 'out.xml']},
    #  5
    {'commands' : [ 'bmconverter.py -m xml2csv pathological.in.xml out.csv'],
     'expected' : 'pathological.csv',
     'out'      :  'out.csv',
     'cleanup'  :  []},
    #  6
    {'commands' : [ 'bmconverter.py -m csv2xml out.csv out.xml'],
     'expected' : 'pathological.via_csv.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.csv', 'out.xml']},
    # pdftk Tests
    #  7
    {'commands' : [ 'bmconverter.py -m xml2pdftk normal.in.xml out.pdftk'],
     'expected' : 'normal.pdftk',
     'out'      :  'out.pdftk',
     'cleanup'  :  []},
    #  8
    {'commands' : [ 'bmconverter.py -m pdftk2xml out.pdftk out.xml'],
     'expected' : 'normal.via_pdftk.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.pdftk', 'out.xml']},
    #  9
    {'commands' : [ 'bmconverter.py -m xml2pdftk pathological.in.xml out.pdftk'],
     'expected' : 'pathological.pdftk',
     'out'      :  'out.pdftk',
     'cleanup'  :  []},
    # 10
    {'commands' : [ 'bmconverter.py -m pdftk2xml out.pdftk out.xml'],
     'expected' : 'pathological.via_pdftk.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.pdftk', 'out.xml']},
     # text Tests
     # 11
    {'commands' : [ 'bmconverter.py -m xml2text normal.in.xml out.txt'],
     'expected' : 'normal.txt',
     'out'      :  'out.txt',
     'cleanup'  :  []},
    # 12
    {'commands' : [ 'bmconverter.py -m text2xml out.txt out.xml'],
     'expected' : 'normal.via_text.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.txt', 'out.xml']},
    # 13
    {'commands' : [ 'bmconverter.py -m xml2text --long pathological.in.xml out.txt'],
     'expected' : 'pathological.txt',
     'out'      :  'out.txt',
     'cleanup'  :  []},
    # 14
    {'commands' : [ 'bmconverter.py -m text2xml out.txt out.xml'],
     'expected' : 'pathological.via_text.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.txt', 'out.xml']},
     # complex tests
     # 15
    {'commands' : [ modificationtest ],
     'expected' :  'modificationtest.xml',
     'out'      :  'out.xml',
     'cleanup'  :  ['out.xml', 'out.csv']}
]

i = 0
for test in tests:
    i += 1
    print '== Test ' + str(i) + " =="
    for command in test['commands']:
        print command,
        if callable(command):
            command()
        else:
            os.system(command)
    if os.system( 'diff %s %s' % (test['out'], test['expected']) ) == 0:
        print "\t\tPassed\n"
    else:
        print "\t\tFAILED\n"
        os.system('kompare %s %s' % (test['out'], test['expected']))
    dummy = raw_input("Press Enter to finish test")
    for file in test['cleanup']:
        os.remove(file)
