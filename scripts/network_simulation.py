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
import prettyplotlib as ppl

# prettyplotlib imports 
import matplotlib.pyplot as plt
import matplotlib as mpl
from prettyplotlib import brewer2mpl

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx
from make_network import import_graph

#NODES = os.path.join(_root_dir, 'tests', 'test_nodes_friends.txt')
#EDGES = os.path.join(_root_dir, 'tests', 'test_edges_friends.txt')
RANDSEED = 2
np.random.seed(RANDSEED)
PROP_TO_REMOVE = 1 #only removing this percent of nodes
FRACTION_OF_NODES = False
MEASURES = [nx.betweenness_centrality, 
			nx.degree_centrality,
			nx.closeness_centrality, 
			nx.eigenvector_centrality]
NETWORKS = {'B_R_BAC_SBS':['OM3','OM2','OM1','OM0']}
			#'B_R_BAC_SBS2':['OM3','OM2','OM1','OM0']}
			#'R_BAC_IDF':['OM3','OM2','OM1','OM0']} #changed OL to OM0 temporarily
# NETWORKS = {'trial1':['OM3'], ##trial networks to test faster
# 			'trial2':['OM3']}
#PLOT_BY = 'bytreatment'
PLOT_BY = 'bymeasure'

PATH = '/Users/sperez/Dropbox/1-Aria/LTSP_networks'
FIGURE_PATH = PATH
#FIGURE_NAME = 'Allnetworks'
FIGURE_NAME = 'SBS' +'_'+ PLOT_BY
DPI = 300


def make_graph(nodeFile, edgeFile):
	'''imports the node and edge file and makes the graph'''
	G = import_graph(nodeFile,edgeFile)
	return G

def get_multiple_graphs(networks, path):
	'''makes multiple graphs from names of networks and a file path'''
	graphs = {}
	for netName in networks:
		nodeFile = os.path.join(path,netName+'_nodes.txt')
		edgeFile = os.path.join(path,netName+'_edges.txt')
		graphs[netName] = make_graph(nodeFile,edgeFile)
		print "Made the networkx graph: "+netName
	return graphs

def get_network_fullnames(networkNames):
	networks = []
	for location,treatments in networkNames.iteritems():
		for t in treatments:
			networks.append(location+'_'+t)
	return networks,treatments

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
	startSize = len(nx.connected_components(G)[0])
	sizes.append(1)
	H = G.copy()

	nodes= G.nodes()
	np.random.shuffle(nodes)

	removal=int(len(nodes)*PROP_TO_REMOVE)-1

	for n in nodes[:removal]:
		H.remove_node(n)
		sizes.append(len(nx.connected_components(H)[0])/float(startSize)) #measure the relative size change
	return sizes


def target_attack(G, measure):
	'''Measure the size of the largest component of the graph
	as nodes are removed given the measure (degree or centrality 
	measure). The order of the nodes to be removed IS NOT updated
	after each removal.
	'''
	sizes = []
	startSize = len(nx.connected_components(G)[0])
	sizes.append(1)
	H = G.copy()

	values = [(n,v) for n,v in measure(G).iteritems()]

	values = sorted(values, key = lambda item: item[1], reverse = True)


	removal=int(len(values)*PROP_TO_REMOVE)-1

	for n in zip(*values)[0][:removal]:
		H.remove_node(n)
		sizes.append(len(nx.connected_components(H)[0])/float(startSize))  #measure the relative size change
	return sizes



def plot_robustness(data,filename):
	'''plots the simulations'''
	colors ='rgbkmy'

	# plotting locations in rows and centralities in columns
	fig, axes = plt.subplots(1)
	measures = ['random']
	measures.extend([m.__name__ for m in MEASURES])

	colors = {measure: ppl.colors.set2[i] for i,measure in enumerate(measures)}

	for measure in measures:
		values = data[measure]
		x = range(len(values))
		ppl.plot(axes, x, 
			values,
			label=str(measure))
			#color=[colors[measure] for measure in measures])

	ppl.legend(axes)  
	figureFile = os.path.join(FIGURE_PATH,filename+'_simulation'+'.png')
	fig.savefig(figureFile)
	print "Saving the figure file: ", figureFile
	return None


def plot_individual(networkNames,path):
	networks,treatments = get_network_fullnames(networkNames)
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

def multi_plot_robustness_by_treatment(multidata,filename,rowLabels,colLabels):
	'''plots the simulations in a multiplot: each row is a location and each column is a treatment'''
	colors ='rgbkmy'

	# plotting locations in rows and treatments in columns
	fig, axes = plt.subplots(len(rowLabels),len(colLabels))
	netNames = rowLabels
	measures = ['random'] + [m.__name__ for m in MEASURES]

	colors = {measure: ppl.colors.set1[i] for i,measure in enumerate(measures)}
	#print netNames, measures, len(rowLabels),len(colLabels), len(axes), colLabels*len(rowLabels)

	iterable = []
	for i,r in enumerate(rowLabels):
		for j,c in enumerate(colLabels):
			if len(rowLabels)>1:
				iterable.append((axes[i][j],r,c))
			else:
				iterable.append((axes[j],r,c))

	netLabeldone = []
	for ax,net,treatment in iterable:

		for measure in measures:
			values = multidata[net+'_'+treatment][measure]
			if FRACTION_OF_NODES:
				x = [float(r)/len(values) for r in range(len(values))]
			else:
				x = range(len(values))
			ppl.plot(ax,
				x, 
				values,
				label=str(measure),
				color=colors[measure])

		ax.set_title(treatment)
		if net not in netLabeldone:
			ax.set_ylabel(net)
			netLabeldone.append(net)
		# ax.set_xticklabels([str(tick)+'%' for tick in range(0,int(PROP_TO_REMOVE*100)+1,int(PROP_TO_REMOVE*100/5))])

	lgd = ppl.legend(loc=5, bbox_to_anchor=(7, 1, 1, 1)) # bbox_to_anchor=(4.2,2.5))

	figureFile = os.path.join(FIGURE_PATH,filename+'_simulation'+'.png')
	#fig.tight_layout()
	fig.set_size_inches(8*len(colLabels),5*len(rowLabels))
	fig.savefig(figureFile,dpi=DPI,  bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None


def plot_multiple(networkNames,path,columns):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,path)
	data = {}
	for netName,G in graphs.iteritems():
		randSizes = random_attack(G)
		data[netName] = {'random':randSizes}
		for m in MEASURES:
			targSizes = target_attack(G, m)
			data[netName][m.__name__] = targSizes
	if columns == 'bytreatment':
		multi_plot_robustness_by_treatment(data,FIGURE_NAME, networkNames.keys(), treatments)
	elif columns == 'bymeasure':
		multi_plot_robustness_by_measure(data,FIGURE_NAME, networkNames.keys(), treatments)
	return None


def multi_plot_robustness_by_measure(multidata,filename,rowLabels,treatments):
	'''plots the simulations in a multiplot: each row is a location and each column is a centrality measure'''
	colors ='rgbkmy'

	# plotting locations in rows and centralities in columns
	measures = ['random'] + [m.__name__ for m in MEASURES]
	fig, axes = plt.subplots(len(rowLabels),len(measures))
	netNames = rowLabels

	colors = {treatment: ppl.colors.set1[i] for i,treatment in enumerate(treatments)}
	#print netNames, measures, len(rowLabels),len(colLabels), len(axes), colLabels*len(rowLabels)

	iterable = []
	for i,r in enumerate(rowLabels):
		for j,c in enumerate(measures):
			if len(rowLabels)>1:
				iterable.append((axes[i][j],r,c))
			else:
				iterable.append((axes[j],r,c))

	netLabeldone = []
	for ax,net,measure in iterable:

		for t in treatments:
			values = multidata[net+'_'+t][measure]
			if FRACTION_OF_NODES:
				x = [float(r)/len(values) for r in range(len(values))]
			else:
				x = range(len(values))
			ppl.plot(ax,
				x, 
				values,
				label=str(t),
				color=colors[t])

		ax.set_title(measure)
		if net not in netLabeldone:
			ax.set_ylabel(net)
			netLabeldone.append(net)

	lgd = ppl.legend(loc='right', bbox_to_anchor=(1, 1, 1, 1))

	figureFile = os.path.join(FIGURE_PATH, filename+'_simulation'+'.png')
	#fig.tight_layout()
	fig.set_size_inches(7*len(treatments),3*len(rowLabels))
	fig.savefig(figureFile,dpi=DPI, bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None




if __name__ == "__main__":
	'''testing purposes'''
	#G = input_files(*sys.argv[1:])
	plot_multiple(NETWORKS,PATH,PLOT_BY)
	#plot_individual(NETWORKS,PATH)

'''
to do:
normalize yticks by original size giant component
switch the oms and the measures to make a diff graph
run on all networks
'''