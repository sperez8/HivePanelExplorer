'''
Created on 27/03/2015

author: sperez8
'''

import sys, os
import argparse
import numpy as np
from network_simulation import *

#What to plot
PATH = '/Users/sperez/Desktop/LTSPnetworks'
FOLDER = 'by_treatment'
FIGURE_PATH = os.path.join(PATH,'plots')

TREATMENTS = ['OM3','OM2','OM1','OM0']
MEASURES = [nx.betweenness_centrality, 
			nx.degree_centrality,
			nx.closeness_centrality, 
			nx.eigenvector_centrality]

PROP_TO_REMOVE = 1 #only removing this percent of nodes
DEGREE_SEQUENCE = False

def main(*argv):
	'''handles user input and runs plsa'''
	parser = argparse.ArgumentParser(description='This scripts produces robustness plots for networks')
	parser.add_argument('-path', help='Path where the networks are', default = PATH)
	parser.add_argument('-folder', help='Folder in path where the networks are', default = FOLDER)
	parser.add_argument('-networks', nargs='*', help='Which network to use: SBS, IDF, etc.')
	parser.add_argument('-simulate', help='Simulates node removal', action = 'store_true')
	parser.add_argument('-calculate', help='Calculates networks properties', action = 'store_true')
	parser.add_argument('-distribution', help='Plots degree distribution', action = 'store_true')
	parser.add_argument('-edgetype', help='Specify which types edges to use', default = 'both')
	#arguments used when running simulations
	parser.add_argument('-fraction', help='Fraction of nodes to remove', default = PROP_TO_REMOVE)
	parser.add_argument('-addrandom', help='Runs simulation on random network of same size', action = 'store_true')
	parser.add_argument('-addscalefree', help='Runs simulation on scale network of same size', action = 'store_true')
	parser.add_argument('-treatment', help='Makes a plot for each treatment', action = 'store_true')
	parser.add_argument('-measure', help='Makes a plot for each centrality measure', action = 'store_true')
	
	args = parser.parse_args()
	
	#check that one of the options is true
	choices = [args.simulate,args.distribution,args.calculate]
	if sum([1 for c in choices if c])>1:
		print "\n***You must specify one of the three options to calculate, simulate or plot the distribution.***\n"
		parser.print_help()
		sys.exit()	

	if (not args.simulate and not args.distribution and not args.calculate):
		print "\n***You must specify what you want to plot or measure.***\n"
		parser.print_help()
		sys.exit()

	if args.edgetype not in ['both','pos','neg']:
		print "\n***You must specify what edges you want to use to build the network: both, pos or neg.***\n"
		parser.print_help()
		sys.exit()

	edgetype = args.edgetype
	net_path = os.path.join(args.path,args.folder)
	if args.folder == 'by_zone':
		networks = {('BAC_'+n if 'BAC_' not in n else n):[] for n in args.networks}
	else:
		networks = {('BAC_'+n if 'BAC_' not in n else n):TREATMENTS for n in args.networks}

	if args.calculate:
		print "\nCalculating structural properties of networks:"
		print ", ".join(networks), '\n'
		fileName = 'table_of_measures_'+'_'.join(args.networks)+'_'+edgetype+'.csv'
		network_structure(net_path,networks,fileName,edgetype)

	elif args.distribution:
		for net in networks.keys():
			if DEGREE_SEQUENCE:
				figureName = 'plot_distribution_'+net+'_'+edgetype+'_sequence'+'.png'
			else:
				figureName = 'plot_distribution_'+net+'_'+edgetype+'.png'
			figurePath = os.path.join(FIGURE_PATH,figureName)
			print "\nPlotting the degree distribution of network ", net
			plot_degree_distribution_per_treatment(net_path, {net: networks[net]}, figurePath, DEGREE_SEQUENCE, edgetype)

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



		fraction = float(args.fraction)
		figureName = 'plot_'+'_'.join(args.networks)+'_'+edgetype+'_'+ plot_by +'_prop='+str(fraction)+'.png'
		figurePath = os.path.join(FIGURE_PATH,figureName)
		measures = MEASURES

		print "\nSimulating and plotting the robustness of networks:"
		print ", ".join(networks)
		print "and plotting "+str(fraction)+" fraction of nodes "+plot_by+" and with following measures:"
		print ", ".join([m.__name__ for m in measures])
		print "\n"
		plot_multiple(net_path, networks, measures, plot_by, fraction, figurePath, add_random, add_scalefree)
	
if __name__ == "__main__":
	main(*sys.argv[1:])




