'''
Created on 27/03/2015

author: sperez8
'''

import sys, os
import argparse
import numpy as np
from network_simulation import *

#What to plot
PATH = '/Users/sperez/Desktop/LTSPnetworks/by_treatment'
FOLDER = 'input'
INPUT_FILE_END = '_BAC-filtered-lineages_final.txt'
FIGURE_PATH = os.path.join(PATH,'plots')

TREATMENTS = ['OM3','OM2','OM1','OM0']

def main(*argv):
	'''handles user input and runs plsa'''
	parser = argparse.ArgumentParser(description='This scripts produces robustness plots for networks')
	parser.add_argument('-path', help='Path where the networks are', default = PATH)
	parser.add_argument('-folder', help='Folder in path where the networks are', default = FOLDER)
	parser.add_argument('-tables', nargs='*', help='Which input tables to use: SBS, IDF, etc.')
	args = parser.parse_args()

	net_path = os.path.join(args.path,args.folder)
	networks = {('BAC_'+n if 'BAC_' not in n else n):TREATMENTS for n in args.networks}

	print "\nCalculating ecological metrics of sample collection for the following networks:"
	print ", ".join(networks), '\n'
	filePath = os.path.join(FIGURE_PATH,'table_of_sample_measures_'+'_'.join(args.networks)+'.csv')
	make_table(net_path,networks,filePath,edgetype)
	
if __name__ == "__main__":
	main(*sys.argv[1:])




