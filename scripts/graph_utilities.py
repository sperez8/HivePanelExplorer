'''
created  10/06/2014

by sperez

Contains functions used by hive class to measure things like network properties
'''

#library imports
import sys
import os
import numpy as np
from math import pi

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx

def edge_analysis(G, rule):
    if rule == 'average connecting degree':
        #returns the average degree of the nodes connected in an edge e
        return [ {}.update( {e:np.mean( [G.degree(n) for n in e] )} ) for e in G.edges() ]
    else:
        print "Edge assignment rule not recognized."
        sys.exit()

def node_analysis(G, rule):
    if rule == 'degree':
        return nx.degree(G)
    elif rule == 'clustering':
        return nx.clustering(G)
    elif rule == 'closeness' or rule == 'centrality':
        return nx.closeness_centrality(G)
    elif rule == 'betweeness':
        return nx.betweenness_centrality(G)
    elif rule == 'average neighbor degree':
        return nx.average_neighbor_degree(G)
    else:
        print "Node assignment rule {0} not recognized.".format(rule)
        sys.exit()

def make_graph(sources, targets, nodes):
    '''Makes a graph using the networkx package Graph instance'''
    G = nx.Graph()
    G.add_edges_from(zipper(sources,targets))
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

def find_categories(data):
    '''checks if a list of data is categorical 
        and if so finds to number of categories'''
    categories = []
    if isinstance(convert_type(data)[0],str):
        categories = set(data)
        if len(categories) < len(data):
            categories = list(categories)
            categories.sort()
            return categories #sort by alphabetical order
        else:
            print 'This data is may be categorical but you have many categories!'
            return None
    else:
        return None
    return categories

def zipper(*args):
    '''a revamped version of zip() method that checks that lists
    to be zipped are the same length'''
    for i,item in enumerate(args):
        if len(item) != len(args[0]):
            raise ValueError('The lists to be zipped aren\'t the same length.')
    
    return zip(*args)
    
    
