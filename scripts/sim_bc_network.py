''' 
created  02/19/2015

by sperez

This script builds 1000 scale free graphs like the C elegans connectome and
measure the highest betweenness centrality.
'''

#library imports
import os
import sys
import numpy as np
#import scipy
import matplotlib.pyplot as plt
import prettyplotlib as ppl

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)


import networkx as nx
import make_network

def create_graph_samedist(w):
	G = nx.expected_degree_graph(w,seed=None, selfloops=False)
	return G

def create_graph_scalefree(N):
	I = nx.scale_free_graph(N,seed=None)
	return I

def get_highest_betweenness(J):
	values = nx.betweenness_centrality(J).values()
	values.sort()
	return values[-1]


BCs = []

graphmlFile = "/Users/sperez/Dropbox/1-Hive panels/C.elegans/c.elegans.herm_pharynx_1.graphml"
H = make_network.import_graphml(graphmlFile)

n = 1000
for i in range(n):
	
	#degrees = H.degree(H).values()
	#G = create_graph_samedist(degrees)
	
	N = H.number_of_nodes()
	G = create_graph_scalefree(N)

	bc = get_highest_betweenness(G)

	BCs.append(bc)

x = 0.103
u = np.mean(BCs)
s = np.std(BCs)
z = (x-u)/s

#p = scipy.stats.norm.sf(z) #one-sided

print n,x,u,s,z#,p
