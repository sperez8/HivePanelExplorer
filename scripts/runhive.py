'''
Created on 06/10/2014

author: sperez8
'''

import sys, os
import argparse
import numpy as np
import webbrowser

from gui import gui
from gui import gui_options
from html_writer import *
from hive import Hive

def main(*argv):
    '''handles user input and runs plsa'''
    parser = argparse.ArgumentParser(description='This scripts produces hive plots given user data without use of the gui.')
    parser.add_argument('-t', help='Title of hive plot', default = gui.TITLE)
    parser.add_argument('-n', help='The node file', default = gui.NODES)
    parser.add_argument('-e', help='The edge file', default = gui.EDGES)
    parser.add_argument('-axes', help='Number of axes', type = int, required = True)
    parser.add_argument('-double', help='Doubles the number of axes', action = 'store_true')
    parser.add_argument('-assignment', help='Node property to use to assign to an axis', required = True)
    parser.add_argument('-position', help='Node property to use to position node along axis', required = True)
    parser.add_argument('-size', help = 'Size of hive plot: big or small', default = 'small')
    parser.add_argument('-color', help = 'Color of palette', default = 'red')
    parser.add_argument('-open', help='Open the hive plot in browser', action = 'store_true')
    parser.add_argument('-debug', help='Print info to debug', action = 'store_true')
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
    assignment = args.assignment
    position = args.position
    size = gui_options.sizes[args.size]
    color = args.color
    open = args.open
    debug = args.debug      
    
    hive = Hive(debug = debug,
                numAxes = axes,
                doubleAxes = double, 
                axisAssignRule = assignment, 
                axisPositRule = position,
                #edgePalette = palette, 
                #edgeStyleRule = edgeStyle,
                nodeColor = color
                )
    hive.make_hive(nodeFile, edgeFile)
    
    rules = {}
    rules['assignment'] = assignment
    rules['position'] = position
    
    url = make_html(title, hive, size, rules = rules)

    if open:
        webbrowser.open("file://"+url, new=1)

    
if __name__ == "__main__":
    main(*sys.argv[1:])
    
    
    