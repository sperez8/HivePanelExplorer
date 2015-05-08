
#library imports
import sys
import os
import argparse
import numpy as np
from tabulate import tabulate

from network_simulation import get_network_fullnames

BEGINNING = '''\\begin{table}
\caption[]{}
\label{tab:label}
\centering'''

END = '''\end{table}'''

def sample_sequence(net_path, networkNames, inputFolder, inputFileEnd):
	'''makes an OTU table with avg depth and othe features per OTU'''

	networks,treatments = get_network_fullnames(networkNames)

	otuTable = {}
	for n in networks:
		otuTable[n] = np.loadtxt(os.path.join(inputFolder,n.replace('BAC_','')+inputFileEnd), dtype='S1000')

	header = ['Sample ID','Number of sequences']
	headerStart = len(header)
	samples = []

	for location,treatments in networkNames.iteritems():
		for t in treatments:
			abundances = otuTable[location+'_'+t]
			sampleNames = abundances[0,1:-1]
			sampleCounts = abundances[1:-1,1:-1].astype(np.int).sum(axis=0)
			samplesAdd = np.concatenate((sampleNames[np.newaxis],sampleCounts[np.newaxis]),axis=0)
			if samples == []:
				samples = samplesAdd
			else:
				samples = np.concatenate((samples,samplesAdd),axis=1)
			print location, t
	print samples.shape

	# fileName = "samples_sequences.tx"
	# tableFile = os.path.join(path,fileName)
	# print "Saving table: ",tableFile

	# np.savetxt(tableFile, featureTable, delimiter="\t", fmt='%s')
	return None


def convert(fileName, header=False, rows=False):
	table = np.loadtxt(fileName, delimiter='\t', dtype='S1000')
	print table
	if header:
		headerNames = list(table[0,:])
		print headerNames
		table = table[1:,:]
		print table
	tableText = tabulate(table, headers=headerNames, tablefmt="latex")
	finalText = collect_pieces(tableText)
	f = open("C:\Users\Sarah\Desktop\LTSPnetworks\dump.txt",'w')
	f.write(finalText)
	return None

def collect_pieces(table):
	text = BEGINNING
	text += table
	text += END
	return text