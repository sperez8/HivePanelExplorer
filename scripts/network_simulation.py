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

RANDSEED = 2
np.random.seed(RANDSEED)
FRACTION_OF_NODES = True
DPI = 200 #resolution of plot


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



def random_attack(G,fraction):
	'''Measure the size of the largest component of the graph
	as nodes are removed randomly'''
	lc_sizes = [] #relative size of big component
	sc_sizes = [] #avg size of smaller components
	startSize = len(nx.connected_components(G)[0])
	lc_sizes.append(1)
	sc_sizes.append(1)
	H = G.copy()

	nodes= G.nodes()
	np.random.shuffle(nodes)

	removal=int(len(nodes)*fraction)-1 #can't remove last node, otherwise there is nothing to measure!

	for n in nodes[:removal]:
		H.remove_node(n)
		components = nx.connected_components(H)
		lc_sizes.append(len(components[0])/float(startSize)) #measure the relative size change
		if len(components)>1:
			sc_sizes.append(np.mean([len(c) for c in components[1:]]))
		else:
			sc_sizes.append(1.0)
	return lc_sizes,sc_sizes


def target_attack(G, measure,fraction):
	'''Measure the size of the largest component of the graph
	as nodes are removed given the measure (degree or centrality 
	measure). The order of the nodes to be removed IS NOT updated
	after each removal.
	'''
	lc_sizes = [] #relative size of big component
	sc_sizes = [] #avg size of smaller components
	startSize = len(nx.connected_components(G)[0])
	lc_sizes.append(1)
	sc_sizes.append(1)
	H = G.copy()

	values = [(n,v) for n,v in measure(G).iteritems()]

	values = sorted(values, key = lambda item: item[1], reverse = True)

	removal=int(len(values)*fraction)-1 #can't remove last node, otherwise there is nothing to measure!

	for n in zip(*values)[0][:removal]:
		H.remove_node(n)
		components = nx.connected_components(H)
		lc_sizes.append(len(components[0])/float(startSize))  #measure the relative size change
		if len(components)>1:
			sc_sizes.append(np.mean([len(c) for c in components[1:]]))
		else:
			sc_sizes.append(1.0)
	return lc_sizes,sc_sizes



def plot_robustness(data,filename):
	'''plots the simulations'''

	# plotting locations in rows and centralities in columns
	fig, axes = plt.subplots(1)
	measures = ['random'] + [m.__name__ for m in measures]
	colors = {measure: ppl.colors.set2[i] for i,measure in enumerate(measures)}

	for measure in measures:
		values = data[measure]
		x = range(len(values))
		ppl.plot(axes, x, 
			values,
			label=str(measure))
			#color=[colors[measure] for measure in measures])

	ppl.legend(axes)  
	figureFile = os.path.join(net_path,filename)
	fig.savefig(figureFile)
	print "Saving the figure file: ", figureFile
	return None


def plot_individual(path,networkNames,fraction):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,path)

	for netName,G in graphs.iteritems():
		rand_lc_sizes, rand_sc_sizes = random_attack(G, fraction)
		data = {}
		data['random']= (rand_lc_sizes, rand_sc_sizes)
		for m in measures:
			targ_lc_sizes, targ_sc_sizes = target_attack(G, m, fraction)
			data[m.__name__] = (targ_lc_sizes, targ_sc_sizes)
		plot_robustness(data, netName)
	return None


def plot_multiple(net_path, networkNames, measures, plotby, fraction, figure_name):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,net_path)
	data = {}
	for netName,G in graphs.iteritems():
		rand_lc_sizes, rand_sc_sizes = random_attack(G, fraction)
		data[netName] = {'random':(rand_lc_sizes, rand_sc_sizes)}
		for m in measures:
			targ_lc_sizes, targ_sc_sizes = target_attack(G, m, fraction)
			data[netName][m.__name__] = (targ_lc_sizes, targ_sc_sizes)
	if plotby == 'by treatment':
		multi_plot_robustness_by_treatment(data, figure_name, networkNames.keys(), treatments, measures, fraction, net_path)
	elif plotby == 'by measure':
		multi_plot_robustness_by_measure(data, figure_name, networkNames.keys(), treatments, measures, fraction, net_path)
	return None


def multi_plot_robustness_by_treatment(multidata,filename,rowLabels,colLabels, measures, fraction, net_path):
	'''plots the simulations in a multiplot: each row is a location and each column is a treatment'''

	# plotting locations in rows and treatments in columns
	fig, axes = plt.subplots(len(rowLabels),len(colLabels))
	netNames = rowLabels

	measures = ['random'] + [m.__name__ for m in measures]

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
			lc_values = multidata[net+'_'+treatment][measure][0]
			sc_values = multidata[net+'_'+treatment][measure][1]
			if FRACTION_OF_NODES:
				x = [float(r)/len(lc_values) for r in range(len(lc_values))]
			else:
				x = range(len(lc_values))
			ppl.plot(ax,
				x, 
				lc_values,
				label=str(measure),
				color=colors[measure])
			ppl.plot(ax,
				x, 
				sc_values,
				label=str(measure),
				color=colors[measure])

		ax.set_title(treatment)
		if net not in netLabeldone:
			ax.set_ylabel(net)
			netLabeldone.append(net)
		# ax.set_xticklabels([str(tick)+'%' for tick in range(0,int(fraction*100)+1,int(fraction*100/5))])

	lgd = ppl.legend(loc=5, bbox_to_anchor=(7, 1, 1, 1)) # bbox_to_anchor=(4.2,2.5))

	figureFile = os.path.join(net_path,filename)
	#fig.tight_layout()
	fig.set_size_inches(8*len(colLabels),5*len(rowLabels))
	fig.savefig(figureFile,dpi=DPI,  bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None

def multi_plot_robustness_by_measure(multidata,filename,rowLabels,treatments,measures,fraction, net_path):
	'''plots the simulations in a multiplot: each row is a location and each column is a centrality measure'''

	# plotting locations in rows and centralities in columns
	measures = ['random'] + [m.__name__ for m in measures]
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
			lc_values = multidata[net+'_'+t][measure]
			if FRACTION_OF_NODES:
				x = [float(r)/len(lc_values) for r in range(len(lc_values))]
			else:
				x = range(len(lc_values))
			ppl.plot(ax,
				x, 
				lc_values,
				label=str(t),
				color=colors[t])


		ax.set_title(measure)
		if net not in netLabeldone:
			ax.set_ylabel(net)
			netLabeldone.append(net)

	lgd = ppl.legend(loc='right', bbox_to_anchor=(1, 1, 1, 1))

	figureFile = os.path.join(net_path, filename)
	#fig.tight_layout()
	fig.set_size_inches(7*len(treatments),3*len(rowLabels))
	fig.savefig(figureFile,dpi=DPI, bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None




'''
to do:
switch the oms and the measures to make a diff graph
run on all networks
'''