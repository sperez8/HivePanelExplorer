'''
created  10/06/2014

by sperez

Contains functions used by hive class to measure things like network properties
'''

#library imports
import numpy as np
from math import pi
import networkx as nx

def edge_analysis(G, rule):
    if rule == 'average connecting degree':
        #returns the average degree of the nodes connected in an edge e
        return [ {}.update( {e,np.mean( [G.degree(n) for n in e] )} ) for e in G.edges() ]
    else:
        print "Node assignment rule not recognized."
        sys.exit()

def node_analysis(G, rule):
    if rule == 'degree':
        return nx.degree(G)
    elif rule == 'clustering':
        return nx.clustering(G)
    elif rule == 'closeness' or rule == 'centrality':
        return nx.closeness_centrality(G)
    elif rule == 'betweeness':
        return nx.betweeness_centrality(G)
    elif rule == 'average neighbor degree':
        return nx.average_neighbor_degree(G)
    else:
        print "Node assignment rule not recognized."
        sys.exit()

def make_graph(sources, targets):
    '''Makes a graph using the networkx package Graph instance'''
    G = nx.Graph()
    G.add_edges_from(zip(sources,targets))
    return G
        
def convert_type(data):
    def num(s):
        '''convert list of strings to corresponding int or float type'''
        try:
            return int(d)
        except ValueError:
            return float(d)
        
    try:
        convertedData = [num(d) for d in data]
        return convertedData
    except ValueError:
        return data

