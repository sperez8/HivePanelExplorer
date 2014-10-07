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
from gui import gui_utilities
from html_writer import *
from hive import Hive

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)

TEMP_FOLDER = _root_dir + '/tmp/'

assignmentHelp = 'Node property to use to assign to an axis. Choose from: "'
assignmentHelp += '","'.join(gui_options.assignmentOptions)
assignmentHelp += '" or inherit node properties.'

positionHelp = 'Node property to use to position node along axis. Choose from: "'
positionHelp += '","'.join(gui_options.positionOptions)
positionHelp += '" or inherit node properties.'

edgeStyleHelp = 'Edge Styling rule. Choose from: "'
edgeStyleHelp += '","'.join(gui_options.edgeStyleOptions)
edgeStyleHelp += '" or inherit edge properties.'

paletteHelp = 'Hue of palette for edge styling. Choose from: "'
paletteHelp += '","'.join(gui_options.colorOptions) +'"'

def main(*argv):
    '''handles user input and runs plsa'''
    parser = argparse.ArgumentParser(description='This scripts produces hive plots given user data without the use of the gui.')
    parser.add_argument('-t', help='Title of hive plot', default = gui.TITLE)
    parser.add_argument('-n', help='The node file', default = gui.NODES)
    parser.add_argument('-e', help='The edge file', default = gui.EDGES)
    parser.add_argument('-path', help='Path where hive plot will be saved', default = TEMP_FOLDER)
    parser.add_argument('-axes', help='Number of axes', type = int)
    parser.add_argument('-double', help='Doubles the number of axes', action = 'store_true')
    parser.add_argument('-assignment', help=assignmentHelp)
    parser.add_argument('-position', help=positionHelp)
    parser.add_argument('-size', help = 'Size of hive plot: big or small', default = 'small')
    parser.add_argument('-nodecolor', help = 'Color of nodes', default = 'purple')
    parser.add_argument('-edgestyle', help = edgeStyleHelp)
    parser.add_argument('-palette', help = paletteHelp, default = 'purple')
    parser.add_argument('-numcolors', help = 'The number of colors to use to style edges', default = 1)
    parser.add_argument('-open', help='Open the hive plot in the browser', action = 'store_true')
    parser.add_argument('-debug', help='Print verbatim to debug', action = 'store_true')
    parser.add_argument('-properties', help='Shows properties that can be used to plot hives', action = 'store_true')
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
    nodeColor = args.nodecolor
    edgeStyle = args.edgestyle
    numColors = args.numcolors
    palette = gui_utilities.get_palette(args.palette,int(numColors))
    open = args.open
    debug = args.debug      
    folder = args.path
    
    if args.properties:
        hive = Hive(debug = debug)
        properties = list(hive.get_nodes(nodeFile).keys()) + gui_options.assignmentOptions
        print '\nNode properties:\n\t"'+ '", "'.join(properties) + '"\n'
        properties = list(hive.get_edges(edgeFile)) + gui_options.edgeStyleOptions
        print 'Edge properties:\n\t"'+ '", "'.join(properties) + '"\n'
        sys.exit()
    else:
        if not axes:
            print "You must specify a number of axes"
            sys.exit()
        if not assignment:
            print "You must specify a node assignment rule"
            sys.exit()
        if not position:
            print "You must specify a node position rule"
            sys.exit()
            
    hive = Hive(debug = debug,
                numAxes = axes,
                doubleAxes = double, 
                axisAssignRule = assignment, 
                axisPositRule = position,
                edgePalette = palette, 
                edgeStyleRule = edgeStyle,
                nodeColor = nodeColor
                )
    hive.make_hive(nodeFile, edgeFile)
    
    rules = {}
    rules['assignment'] = assignment
    rules['position'] = position
    rules['edges'] = edgeStyle
    
    url = make_html(title, hive, size, rules = rules, folder = folder)

    if open:
        webbrowser.open("file://"+url, new=1)

    
if __name__ == "__main__":
    main(*sys.argv[1:])
    
    
    