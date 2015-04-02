'''
created  10/06/2014

by sperez

Contains functions used by hive class to measure things like network properties
'''

#library imports
import sys
import os
import argparse
import numpy as np
from math import pi
import hive as hive

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx
from make_network import *


def number_of_nodes(G):
	return G.number_of_nodes()

def number_of_edges(G):
	return G.number_of_edges()

def average_degree(G):
    return np.mean(G.degree().values())

def connectance(G):
    return nx.density(G)

def global_clustering_coefficient(G):
    return nx.average_clustering(G)

def fraction_of_possible_triangles(G):
    return nx.transitivity(G)

def size_of_largest_clique(G):
    return nx.graph_clique_number(G)

def degree_assortativity(G):
    return nx.degree_assortativity_coefficient(G)

def diameter_of_largest_connected_component(G):
    H = nx.connected_component_subgraphs(G)[0]
    return nx.diameter(H)

def average_path_on_largest_connected_component(G):
    H = nx.connected_component_subgraphs(G)[0]
    return nx.average_shortest_path_length(H)




# def assortativity_of_degree_and_betweenness_centrality(G):
#     bc = nx.betweenness_centrality(G)
#     H = nx.Graph()
#     for n in G.nodes(): 
#         H.add_nodes_from(n, att = bc[n])
#         print n,bc[n]
#     H.add_edges_from(G.edges())
#     return nx.numeric_assortativity_coefficient(H,'att')



NODES = os.path.join(_root_dir, 'tests', 'test_nodes_friends.txt')
EDGES = os.path.join(_root_dir, 'tests', 'test_edges_friends.txt')


def main(*argv):
    '''handles user input and runs plsa'''
    parser = argparse.ArgumentParser(description='This scripts produces an interactive hive panel.')
    parser.add_argument('-n', help='The node file', default = NODES)
    parser.add_argument('-e', help='The edge file', default = EDGES)
    args = parser.parse_args()
    
    if (args.n == '' and args.e != '') or (args.n != '' and args.e == ''):
        print "\n***You must specify both a node and an edge file if specifying either.***\n"
        parser.print_help()
        sys.exit()
        
    nodeFile = args.n
    edgeFile = args.e

    G = import_graph(nodeFile,edgeFile)

    print "\nMade the networkx graph."

    return G

def measure_whole(G):
    '''measure all interesting global network measures'''
    measures = {}

    measures['components'] = [len(x) for x in nx.connected_components(G)]
    measures['d'] =  list(G.degree().values())
    measures['bc'] =  list(nx.betweenness_centrality(G).values())
    measures['cc'] =  list(nx.closeness_centrality(G).values())
    measures['clustering'] =  list(nx.clustering(G).values())
    

    return measures

def measure_component(G):
    '''measure all interesting global network measures'''
    measuresC = {}

    components = nx.connected_component_subgraphs(G)
    for i,c in enumerate(components):
        measuresC[i] = {}
        measuresC[i]['d'] = list(c.degree().values())
        measuresC[i]['bc'] =  list(nx.betweenness_centrality(c).values())
        measuresC[i]['cc'] =  list(nx.closeness_centrality(c).values())
        measuresC[i]['clustering'] =  list(nx.clustering(c).values())
    return measuresC

if __name__ == "__main__":
    '''testing purposes'''
    G = main(*sys.argv[1:])
    measures = measure_whole(G)
    measures.update(measure_component(G))

    '''Use  commands like:
    nx.attribute_mixing_matrix(G, 'Gender')
    and
    nx.attribute_assortativity_coefficient(G, 'Gender')
    to find the assortativity between node attributes'''


