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
import network_measures as nm

RANDSEED = 2
np.random.seed(RANDSEED)
DPI = 400 #resolution of plot #low for testing
ADD_RANDOM,ADD_SCALE = True, True #True,True
RAND_NAME = 'random_network_size_of_'
SCALE_NAME = 'scalefree_network_size_of_'

STRUCTURE_METRICS = [nm.number_of_nodes, 
					nm.number_of_edges,
					nm.average_degree, 
					nm.connectance, 
					nm.global_clustering_coefficient,
					nm.fraction_of_possible_triangles,
					#nm.size_of_largest_clique,
					nm.degree_assortativity,
					#nm.assortativity_of_degree_and_betweenness_centrality
					nm.diameter_of_largest_connected_component,
					#nm.average_path_on_largest_connected_component
					]

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
		G = make_graph(nodeFile,edgeFile)
		graphs[netName] = G
		print 'Made the networkx graph {0} with N = {1}, E = {2}.'.format(netName,G.number_of_nodes(),G.number_of_edges())
		
		##adding random graph for comparaison
		if ADD_RANDOM:
			M = nx.number_of_edges(G)
			N = nx.number_of_nodes(G)
			H = nx.gnm_random_graph(N,M,seed=RANDSEED)
			graphs[RAND_NAME+netName] = H
		if ADD_SCALE:
			N = nx.number_of_nodes(G)
			H = nx.scale_free_graph(N,seed=RANDSEED)
			UH = H.to_undirected()
			UH = nx.Graph(UH)
			graphs[SCALE_NAME+netName] = UH
	return graphs

def get_network_fullnames(networkNames):
	networks = []
	key = networkNames.keys()[0]
	if networkNames[key] == []:
		print 'here'
		return networkNames.keys(),None
	for location,treatments in networkNames.iteritems():
		location, treatments
		for t in treatments:
			networks.append(location+'_'+t)
	return networks,treatments


##########################################

##########################################

def plot_degree_distribution_per_treatment(net_path, networkNames, figurePath, plot_sequence):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,net_path)
	data = {}
	network = networkNames.keys()[0].split('_')
	network = network[1]

	# plotting locations in rows and treatments in columns
	fig, ax = plt.subplots(1)

	colors = {treatment: ppl.colors.set1[i] for i,treatment in enumerate(treatments)}

	for t,net in zip(treatments,networks):
		G = graphs[net]
		if plot_sequence:
			ax.set_title('Degree histogram of '+network+' network')
			ax.set_xlabel('nodes ranked by degree')
			ax.set_ylabel('degree')
			
			#to plot histogram
			degree_sequence = sorted(nx.degree(G).values(),reverse=True)
			
			ppl.plot(degree_sequence,
				marker='.',
				linestyle='-',
				label=str(t),
				color=colors[t])
		else:
			ax.set_title('Degree distribution of '+network+' network')
			ax.set_xlabel('degree')
			ax.set_ylabel('frequency of degree')
			N = G.number_of_nodes()
			ds = [] #each degree
			fds = [] #each degree's frequency
			degrees = sorted(nx.degree(G).values(),reverse=True)
			for d in set(degrees):
				ds.append(d)
				fds.append(float(degrees.count(d))/N)

			ppl.scatter(ds,
				fds,
				marker='.',
				#linestyle='-',
				label=str(t),
				color=colors[t])

	lgd = ppl.legend(bbox_to_anchor=(1.05, 1), loc=2)

	fig.set_size_inches(9,6)
	fig.savefig(figurePath, dpi=DPI, bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figurePath
	return None



##########################################

##########################################

def network_structure(net_path,networkNames, filename):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,net_path)
	if treatments != []:
		table = np.zeros(shape=(len(STRUCTURE_METRICS)+2, len(networkNames)*len(treatments)+1), dtype='S100')
		i,j = 0,1 # i is row, j is column
		column = ['Zones','Treatments']
		column.extend([sm.__name__.replace('_',' ').capitalize() for sm in STRUCTURE_METRICS])
		table[:,0]=column
		for location,treatments in networkNames.iteritems():
			table[i,j]=location
			for t in treatments:
				i+=1
				table[i,j]=t
				for sm in STRUCTURE_METRICS:
					print "For network for zone {0} treatment {1} calculating metric {2}".format(location,t,sm.__name__)
					i+=1
					G = graphs[location+'_'+t]
					table[i,j]=sm(G)
				j+=1
				i=0
	else:
		print 'rere'

	np.savetxt(os.path.join(net_path,filename), table, delimiter=",", fmt='%s')
	return None


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


def plot_multiple(net_path, networkNames, measures, plotby, fraction, figurePath):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,net_path)
	data = {}
	for netName,G in graphs.iteritems():
		print 'Running simulation on {0}.'.format(netName)
		rand_lc_sizes, rand_sc_sizes = random_attack(G, fraction)
		data[netName] = {'random':(rand_lc_sizes, rand_sc_sizes)}
		for m in measures:
			targ_lc_sizes, targ_sc_sizes = target_attack(G, m, fraction)
			data[netName][m.__name__] = (targ_lc_sizes, targ_sc_sizes)
	networkNamesPlot = networkNames.keys()
	if ADD_RANDOM:
		networkNamesPlot.extend([RAND_NAME+n for n in networkNames.keys()])
	if ADD_SCALE:
		networkNamesPlot.extend([SCALE_NAME+n for n in networkNames.keys()])
	if plotby == 'by_treatment':
		multi_plot_robustness_by_treatment(data, figurePath, networkNamesPlot, treatments, measures, fraction, net_path)
	elif plotby == 'by_measure':
		multi_plot_robustness_by_measure(data, figurePath, networkNamesPlot, treatments, measures, fraction, net_path)
	return None


def multi_plot_robustness_by_treatment(multidata,figurePath,rowLabels,colLabels, measures, fraction, net_path):
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

	net_label_done = []
	treatment_label_done = []
	x_axis_label_done = False

	#to add to legend
	ppl.plot([], [], color='black', linestyle='-', label='relative size of LCC')
	ppl.plot([], [], color='black', linestyle='--', label='avg size of other CC')


	for ax,net,treatment in iterable:

		for measure in measures:
			lc_values = multidata[net+'_'+treatment][measure][0]
			sc_values = multidata[net+'_'+treatment][measure][1]
			x = [float(r)/len(lc_values)*fraction for r in range(len(lc_values))]
			ppl.plot(ax,
				x, 
				lc_values,
				marker='.',
				linestyle='-',
				label=str(measure.replace('_',' ')),
				color=colors[measure])
			ppl.plot(ax,
				x, 
				sc_values,
				color=colors[measure],
				linestyle='--')
			
		if treatment not in treatment_label_done:
			ax.set_title(treatment)
			treatment_label_done.append(treatment)
		ax.set_title(treatment)
		if net not in net_label_done:
			ax.set_ylabel(net)
			net_label_done.append(net)

		if not x_axis_label_done:
			x_axis_label_done = True
			ax.set_xlabel('fraction of removed nodes')
		
	lgd = ppl.legend(bbox_to_anchor=(1.05, 1), loc=2)

	figureFile = os.path.join(net_path,figurePath)
	#fig.tight_layout()
	fig.set_size_inches(9*len(colLabels),7*len(rowLabels))
	fig.savefig(figureFile, dpi=DPI,  bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None

def multi_plot_robustness_by_measure(multidata,figurePath,rowLabels,treatments,measures,fraction, net_path):
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

	net_label_done = []
	measure_label_done = []
	x_axis_label_done = False

	#to add to legend
	ppl.plot([], [], color='black', marker= '.', linestyle='-', label='relative size of LCC')
	ppl.plot([], [], color='black', linestyle='--', label='avg size of other CC')

	for ax,net,measure in iterable:

		for t in treatments:
			lc_values = multidata[net+'_'+t][measure][0]
			sc_values = multidata[net+'_'+t][measure][1]
			x = [float(r)/len(lc_values)*fraction for r in range(len(lc_values))]
			ppl.plot(ax,
				x, 
				lc_values,
				marker='.',
				linestyle='-',
				label=str(t),
				color=colors[t])
			ppl.plot(ax,
				x, 
				sc_values,
				color=colors[t],
				linestyle='--')

		if measure not in measure_label_done:
			ax.set_title(measure)
			measure_label_done.append(measure)
		if net not in net_label_done:
			ax.set_ylabel(net)
			net_label_done.append(net)

		if not x_axis_label_done:
			x_axis_label_done = True
			ax.set_xlabel('fraction of removed nodes')

	lgd = ppl.legend(bbox_to_anchor=(1.05, 1), loc=2)

	figureFile = os.path.join(net_path, figurePath)
	#fig.tight_layout()
	fig.set_size_inches(9*len(treatments),9*len(rowLabels))
	fig.savefig(figureFile, dpi=DPI, bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None




'''
to do:
switch the oms and the measures to make a diff graph
run on all networks
'''