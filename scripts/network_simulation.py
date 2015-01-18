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
import prettyplotlib as ppl

# prettyplotlib imports 
import matplotlib.pyplot as plt
import matplotlib as mpl
from prettyplotlib import brewer2mpl

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx
from make_network import *

NODES = os.path.join(_root_dir, 'tests', 'test_nodes_friends.txt')
EDGES = os.path.join(_root_dir, 'tests', 'test_edges_friends.txt')

RANDSEED = 2
np.random.seed(RANDSEED)
MEASURES = [nx.betweenness_centrality, nx.degree_centrality, 
		nx.closeness_centrality, nx.eigenvector_centrality, nx.load_centrality]

def get_graph(nodeFile, edgeFile):
	G = import_graph(nodeFile,edgeFile)
	print "\nMade the networkx graph."
	return G


def input_files(*argv):
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

	G = get_graph(nodeFile, edgeFile)
	return G



def random_attack(G):
	'''Measure the size of the largest component of the graph
	as nodes are removed randomly'''
	sizes = []
	sizes.append(len(nx.connected_components(G)[0]))
	H = G.copy()

	nodes= G.nodes()
	np.random.shuffle(nodes)
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

	measures = sorted(measures, key = lambda item: item[1], reverse = True)

	for n,v in measures[:-1]:
		H.remove_node(n)
		sizes.append(len(nx.connected_components(H)[0]))

	return sizes



def plot_robustness(data):
	'''plots the simulations'''
	colors ='rgbkmy'

	# plotting locations in rows and centralities in columns
	fig, axes = plt.subplots(2,6)

	print axes
	for i,ax in enumerate(axes):
		name,values = data[i]
		print name, values,i,ax
		#plt.plot(range(len(values)),values,colors[i])
		ppl.plot(ax, range(len(values)), values)

	ppl.legend(ax)

	fig.savefig('plot_prettyplotlib_default.png')




networks = ['B_R_BAC_SBS_OM3']
path = 'C:\\Users\\Sarah\\Dropbox\\1-Aria\\LTSP_networks\\'

if __name__ == "__main__":
	'''testing purposes'''
	#G = input_files(*sys.argv[1:])
	graphs = {}
	for netName in networks:
		nodeFile = os.path.join(path,netName+'_nodes.txt')
		edgeFile = os.path.join(path,netName+'_edges.txt')
		graphs[netName] = get_graph(nodeFile,edgeFile)

	for netName,G in graphs.iteritems():
		randSizes = random_attack(G)
		data = []
		data.append(('random',randSizes))
		for m in MEASURES:
			targSizes = target_attack(G, m)
			data.append((m.__name__,targSizes))
		plot_robustness(data)