'''
created  10/06/2014

by sperez

Contains functions used by hive class to measure things like network properties
'''

#library imports
import sys
import os
import argparse
import numpy as np
from math import pi
import hive as hive


_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx
from make_network import *

NODES = os.path.join(_root_dir, 'tests', 'test_nodes_friends.txt')
EDGES = os.path.join(_root_dir, 'tests', 'test_edges_friends.txt')

def main(*argv):
    '''handles user input and runs plsa'''
    parser = argparse.ArgumentParser(description='This scripts produces an interactive hive panel.')
    parser.add_argument('-n', help='The node file', default = NODES)
    parser.add_argument('-e', help='The edge file', default = EDGES)
    args = parser.parse_args()
    
    if (args.n == '' and args.e != '') or (args.n != '' and args.e == ''):
        print "\n***You must specify both a node and an edge file if specifying either.***\n"
        parser.print_help()
        sys.exit()
        
    nodeFile = args.n
    edgeFile = args.e

    G = import_graph(nodeFile,edgeFile)

    print "\n\n\nMade the networkx graph:"
    print G.nodes(data=True)
    print G.edges(data=True)
    return G

def measure_all(G):
    '''measure all interesting global network measures'''
    measure = {}
    
    return measures


    
if __name__ == "__main__":
    '''testing purposes'''
    main(*sys.argv[1:])


