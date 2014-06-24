'''
created  03/06/2014

by sperez

Takes user input and calls Hive module to produce the JavaScript files
needed to make a hive plot in D3 using Mike Bolstock's D3 hive module
'''
#library imports
import os
import sys
import getopt
import string

#hive plot specific imports
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from data import html_items
from hive import Hive
from html_uttilities import *
from tests.test_parameter_friends import *


def main(*argv):
    '''handles the user input and runs the functions 
        needed to make the hive plot'''
    nodefile = ''
    edgefile = ''
    debug = False
    title = ''
    try:
        opts, args = getopt.getopt(argv,"hn:e:t:d",["nfile=","efile=","title="])
    except getopt.GetoptError:
       print 'main.py -n <nodefile> -e <edgefile> -t <title> -d'
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -n <nodefile> -e <edgefile> -t <title> -d'
            sys.exit()
        elif opt in ("-n", "--nfile"):
            nodefile = arg
        elif opt in ("-e", "--efile"):
            edgefile = arg
        elif opt in ("-d"):
            debug = True
        elif opt in ("-t", "--title"):
            title = arg
    print '\n    Node file is "', nodefile, '"'
    print '    Edge file is "', edgefile, '"'
    
    
    hive = Hive(debug = debug,
            numAxes = numAxes, 
            doubleAxes = doubleAxes, 
            axisAssignRule = axisAssignRule, 
            axisPositRule = axisPositRule, 
            edgePalette = edgeColorPalette, 
            edgeStyleRule = edgeColorRule)
        
    hive.make_hive(nodefile, edgefile)
    make_html(title, hive)
    
    print '\n'


if __name__ == "__main__":
    main(*sys.argv[1:])
