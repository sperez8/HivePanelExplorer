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
import make_network

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx

N = 1000 #number of nodes
seed = 2 #random seed

def create_graphs():
	G = nx.scale_free_graph(N,seed=seed)
	M = nx.number_of_edges(G)
	H = nx.gnm_random_graph(N,M,seed=seed)
	print N, M
	return G,H

def plot_distributions(G,H):
	G_degrees = sorted(nx.degree(G).values(),reverse=True)
	H_degrees = sorted(nx.degree(H).values(),reverse=True)
	M = nx.number_of_edges(G)

	# get degree frequencies and add attributes
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


	# Create a plot
	fig, ax = plt.subplots(1)

	# Axis needs to be set before plotting the bars
	# ax.set_yscale('log')
	# ax.set_xscale('log')

	ppl.plot(ax, G_k, G_p_k, 'o-', color = "#9e9ac8", label = "Network with power-law distribution")
	ppl.plot(ax,  H_k, H_p_k, 'o-', color = "#6baed6", label = "Network with binomial degree distribution")

	//ax.set_title("Degree distribution of networks with "+str(N)+" nodes and "+str(M)+" edges.\n")
	ax.xaxis.set_label_text("degree (k)")
	ax.yaxis.set_label_text("Degree frequency P(k)")

	ppl.legend(ax, loc='upper right', ncol=1)
	ax.set_xlim([0,20]) #Otherwise we can'st see the curves they are so close ot 0

	fig.savefig('test_distribution.pdf')


def add_properties(G,H):
	##need to add properties to nodes and edges when making hive plots.
	for n in H.nodes():
		H.node[n]['node_property'] = 'good'
	for n in G.nodes():
		G.node[n]['node_property'] = 'good'
	for e in G.edges():
		G.remove_edge(e[0], e[1])
		G.add_edge(e[0], e[1], edge_property = 'good')
	for e in H.edges():
		H[e[0]][e[1]]['edge_property'] = 'good'

	return G,H


G,H = create_graphs()
#G,H = add_properties(G,H)
plot_distributions(G,H)


#make_network.convert_graph(G,'scale_free_1000')
#make_network.convert_graph(H,'binomial_1000')
