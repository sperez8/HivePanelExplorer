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

NETWORKS = ['B_R_BAC_SBS_OM3','B_R_BAC_SBS_OM2']
PATH = 'C:\\Users\\Sarah\\Dropbox\\1-Aria\\LTSP_networks\\'


def make_graph(nodeFile, edgeFile):
	'''imports the node and edge file and makes the graph'''
	G = import_graph(nodeFile,edgeFile)
	print "\nMade the networkx graph."
	return G

def get_multiple_graphs(networks, path):
	'''makes multiple graphs from names of networks and a file path'''
	graphs = {}
	for netName in networks:
		nodeFile = os.path.join(path,netName+'_nodes.txt')
		edgeFile = os.path.join(path,netName+'_edges.txt')
		graphs[netName] = make_graph(nodeFile,edgeFile)
	return graphs

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

	G = make_graph(nodeFile, edgeFile)
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



def plot_robustness(data,filename):
	'''plots the simulations'''
	colors ='rgbkmy'

	# plotting locations in rows and centralities in columns
	fig, axes = plt.subplots(1)
	measures = data.keys()
	measures.remove('random')
	measures.insert(0,'random') #put at front

	colors = {measure: ppl.colors.set2[i] for i,measure in enumerate(measures)}

	for measure in measures:
		values = data[measure]
		x = range(len(values))
		ppl.plot(axes, x, 
			values,
			label=str(measure))
			#color=[colors[measure] for measure in measures])

	ppl.legend(axes)  
	fig.savefig(filename+'_simulation'+'.png')
	return None


def plot_individual(networks,path):
	graphs = get_multiple_graphs(networks,path)

	for netName,G in graphs.iteritems():
		randSizes = random_attack(G)
		data = {}
		data['random']=randSizes
		for m in MEASURES:
			targSizes = target_attack(G, m)
			data[m.__name__] = targSizes
		plot_robustness(data, netName)
	return None

def multi_plot_robustness(multidata,filename):
	'''plots the simulations in a multiplot'''
	colors ='rgbkmy'

	# plotting locations in rows and centralities in columns
	fig, axes = plt.subplots(len(multidata.keys()))
	netNames = multidata.keys()
	measures = multidata[netNames[0]].keys()
	measures.remove('random')
	measures.insert(0,'random') #put at front

	colors = {measure: ppl.colors.set1[i] for i,measure in enumerate(measures)}

	for ax, net in zip(axes,netNames):
		for measure in multidata[net].keys():
			values = multidata[net][measure]
			x = range(len(values))
			ppl.plot(ax,
				x, 
				values,
				label=str(measure),
				color=colors[measure])
		ax.set_title(net)

	ppl.legend(axes)
	fig.tight_layout()
	fig.savefig(filename+'_simulation'+'.png')
	return None

def plot_multiple(networks,path):
	graphs = get_multiple_graphs(networks,path)
	data = {}
	for netName,G in graphs.iteritems():
		randSizes = random_attack(G)
		data[netName] = {'random':randSizes}
		for m in MEASURES:
			targSizes = target_attack(G, m)
			data[netName][m.__name__] = targSizes
	
	multi_plot_robustness(data,'Allnetworks')
	return None


if __name__ == "__main__":
	'''testing purposes'''
	#G = input_files(*sys.argv[1:])
	plot_multiple(NETWORKS,PATH)
	#plot_individual(NETWORKS,PATH)

'''
to do:
Run sim on 10% of networks
normalize yticks by original size giant component
switch the oms and the measures
do all networks
'''