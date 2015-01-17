'''
created  01/17/2014

by sperez

Runs attack/extinction simulations on networks
'''

#library imports
import sys
import os
import argparse
import numpy as np
import hive as hive
import random
import matplotlib.pyplot as plt

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx
from make_network import *

NODES = os.path.join(_root_dir, 'tests', 'test_nodes_friends.txt')
EDGES = os.path.join(_root_dir, 'tests', 'test_edges_friends.txt')

RANDSEED = 2
random.seed(RANDSEED)
MEASURES = [nx.betweenness_centrality, nx.degree_centrality, 
		nx.closeness_centrality, nx.eigenvector_centrality, nx.load_centrality]

def main(*argv):
    '''handles user input and runs plsa'''
    parser = argparse.ArgumentParser(description='This scripts runs an extinction simulation.')
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

    print "\nMade the networkx graph."

    return G


def random_attack(G):
	'''Measure the size of the largest component of the graph
	as nodes are removed randomly'''
	sizes = []
	sizes.append(len(nx.connected_components(G)[0]))
	H = G.copy()

	nodes= G.nodes()
	random.shuffle(nodes)
	for n in nodes[:-1]:
		H.remove_node(n)
		sizes.append(len(nx.connected_components(H)[0]))

	return sizes

def target_attack(G, measure):
	'''Measure the size of the largest component of the graph
	as nodes are removed given the measure (degree or centrality 
	measure). The order of the nodes to be removed IS NOT updated
	after each removal.
	'''
	sizes = []
	sizes.append(len(nx.connected_components(G)[0]))
	H = G.copy()

	measures = [(n,v) for n,v in measure(G).iteritems()]

	def getKey(item):
		return item[1]
	measures = sorted(measures, key = getKey, reverse = True)

	for n,v in measures[:-1]:
		H.remove_node(n)
		sizes.append(len(nx.connected_components(H)[0]))

	return sizes

def plot_robustness(data):
	colors ='rgbkmy'
	for i,(name,values) in enumerate(data):
		print colors[i],name,values
		plt.plot(range(len(values)),values,colors[i])
	plt.show()
	return None

if __name__ == "__main__":
    '''testing purposes'''
    G = main(*sys.argv[1:])
    randSizes = random_attack(G)
    data = []
    data.append(('random',randSizes))
    for m in MEASURES:
    	targSizes = target_attack(G, m)
    	data.append((m.__name__,targSizes))
    print data
    plot_robustness(data)