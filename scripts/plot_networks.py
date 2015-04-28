'''
Created on 27/03/2015

author: sperez8
'''

import sys, os
import argparse
import numpy as np
from network_simulation import *

#What to plot
import platform
if platform.system() == 'Windows':
	PATH = '\Users\Sarah\Desktop\LTSPnetworks'
else:
	PATH = '/Users/sperez/Desktop/LTSPnetworks'

FOLDER = 'by_treatment'
WHOLE_FOLDER = 'by_zone'
FIGURE_PATH = os.path.join(PATH,'plots')
SAMPLES_FILE = os.path.join(PATH, 'Bacterialtags_info_edited.txt')

INPUT_FOLDER = 'input'
INPUT_FILE_END = '_BAC-filtered-lineages_final.txt'

INDVAL_FOLDER = 'indtables'
INDVAL_FILE_END = '_indvals_combo_om_horizon.txt'

FEATURE_PATH = os.path.join(PATH,'tables')
FEATURE_FILE = 'feature_and_posnode_measures_table'
FEATURES = ['SoilHorizon']
BC_FEATURES = ['Betweenness centrality','SoilHorizon avg','SoilHorizon std','Abundance']
MEASURES = [nx.betweenness_centrality, 
			nx.degree_centrality,
			 ]
PERCENT_BC_NODES = 0.1

TAX_LEVEL = 'phylum'

TREATMENTS = ['OM0']#,'OM1','OM2','OM3']

PROP_TO_REMOVE = 1 #only removing this percent of nodes
MAX_Y_AXIS = None
DEGREE_SEQUENCE = False

def main(*argv):
	'''handles user input and runs plsa'''
	parser = argparse.ArgumentParser(description='This scripts analyzes co-occurrence networks')
	parser.add_argument('-path', help='Path where the networks are', default = PATH)
	parser.add_argument('-folder', help='Folder in path where the networks are', default = FOLDER)
	parser.add_argument('-networks', nargs='*', help='Which network to use: SBS, IDF, etc.')
	parser.add_argument('-simulate', help='Simulates node removal', action = 'store_true')
	parser.add_argument('-calculate', help='Calculates networks properties', action = 'store_true')
	parser.add_argument('-modules', help='Calculates module properties', action = 'store_true')
	parser.add_argument('-distribution', help='Plots degree distribution', action = 'store_true')
	parser.add_argument('-assess', help='Assess ecological properties', action = 'store_true')
	parser.add_argument('-maketable', help='Make OTU table with eclogical measures', action = 'store_true')
	parser.add_argument('-edgetype', help='Specify which types edges to use', default = 'both')
	#arguments used when running simulations
	parser.add_argument('-fraction', help='Fraction of nodes to remove', default = PROP_TO_REMOVE)
	parser.add_argument('-addrandom', help='Runs simulation on random network of same size', action = 'store_true')
	parser.add_argument('-addscalefree', help='Runs simulation on scale network of same size', action = 'store_true')
	parser.add_argument('-treatment', help='Makes a plot for each treatment', action = 'store_true')
	parser.add_argument('-measure', help='Makes a plot for each centrality measure', action = 'store_true')
	parser.add_argument('-showcomponents', help='Average size of large component fragments to show', default = MAX_Y_AXIS)
	parser.add_argument('-wholenetwork', help='Makes a plot for whole network, not per treatments', action = 'store_true')
	parser.add_argument('-boxplot', help='Makes a boxplot per taxonomic level of otu centrality', action = 'store_true')
	parser.add_argument('-level', help='Selects taxonomic level at which to make the boxplot', default = TAX_LEVEL)
	parser.add_argument('-bcplot', help='Makes a boxplot per treatment high BC otu features', action = 'store_true')
	parser.add_argument('-percentnodes', help='Select the proportion of high bc nodes to plot', default = PERCENT_BC_NODES)
	parser.add_argument('-vennplot', help='Makes a venn diagram of high BC otu per ecozone', action = 'store_true')

	args = parser.parse_args()
	
	#check that one of the options is true
	choices = [args.simulate,args.distribution,args.calculate,
				args.assess,args.maketable,args.boxplot,
				args.modules,args.bcplot,args.vennplot]
	if sum([1 for c in choices if c])>1 or sum([1 for c in choices if c])==0:
		print "\n***You must specify one of the three options to calculate porperties of, run simulations on or plot networks.***\n"
		parser.print_help()
		sys.exit()	

	if args.edgetype not in ['both','pos','neg']:
		print "\n***You must specify what edges you want to use to build the network: both, pos or neg.***\n"
		parser.print_help()
		sys.exit()

	if args.wholenetwork:
		treatments = None
		args.folder = WHOLE_FOLDER
	else:
		treatments = TREATMENTS

	edgetype = args.edgetype
	net_path = os.path.join(args.path,args.folder)
	print net_path
	if args.folder == 'by_zone':
		networks = {('BAC_'+n if 'BAC_' not in n else n):[] for n in args.networks}
	else:
		networks = {('BAC_'+n if 'BAC_' not in n else n):treatments for n in args.networks}


	###depending on option specified, choose different things
	if args.calculate:
		print "\nCalculating structural properties on "+edgetype+" type of edges of networks:"
		print ", ".join(networks), '\n'
		filePath = os.path.join(FIGURE_PATH,'table_of_measures_'+'_'.join(args.networks)+'_'+edgetype+'.txt')
		print filePath
		network_structure(net_path,networks,filePath,edgetype, os.path.join(PATH,INPUT_FOLDER),INPUT_FILE_END, FEATURE_PATH, FEATURE_FILE)

	elif args.modules:
		print "\nCalculating structural properties on "+edgetype+" type of edges of modules in networks:"
		print ", ".join(networks), '\n'
		filePath = os.path.join(FIGURE_PATH,'table_of_module_measures_'+'_'.join(args.networks)+'_'+edgetype+'.txt')
		print filePath
		module_structure(net_path,networks,filePath,edgetype, os.path.join(PATH,INPUT_FOLDER),INPUT_FILE_END, FEATURE_PATH, FEATURE_FILE)


	elif args.assess:
		print "\nCalculating ecological metrics of sample collection for the following networks:"
		print ", ".join(networks), '\n'
		filePath = os.path.join(FIGURE_PATH,'ecological_measures_'+'_'.join(args.networks)+'.txt')
		make_ecological_table(net_path,networks,filePath,edgetype,os.path.join(PATH,INPUT_FOLDER),INPUT_FILE_END)

	elif args.maketable:
		print "\nMaking OTU table with ecological metrics for the following networks:"
		print ", ".join(networks), '\n'
		make_OTU_feature_table(net_path, networks, os.path.join(PATH,INPUT_FOLDER),INPUT_FILE_END,os.path.join(PATH,INDVAL_FOLDER),INDVAL_FILE_END, SAMPLES_FILE, FEATURES, FEATURE_PATH, FEATURE_FILE)

	elif args.distribution:
		for net in networks.keys():
			if DEGREE_SEQUENCE:
				figureName = 'plot_distribution_'+net+'_'+edgetype+'_sequence'+'.png'
			else:
				figureName = 'plot_distribution_'+net+'_'+edgetype+'.png'
			figurePath = os.path.join(FIGURE_PATH,figureName)
			print "\nPlotting the degree distribution on "+edgetype+" type of edges of network ", net
			plot_degree_distribution_per_treatment(net_path, {net: networks[net]}, figurePath, DEGREE_SEQUENCE, edgetype)

	elif args.boxplot:
		percentNodes = float(args.percentnodes)
		level = args.level
		if level not in TAXONOMY:
			print level, "is not a taxonomic level"
			sys.exit()
		print "\nPlotting "+level+" centrality for OTUs in the following networks with "+edgetype+" type of edges:"
		print ", ".join(networks), '\n'
		centrality_plot(net_path,networks,FIGURE_PATH,FEATURE_PATH, FEATURE_FILE,level,percentNodes)

	elif args.vennplot:
		percentNodes = float(args.percentnodes)
		level = args.level
		if level not in TAXONOMY:
			print level, "is not a taxonomic level"
			sys.exit()
		print "\nPlotting "+level+" venn diagrma of central OTUs per ecozone with "+edgetype+" type of edges:"
		print ", ".join(networks), '\n'
		plot_venn_diagram(net_path,networks,FIGURE_PATH,FEATURE_PATH, FEATURE_FILE,level,percentNodes)


	elif args.bcplot:
		percentNodes = float(args.percentnodes)
		print "\nPlotting different features of high betweenness centrality OTUs in the following networks with "+edgetype+" type of edges:"
		print ", ".join(networks), '\n'
		keystone_quantitative_feature_plot(net_path,networks,FIGURE_PATH,FEATURE_PATH, FEATURE_FILE, BC_FEATURES, percentNodes)


	elif args.simulate:
		if not args.treatment and not args.measure:
			print "\n***You must specify to plot by treatment or by measure.***\n"
			parser.print_help()
			sys.exit()
		if args.treatment:
			plot_by = 'by_treatment'
		elif args.measure:
			plot_by = 'by_measure'
		if args.addscalefree:
			add_scalefree = True
		else: 
			add_scalefree = False
		if args.addrandom:
			add_random = True
		else:
			add_random = False
		max_y = args.showcomponents
		if max_y:
			max_y = float(max_y)

		fraction = float(args.fraction)
		figureName = 'plot_'+'_'.join(args.networks)+'_'+edgetype+'_'+ plot_by +'_prop='+str(fraction)+'_maxy='+str(max_y)+'.png'
		figurePath = os.path.join(FIGURE_PATH,figureName)
		measures = MEASURES

		print "\nSimulating and plotting the robustness on "+edgetype+" type of edges of networks:"
		print ", ".join(networks)
		print "and plotting "+str(fraction)+" fraction of nodes "+plot_by+" and with following measures:"
		print ", ".join([m.__name__ for m in measures])
		print "\n"
		plot_multiple(net_path, networks, measures, plot_by, fraction, figurePath, edgetype, add_random, add_scalefree, max_y)
	
if __name__ == "__main__":
	main(*sys.argv[1:])




