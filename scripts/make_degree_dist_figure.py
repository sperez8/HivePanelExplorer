''' 
created  03/06/2015

by sperez

This script builds a scale free graph 
and a graph with binomial degree distribution
of the same size.

http://networkx.github.io/documentation/latest/reference/generated/networkx.generators.social.florentine_families_graph.html#networkx.generators.social.florentine_families_graph
http://networkx.github.io/documentation/latest/reference/generated/networkx.generators.social.davis_southern_women_graph.html#networkx.generators.social.davis_southern_women_graph
'''

#library imports
import sys
import os
import matplotlib.pyplot as plt
import prettyplotlib as ppl
#import numpy as np
#from math import pi
#import hive as Hive
#from hive_utilities import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx

N = 1000 #number of nodes
seed = 2 #random seed

G = nx.scale_free_graph(N,seed=seed)

M = nx.number_of_edges(G)

H = nx.gnm_random_graph(N,M,seed=seed)

print N, M



G_degrees = sorted(nx.degree(G).values(),reverse=True)
H_degrees = sorted(nx.degree(H).values(),reverse=True)

G_k = []
G_p_k = []
for n in set(G_degrees):
	G_k.append(n)
	G_p_k.append(G_degrees.count(n)/float(N))


H_k = []
H_p_k = []
for n in set(H_degrees):
	H_k.append(n)
	H_p_k.append(H_degrees.count(n)/float(N))



fig, (axG,axH) = plt.subplots(2, sharex = True)

# Axis needs to be set before plotting the bars
axG.set_yscale('log')
axG.set_xscale('log')
axH.set_yscale('log')
axH.set_xscale('log')

ppl.bar(axG, G_k, G_p_k, color = ppl.colors.set2[0], label = "Power-law distribution network", annotate=False, grid='y')
ppl.bar(axH,  H_k, H_p_k, color = ppl.colors.set2[1], label = "Binomial degree distribtuion network", annotate=False, grid='y')

axG.set_title("Degree distribution of two networks with "+str(N)+" nodes and "+str(M)+" edges.\n")
axG.xaxis.set_label_text("degree (k)")
axG.yaxis.set_label_text("Degree frequency P(k)")
axH.xaxis.set_label_text("degree (k)")
axH.yaxis.set_label_text("Degree frequency P(k)")

ppl.legend(axG, loc='upper right', ncol=1)


fig.savefig('test_distribution.png')




# # draw graph in inset
# plt.axes([0.45,0.45,0.45,0.45])
# pos=nx.spring_layout(G)
# nx.draw_networkx_nodes(G,pos,node_size=10, node_color = 'm', alpha = 0.4)
# nx.draw_networkx_edges(G,pos,alpha=0.2)

# plt.axes([0.45,0.45,0.45,0.45])
# pos=nx.spring_layout(H)
# plt.axis('off')
# nx.draw_networkx_nodes(H,pos,node_size=10, node_color = 'm', alpha = 0.4)
# nx.draw_networkx_edges(H,pos,alpha=0.2)