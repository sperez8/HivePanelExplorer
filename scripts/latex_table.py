'''
Created on 27/03/2015

author: sperez8
'''

import sys, os
import argparse
import numpy as np
from table_methods import *

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
FEATURE_FILE = 'feature_and_node_measures_table'
FEATURES = ['SoilHorizon']
BC_FEATURES = ['Betweenness centrality','SoilHorizon avg','SoilHorizon std','Abundance']

PERCENT_BC_NODES = 0.1

FOLDER_NEW_NETWORKS = os.path.join(PATH,'panels','data')

TAX_LEVEL = 'phylum'

#TREATMENTS = ['OM3'] #use when testing
TREATMENTS = ['OM0','OM1','OM2','OM3']

PROP_TO_REMOVE = 1 #only removing this percent of nodes
MAX_Y_AXIS = None
DEGREE_SEQUENCE = False

def main(*argv):
	'''handles user input and runs plsa'''
	parser = argparse.ArgumentParser(description='This scripts analyzes co-occurrence networks')
	parser.add_argument('-path', help='Path where the networks are', default = PATH)
	parser.add_argument('-folder', help='Folder in path where the networks are', default = FOLDER)
	parser.add_argument('-networks', nargs='*', help='Which network to use: SBS, IDF, etc.')
	parser.add_argument('-sequence', help='Makes table of samples and sequences', action = 'store_true')
	parser.add_argument('-edgetype', help='Specify which types edges to use', default = 'both')
	args = parser.parse_args()

	#check that one of the options is true
	choices = [args.sequence]
	if sum([1 for c in choices if c])>1 or sum([1 for c in choices if c])==0:
		print "\n***You must specify one of the three options to calculate porperties of, run simulations on or plot networks.***\n"
		parser.print_help()
		sys.exit()	

	if args.edgetype not in ['both','pos','neg']:
		print "\n***You must specify what edges you want to use to build the network: both, pos or neg.***\n"
		parser.print_help()
		sys.exit()

	treatments = TREATMENTS

	edgetype = args.edgetype
	net_path = os.path.join(args.path,args.folder)
	print net_path
	if args.folder == 'by_zone':
		networks = {('BAC_'+n if 'BAC_' not in n else n):[] for n in args.networks}
	else:
		networks = {('BAC_'+n if 'BAC_' not in n else n):treatments for n in args.networks}


	###depending on option specified, choose different things
	if args.sequence:
		print "\nMaking sample sequence table"
		print ", ".join(networks), '\n'
		sample_sequence(net_path, networks, os.path.join(PATH,INPUT_FOLDER),INPUT_FILE_END)

if __name__ == "__main__":
	main(*sys.argv[1:])




