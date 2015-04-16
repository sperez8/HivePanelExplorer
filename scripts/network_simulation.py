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
import math

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
RAND_NAME = 'random_network_size_of_'
SCALE_NAME = 'scalefree_network_size_of_'
FILTER_NON_OTUS = True
MARKER_SIZE = 200

NOT_A_NODE_VALUE = 'NA'

STRUCTURE_METRICS = [nm.number_of_nodes, 
					nm.number_of_edges,
					nm.number_of_components,
					nm.size_of_components,
					nm.number_of_nodes_of_largest_connected_component, 
					nm.number_of_edges_of_largest_connected_component,
					nm.average_degree, 
					nm.connectance, 
					nm.global_clustering_coefficient,
					nm.fraction_of_possible_triangles,
					#nm.size_of_largest_clique,
					nm.diameter_of_largest_connected_component,
					#nm.average_path_on_largest_connected_component,
					nm.degree_assortativity,
					nm.correlation_of_degree_and_betweenness_centrality,
					]

INPUT_METRICS = [nm.richness,
				nm.shannon_diversity,
				]
OTU_METRICS = [nm.correlation_of_degree_and_depth,
				nm.correlation_of_edge_depth,
				]
MEASURES = [nm.node_degrees,
			nx.betweenness_centrality, 
			nx.closeness_centrality, 
			nm.in_largest_connected_component,
			]

PHYLA = ['Proteobacteria',
			'Acidobacteria',
			'Actinobacteria',
			'Chloroflexi',
			'unclassified',
			'Bacteroidetes',
			'Planctomycetes',
			'Verrucomicrobia',
			'Gemmatimonadetes',
			'WCHB1-60',
			'Cyanobacteria',
			]

def make_graph(nodeFile, edgeFile,edgetype):
	'''imports the node and edge file and makes the graph'''
	G = import_graph(nodeFile,edgeFile,edgetype,FILTER_NON_OTUS)
	return G

def get_multiple_graphs(networks, path, edgetype, add_random, add_scalefree, LC=False):
	'''makes multiple graphs from names of networks and a file path'''
	graphs = {}
	for netName in networks:
		nodeFile = os.path.join(path,netName+'_nodes.txt')
		edgeFile = os.path.join(path,netName+'_edges.txt')
		G = make_graph(nodeFile,edgeFile,edgetype)
		if LC:
			G = nx.connected_component_subgraphs(G)[0]
		graphs[netName] = G
		print 'Made the networkx graph {0} with N = {1}, E = {2}.'.format(netName,G.number_of_nodes(),G.number_of_edges())
		
		##adding random graph for comparaison
		if add_random:
			M = nx.number_of_edges(G)
			N = nx.number_of_nodes(G)
			H = nx.gnm_random_graph(N,M,seed=RANDSEED)
			if LC:
				H = nx.connected_component_subgraphs()[0]
			graphs[RAND_NAME+netName] = H
		if add_scalefree:
			N = nx.number_of_nodes(G)
			H = nx.scale_free_graph(N,seed=RANDSEED)
			UH = H.to_undirected()
			UH = nx.Graph(UH)
			if LC:
				UH = nx.connected_component_subgraphs(UH)[0]			
			graphs[SCALE_NAME+netName] = UH
	return graphs

def get_network_fullnames(networkNames):
	networks = []
	key = networkNames.keys()[0]
	if networkNames[key] == []:
		return networkNames.keys(),None
	for location,treatments in networkNames.iteritems():
		location, treatments
		for t in treatments:
			networks.append(location+'_'+t)
	return networks,treatments



#####################################################################################

#####################################################################################

#####################################################################################


def load_samples_info(samplesFile):
	samplesTable = np.loadtxt(samplesFile, comments=None, delimiter='\t', dtype='S100')
	return samplesTable

def get_info_per_samples(samplesFile, samples, feature):
	'''gets a list of samples and an ecological feature,
	 and returns a dicttionary of sample values for the desired feature'''
	sampleInfo = {}
	table = load_samples_info(samplesFile)
	for s in samples:
		row = np.where(table[:,0]==s)[0][0]
		column = np.where(table[0,:]==feature)[0][0]
		sampleInfo[s] = table[row,column]
	return sampleInfo

def make_OTU_feature_table(net_path, networkNames, inputFolder, inputFileEnd, samplesFile, features, path, featureFile):
	'''makes an OTU table with avg depth and othe features per OTU'''

	networks,treatments = get_network_fullnames(networkNames)
	if len(MEASURES)>=1:
		graphs = get_multiple_graphs(networks, net_path, 'pos', False, False)

	otuTable = {}
	for n in networks:
		otuTable[n] = np.loadtxt(os.path.join(inputFolder,n.replace('BAC_','')+inputFileEnd), dtype='S100')

	header = ['OTUs','Abundance']
	for f in features:
		header.append(f+ ' avg')
		header.append(f+ ' std')
	header.extend([m.__name__.replace('_',' ').capitalize() for m in MEASURES])
	header.append('Taxonomy')
				
	print header

	for location,treatments in networkNames.iteritems():
		for t in treatments:
			abundances = otuTable[location+'_'+t]
			sampleNames = abundances[0,1:-1]
			sampleCounts = abundances[1:-1,1:-1].astype(np.float).sum(axis=0)
			featureTable = np.zeros(shape=(abundances.shape[0]-1,3+len(features)*2+len(MEASURES)), dtype='S100')
			featureTable[0,:] = np.array(header)
			for i,f in enumerate(features):
				print "For input table from zone {0} treatment {1} calculating feature {2}".format(location,t,f)
				fdist = get_info_per_samples(samplesFile, sampleNames, f)				
				for r,row in enumerate(abundances[1:-1,]):
					otu = row[0]
					ab = row[1:-1].astype(np.float)/sampleCounts
					tax = row[-1]
					featureTable[r+1][0]=otu
					featureTable[r+1][1]=np.mean(ab)
					featureTable[r+1][-1]=tax
					fcount = []
					stdCount = []
					featureValues = [float(fdist[s]) for s in sampleNames]
					avg = np.average(featureValues, weights = ab)
					std = math.sqrt(np.average((featureValues-avg)**2, weights=ab))
					featureTable[r+1][i+2]=avg
					featureTable[r+1][i+3]=std

			column_bias = 2+len(features)*2
			for i,m in enumerate(MEASURES):
				print "For input table from zone {0} treatment {1} calculating measure {2}".format(location,t,m.__name__)
				col = i+column_bias
				G = graphs[location+'_'+t]
				values = m(G)
				for r,row in enumerate(abundances[1:-1,]):
					otu = row[0]
					measureValue = 0
					if otu in G.nodes():
						measureValue = values[otu]
					elif 'OTU-'+otu in G.nodes():
						measureValue = values['OTU-'+otu]
					else:
						measureValue = NOT_A_NODE_VALUE				
					featureTable[r+1][col]=measureValue

			fileName = featureFile+'_{0}_{1}.txt'.format(location,t)
			tableFile = os.path.join(path,fileName)
			print "Saving table: ",tableFile

			np.savetxt(tableFile, featureTable, delimiter="\t", fmt='%s')
	return None

def plot_degree_distribution_per_treatment(net_path, networkNames, figurePath, plot_sequence, edgetype):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks, net_path, edgetype, False, False)
	data = {}
	network = networkNames.keys()[0].split('_')
	network = network[1]

	# plotting locations in rows and treatments in columns
	fig, ax = plt.subplots(1)

	colors = {treatment: ppl.colors.set1[i] for i,treatment in enumerate(treatments)}

	for t,net in zip(treatments,networks):
		G = graphs[net]
		if plot_sequence:
			ax.set_title('Degree histogram of '+network+' network with '+edgetype+' type of edges')
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
			ax.set_title('Degree distribution of '+network+' network with '+edgetype+' type of edges')
			ax.set_xlabel('degree')
			ax.set_ylabel('frequency of degree')
			ax.set_yscale('log')
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
				s=MARKER_SIZE,
				#linestyle='-',
				label=str(t),
				color=colors[t])

		

	#ppl.scatter(ds,[max(fds)*math.exp(-d/6.0) for d in ds],color='black')
	ax.set_ylim([0,1])

	lgd = ppl.legend(bbox_to_anchor=(1.05, 1), loc=2)

	fig.set_size_inches(10,9)
	fig.savefig(figurePath, dpi=DPI, bbox_extra_artists=(lgd,), bbox_inches='tight')
	print "Saving the figure file: ", figurePath
	return None

def make_ecological_table(net_path, networkNames, filePath, edgetype, inputFolder, inputFileEnd):
	networks,treatments = get_network_fullnames(networkNames)
	#graphs = get_multiple_graphs(networks,net_path,edgetype, False, False)

	otuTable = {}
	for n in networks:
		otuTable[n] = np.loadtxt(os.path.join(inputFolder,n.replace('BAC_','')+inputFileEnd), dtype='S100')

	table = np.zeros(shape=(len(INPUT_METRICS)+2, len(networkNames)*len(treatments)+1), dtype='S100')
	i,j = 0,1 # i is row, j is column
	column = ['Zones','Treatments']
	column.extend([sm.__name__.replace('_',' ').capitalize() for sm in INPUT_METRICS])
	table[:,0]=column
	for location,treatments in networkNames.iteritems():
		table[i,j]=location
		for t in treatments:
			i+=1
			table[i,j]=t
			for im in INPUT_METRICS:
				print "For input table from zone {0} treatment {1} measuring {2}".format(location,t,im.__name__)
				i+=1
				S = otuTable[location+'_'+t]
				table[i,j]=im(S)
			j+=1
			i=0

	print "Saving table: ", filePath

	np.savetxt(filePath, table, delimiter="\t", fmt='%s')
	return None

def centrality_plot(net_path, networkNames, figurePath, featurePath, featureFile):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,net_path,'pos', False, False)
	colName = nx.betweenness_centrality.__name__.replace('_',' ').capitalize()

	for location,treatments in networkNames.iteritems():
		for t in treatments:
			G = graphs[location+'_'+t]
			featureTableFile = os.path.join(featurePath,featureFile+'_{0}_{1}.txt'.format(location,t))
			featureTable = np.loadtxt(featureTableFile,delimiter='\t', dtype='S100')
			col = np.where(featureTable[0,:]==colName)[0][0]
			centralities = []
			for i,p in enumerate(PHYLA):
				centralities.append([])
				for n in G.nodes():
					row = nm.findRow(n,featureTable)
					if p in featureTable[row][-1]:
						value = featureTable[row][col]
						if value != NOT_A_NODE_VALUE and value !='0.0':
							centralities[i].append(float(value))

			labels = [p+' ('+str(len(centralities[i]))+')' for i,p in enumerate(PHYLA)]
			fig, ax = plt.subplots()
			ppl.boxplot(ax, centralities, xticklabels = labels)

			title = "Centrality of phyla present in network {0} with treatment {1}".format(location,t)
			figureTitle = fig.suptitle(title, horizontalalignment='center', fontsize=20)

			fig.set_size_inches(3*len(PHYLA),5)
			figureFile = os.path.join(net_path,figurePath,'centrality_plot_'+location+'_'+t+'.png')
			fig.savefig(figureFile, dpi=DPI,bbox_inches='tight')
			print "Saving the figure file: ", figureFile
	return None

def network_structure(net_path, networkNames, filePath, edgetype, inputFolder, inputFileEnd,featurePath, featureFile):
	networks,treatments = get_network_fullnames(networkNames)
	print networks, treatments
	graphs = get_multiple_graphs(networks,net_path,edgetype, False, False)
	#sys.exit()
	otuTable = {}
	for n in networks:
		otuTable[n] = np.loadtxt(os.path.join(inputFolder,n.replace('BAC_','')+inputFileEnd), dtype='S100')

	if treatments != []:
		table = np.zeros(shape=(len(INPUT_METRICS)+len(STRUCTURE_METRICS)+len(OTU_METRICS)+2, len(networkNames)*len(treatments)+1), dtype='S100')
		i,j = 0,1 # i is row, j is column
		column = ['Zones','Treatments']
		column.extend([sm.__name__.replace('_',' ').capitalize() for sm in INPUT_METRICS])
		column.extend([sm.__name__.replace('_',' ').capitalize() for sm in STRUCTURE_METRICS])
		column.extend([om.__name__.replace('_',' ').capitalize() for om in OTU_METRICS])
		table[:,0]=column
		for location,treatments in networkNames.iteritems():
			table[i,j]=location
			for t in treatments:
				i+=1
				table[i,j]=t
				for im in INPUT_METRICS:
					print "For input table from zone {0} treatment {1} measuring {2}".format(location,t,im.__name__)
					i+=1
					S = otuTable[location+'_'+t]
					table[i,j]=im(S)
				for sm in STRUCTURE_METRICS:
					print "For network for zone {0} treatment {1} calculating metric {2}".format(location,t,sm.__name__)
					i+=1
					G = graphs[location+'_'+t]
					table[i,j]=sm(G)
				for om in OTU_METRICS:
					print "For network for zone {0} treatment {1} calculating metric {2}".format(location,t,om.__name__)
					i+=1
					G = graphs[location+'_'+t]
					featureTableFile = os.path.join(featurePath,featureFile+'_{0}_{1}.txt'.format(location,t))
					featureTable = np.loadtxt(featureTableFile,delimiter='\t', dtype='S100')
					table[i,j]=om(G,featureTable)
				j+=1
				i=0
	else:
		print 'Can only do for multiple treatments. FIX ME'

	np.savetxt(filePath, table, delimiter="\t", fmt='%s')
	return None

def plot_multiple(net_path, networkNames, measures, plotby, fraction, figurePath, edgetype, add_random, add_scalefree, max_y):
	networks,treatments = get_network_fullnames(networkNames)
	graphs = get_multiple_graphs(networks,net_path,edgetype, add_random, add_scalefree, LC=True)
	data = {}
	for netName,G in graphs.iteritems():
		print 'Running simulation on {0}.'.format(netName)
		rand_lc_sizes, rand_sc_sizes = random_attack(G, fraction)
		data[netName] = {'random':(rand_lc_sizes, rand_sc_sizes)}
		for m in measures:
			targ_lc_sizes, targ_sc_sizes = target_attack(G, m, fraction)
			data[netName][m.__name__] = (targ_lc_sizes, targ_sc_sizes)
	networkNamesPlot = networkNames.keys()
	title = 'Robustness simulation on LC of networks {0} with {1} type of edges'.format(','.join([n.replace('BAC_','') for n in networkNamesPlot]), edgetype)
	if add_random:
		networkNamesPlot.extend([RAND_NAME+n for n in networkNames.keys()])
	if add_scalefree:
		networkNamesPlot.extend([SCALE_NAME+n for n in networkNames.keys()])
	if plotby == 'by_treatment':
		multi_plot_robustness_by_treatment(data, figurePath, networkNamesPlot, treatments, measures, fraction, net_path, title, max_y)
	elif plotby == 'by_measure':
		multi_plot_robustness_by_measure(data, figurePath, networkNamesPlot, treatments, measures, fraction, net_path, title, max_y)
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

def multi_plot_robustness_by_treatment(multidata,figurePath,rowLabels,colLabels, measures, fraction, net_path, title, max_y):
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

	min_yvalue = 1
	max_yvalue = 1
	for ax,net,treatment in iterable:

		for measure in measures:
			lc_values = multidata[net+'_'+treatment][measure][0]
			sc_values = multidata[net+'_'+treatment][measure][1]
			min_yvalue = min(min_yvalue ,min(lc_values))
			max_yvalue = max(max_yvalue ,max(sc_values))
			x = [float(r)*fraction for r in range(len(lc_values))]
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
			ax.set_xlabel('Number of removed nodes')

	for ax in axes:
		ax.set_autoscaley_on(False)
		if max_y and max_yvalue > max_y:
			max_yvalue = max_y
		ax.set_ylim([min_yvalue,max_yvalue])

	figureTitle = fig.suptitle(title,
         horizontalalignment='center',
         fontsize=20) 

	lgd = ppl.legend(bbox_to_anchor=(1.05, 1), loc=2)

	figureFile = os.path.join(net_path,figurePath)
	fig.set_size_inches(10*len(colLabels),7*len(rowLabels))
	fig.savefig(figureFile, dpi=DPI,  bbox_extra_artists=(lgd,figureTitle), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None

def multi_plot_robustness_by_measure(multidata,figurePath,rowLabels,treatments,measures,fraction, net_path, title, max_y):
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

	min_yvalue = 1
	max_yvalue = 1
	for ax,net,measure in iterable:

		for t in treatments:
			lc_values = multidata[net+'_'+t][measure][0]
			sc_values = multidata[net+'_'+t][measure][1]
			min_yvalue = min(min_yvalue ,min(lc_values))
			max_yvalue = max(max_yvalue ,max(sc_values))
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

	for ax in axes:
		ax.set_autoscaley_on(False)
		if max_y and max_yvalue > max_y:
			max_yvalue = max_y
		ax.set_ylim([min_yvalue,max_yvalue])

	figureTitle = fig.suptitle(title,
         horizontalalignment='center',
         fontsize=20)

	lgd = ppl.legend(bbox_to_anchor=(1.05, 1), loc=2)

	figureFile = os.path.join(net_path, figurePath)
	#fig.tight_layout()
	fig.set_size_inches(9*len(treatments),9*len(rowLabels))
	fig.savefig(figureFile, dpi=DPI, bbox_extra_artists=(lgd,figureTitle), bbox_inches='tight')
	print "Saving the figure file: ", figureFile
	return None











