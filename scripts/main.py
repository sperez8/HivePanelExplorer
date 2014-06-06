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

#hive data imports
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from data import html_items
from hive import Hive

#-----------------------
# Below are variables which would normally be inputer by the user.
# For the sake of developing the script I have stored them here for convenience
#-----------------------
debug = False
numAxes = 3
doubleAxes = True
axisAssignRule = 'degree'
axisPositRule = 1


def make_html(hive):
    '''takes a hive instance and write the
    following files:
        nodes.js - contains nodes, position and coloring
        edges.js - contains edges and their type
        hiveplot.html - contains the html and D3 script to make the hive plot!
    '''
    
    #print htmlContainer
    return None

def make_hive(nodefile, edgefile):
    '''creates a hive instance form user input'''
    
    hive = Hive(debug=debug)
    hive.get_nodes('tests/test_nodes_friends.csv')
    hive.get_edges('tests/test_edges_friends.csv')
    hive.make_axes(numAxes = numAxes, doubleAxes = doubleAxes)
    hive.node_assignment(rule = axisAssignRule)
    hive.node_position(rule = axisPositRule)
    hive.node_properties()
    hive.make_edges()
    hive.edge_properties()
    
    return hive

def main(*argv):
    '''handles the user input and runs the functions 
        needed to make the hive plot'''
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
    print '\n\nNode file is "', nodefile, '"'
    print 'Edge file is "', edgefile, '"'
    
    hive = make_hive(nodefile, edgefile)
    make_html(hive)
    
    print "\n\n"
    


if __name__ == "__main__":
    main(*sys.argv[1:])
