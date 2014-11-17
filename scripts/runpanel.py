'''
created  07/11/2014

by sperez

Panel class stores the hive plots to be displayed
'''

#library imports
import sys
import os
import numpy as np
import webbrowser
import argparse
from hive import *
from html_writer import *
from panel import Panel

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)

SIZE = (5,5) #assignment by position rules
ASSIGNMENT_RULES = ['degree', 'betweeness', 'clustering', 'centrality','component']
POSITION_RULES = ['degree', 'betweeness', 'clustering', 'centrality','component']
NODES = os.path.join(_root_dir, 'tests', 'test_nodes_friends.txt')
EDGES = os.path.join(_root_dir, 'tests', 'test_edges_friends.txt')
TITLE = 'friends_panel_test'
FOLDER = os.path.join(_root_dir, 'tests')

def main(*argv):
    '''handles user input and runs plsa'''
    parser = argparse.ArgumentParser(description='This scripts produces an interactive hive panel.')
    parser.add_argument('-t', help='Title of hive plot', default = TITLE)
    parser.add_argument('-n', help='The node file', default = NODES)
    parser.add_argument('-e', help='The edge file', default = EDGES)
    parser.add_argument('-path', help='Path where hive plot will be saved', default = FOLDER)
    parser.add_argument('-axes', help='Number of axes', type = int)
    parser.add_argument('-double', help='Doubles the number of axes', action = 'store_true')
#     parser.add_argument('-assignment', help=assignmentHelp)
#     parser.add_argument('-position', help=positionHelp)
#     parser.add_argument('-size', help = 'Size of hive plot: big or small', default = 'small')
    parser.add_argument('-debug', help='Print verbatim to debug', action = 'store_true')
    args = parser.parse_args()
    
    if (args.n == '' and args.e != '') or (args.n != '' and args.e == ''):
        print "\n***You must specify both a node and an edge file if specifying either.***\n"
        parser.print_help()
        sys.exit()
        
    title = args.t
    nodeFile = args.n
    edgeFile = args.e
    axes = args.axes
    double = args.double
#     assignment = args.assignment
#     position = args.position
#     size = gui_options.sizes[args.size]
    debug = args.debug
    folder = args.path
    
    if not axes:
        print "You must specify a number of axes"
        sys.exit()
            
    P = Panel(size = SIZE,
              debug = debug,
              numAxes = axes,
              doubleAxes = double,
              assignmentRules = ASSIGNMENT_RULES, 
              positionRules = POSITION_RULES, 
              rawMeasures = True)
    P.make_panel(nodeFile, edgeFile)
    P.open_panel(title, folder, only_input_files = True)

    
    
if __name__ == "__main__":
    '''testing purposes'''
    main(*sys.argv[1:])












