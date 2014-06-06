'''
created  03/06/2014

by sperez

Takes user input and calles Hive module to produce the JavaScript files
needed to make a hive plot in D3 using Mike Bolstock's D3 hive module
'''
#library imports
import os
import sys
import getopt
import numpy as np

#hive data imports
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from data import html_items
from hive import Hive


def make_html():
    #print htmlContainer
    return None

def make_hive(nodefile, edgefile):
    hive = Hive(debug=True)
    hive.get_nodes('tests/test_nodes_friends.csv')
    hive.get_edges('tests/test_edges_friends.csv')
    return None

def main(*argv):
    nodefile = ''
    edgefile = ''
    try:
       opts, args = getopt.getopt(argv,"hn:e:",["nfile=","ofile="])
    except getopt.GetoptError:
       print 'main.py -n <nodefile> -o <edgefile>'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'main.py -n <nodefile> -o <edgefile>'
          sys.exit()
       elif opt in ("-n", "--nfile"):
          nodefile = arg
       elif opt in ("-e", "--efile"):
          edgefile = arg
    print 'Node file is "', nodefile, '"'
    print 'Edge file is "', edgefile, '"'
    
    make_hive(nodefile, edgefile)
    


if __name__ == "__main__":
    main(*sys.argv[1:])
