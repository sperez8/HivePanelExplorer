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

#hive data imports
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from data import html_items
from hive import Hive

#-----------------------
# Below are variables which would normally be inputer by the user.
# For the sake of developing the script I have stored them here for convenience
numAxes = 3
doubleAxes = True
axisAssignRule = 'degree'
axisPositRule = 2


def make_html(hive):
    '''takes a hive instance and write the
    following files:
        nodes.js - contains nodes, position and coloring
        edges.js - contains edges and their type
        hiveplot.html - contains the html and D3 script to make the hive plot!
    '''
    
    #print htmlContainer
    return None

def make_hive(nodefile, edgefile, debug):
    '''creates a hive instance form user input'''
    
    hive = Hive(numAxes = numAxes, 
                doubleAxes = doubleAxes, 
                axisAssignRule = axisAssignRule, 
                axisPositRule = axisPositRule, 
                debug = debug)
    hive.get_nodes(nodefile)
    hive.get_edges(edgefile)
    hive.make_axes()
    hive.node_assignment()
    hive.node_position()
    hive.node_style()
    hive.make_edges()
    hive.edge_style()
    
    return hive

def main(*argv):
    '''handles the user input and runs the functions 
        needed to make the hive plot'''
    nodefile = ''
    edgefile = ''
    debug = False
    try:
        opts, args = getopt.getopt(argv,"hn:e:d",["nfile=","efile="])
    except getopt.GetoptError:
       print 'main.py -n <nodefile> -e <edgefile> -d'
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -n <nodefile> -e <edgefile> -d'
            sys.exit()
        elif opt in ("-n", "--nfile"):
            nodefile = arg
        elif opt in ("-e", "--efile"):
            edgefile = arg
        elif opt in ("-d"):
            debug = True
    print '\nNode file is "', nodefile, '"'
    print 'Edge file is "', edgefile, '"'
    
    hive = make_hive(nodefile, edgefile, debug)
    make_html(hive)    
    
    print '\n'


if __name__ == "__main__":
    main(*sys.argv[1:])
