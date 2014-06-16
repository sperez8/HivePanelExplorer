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
from tests.test_parameter_friends import *


def write_nodes(file, hive):
    '''outputs node info to a text file
        in a javascript variable format'''
    
    f = open(file, 'w')
    f.write('var nodes = [\n')
    
    for i,n in enumerate(hive.nodes):
        f.write('  {axis: ' + str(hive.axisAssignment[n]-1) + ', pos: ' + str(hive.nodePositions[n]) + '},\n')
    f.write('];')
    
def write_edges(file, hive):
    '''outputs node info to a text file
        in a javascript variable format'''
    
    f = open(file, 'w')
    f.write('var links = [\n')
    for s, t in hive.edges:
        f.write('  {source: nodes['+str(hive.nodes.index(s))+'], target: nodes['+str(hive.nodes.index(t))+'], type: ' + str(hive.edgeStyling[(s,t)]) + '},\n')
    f.write('];')
    
def make_html(title, hive):
    '''takes a hive instance and write the
    following files:
        nodes.js - contains nodes, position and coloring
        edges.js - contains edges and their type
        hiveplot.html - contains the html and D3 script to make the hive plot!
    '''
    htmlItems = html_items.htmlContainer
    keyOrder = html_items.keyOrder
    
    outputfile = _root_dir + '/tests/' + title + ".html"
    print '    Making the hive plot \'{0}\''.format(outputfile) 
    nodeFile = _root_dir + '/tests/' + 'nodes' + title + '.js'
    edgeFile = _root_dir + '/tests/' + 'edges' + title + '.js'
    
    write_nodes(nodeFile, hive)
    write_edges(edgeFile, hive)
    
    with open(outputfile, 'w') as f:
        for key in keyOrder:
            text = htmlItems[key]
            #wrap text given user input
            if key == 'nodefile':
                f.write('<script src="' + nodeFile +  '"></script>')
            elif key == 'edgefile':
                f.write('<script src="' + edgeFile +  '"></script>')
            elif key == 'start js parameters':
                f.write('<script> \n//All the user defined parameters')
            elif key == 'titleheader':
                f.write('var SVGTitle = \'' + 'Hive plot : ' + title + '\'')
            elif key == 'angles':
                f.write('var angle = ['+ ','.join([str(a) for a in hive.angles]) +']')
            elif key == 'color':
                #f.write('var modulecolor = ' + '[\'' + color + '\']') #doesn't work yet
                f.write('var nodecolor = ' + '\'' + color + '\'')
            elif key == 'edge_color':
                f.write('var edge_color = [\'' + '\',\''.join([str(c) for c in edgeColorPalette]) +'\']')
            elif key == 'numAxes':
                if hive.doubleAxes:
                    f.write('var num_axis = ' + str(hive.numAxes*2))
                else:
                    f.write('var num_axis = ' + str(hive.numAxes))
            elif key == 'end js parameters':
                f.write('</script>')
            else:
                f.write(text)
            f.write('\n')
        
    f.close()
    
    return None

def make_hive(nodefile, edgefile, debug):
    '''creates a hive instance form user input'''  
        
    hive = Hive(debug = debug,
                numAxes = numAxes, 
                doubleAxes = doubleAxes, 
                axisAssignRule = axisAssignRule, 
                axisPositRule = axisPositRule, 
                edgePalette = edgeColorPalette, 
                edgeStyleRule = edgeColorRule)
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
    
    hive = make_hive(nodefile, edgefile, debug)
    make_html(title, hive)
    
    print '\n'


if __name__ == "__main__":
    main(*sys.argv[1:])
