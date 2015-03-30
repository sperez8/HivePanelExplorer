'''
Created on 27/03/2015

author: sperez8
'''

import sys, os
import argparse
import numpy as np
from network_simulation import *

#What to plot
PATH = '/Users/sperez/Dropbox/1-Aria/LTSP_networks'
FIGURE_PATH = PATH

TREATMENTS = ['OM3','OM2','OM1','OM0']
MEASURES = [nx.betweenness_centrality, 
			nx.degree_centrality,
			nx.closeness_centrality, 
			nx.eigenvector_centrality]
NETWORKS = ['SBS']#,'IDF']

## to change names of network files from R_B_***_BAC_SBS* to BAC_SBS*
#run the following command in network folder:
# ls *_BAC*|sed 's/.*BAC\(.*\)/mv & BAC\1/' | sh

#for testing and spead
#NETWORKS = ['trial1'] ##trial networks to test faster
#TREATMENTS = ['OM3']

PROP_TO_REMOVE = 1 #only removing this percent of nodes


def main(*argv):
	'''handles user input and runs plsa'''
	parser = argparse.ArgumentParser(description='This scripts produces robustness plots for networks')
	parser.add_argument('-path', help='Path where the networks are', default = PATH)
	parser.add_argument('-treatment', help='Makes a plot for each treatment', action = 'store_true')
	parser.add_argument('-measure', help='Makes a plot for each centrality measure', action = 'store_true')
	parser.add_argument('-networks', nargs='*', help='Which network to use: SBS, IDF, etc.', default = NETWORKS)
	parser.add_argument('-fraction', help='Fraction of nodes to remove', default = PROP_TO_REMOVE)
	args = parser.parse_args()
	
	if not args.treatment and not args.measure:
		print "\n***You must specify to plot by treatment or by measure.***\n"
		parser.print_help()
		sys.exit()
		
	net_path = args.path
	if args.treatment:
		plot_by = 'by treatment'
	elif args.measure:
		plot_by = 'by measure'
	networks = {('BAC_'+n if 'BAC_' not in n else n):TREATMENTS for n in args.networks}
	fraction = float(args.fraction)
	figure_name = 'plot_'+'_'.join(networks)+'_' + plot_by +'.png'
	measures = MEASURES

	print "\nSimulating and plotting the robustness of networks:"
	print ", ".join(networks)
	print "and plotting "+str(fraction)+" fraction of nodes "+plot_by+" and with following measures:"
	print ", ".join([m.__name__ for m in measures])
	print "\n"

	plot_multiple(net_path, networks, measures, plot_by, fraction, figure_name)
	#plot_individual(path, networks, fraction)
	
if __name__ == "__main__":
	main(*sys.argv[1:])




