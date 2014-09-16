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
    
    #make sure only represented nodes are in the graph
    badNodes = []
    for n in G.nodes(data=False):
        if n in nodes:
            pass
        elif (n +".1") in nodes:
            pass
        else:
            badNodes.append(n)
    
    print badNodes
    
    G.remove_nodes_from(badNodes)
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
            
def filter_nodes(nodeFile, edgeFile):
    '''check that all nodes are found in the sources and targets and vice versa.
    Remove nodes such that all nodes are connected to another node.
    Remove edges whose nodes aren't found in the nodes file'''

    nodeData = np.genfromtxt(nodeFile, delimiter=',', dtype='str', filling_values = 'None')

    edgeData = np.genfromtxt(edgeFile, delimiter=',', dtype='str', filling_values = 'None')
    
    #filter all nodes which aren't in an edge
    sourceTest = np.in1d(nodeData[:,0], edgeData[:,0], assume_unique = False)
    targetTest = np.in1d(nodeData[:,0], edgeData[:,1], assume_unique = False)

    newNode = nodeData[sourceTest + targetTest,:]
    
    print "Of the {0} nodes, {1} were not found in the edges and removed".format(nodeData.shape, newNode.shape)

    nodeFile = nodeFile[:-4] +  '_filtered' + nodeFile[-4:]
    
    print newNode.shape
    
    np.savetxt(nodeFile, newNode, delimiter = ',', fmt="%s %s")#*newNode.shape[1])
    
    return None
            


NODES = "/Users/sperez/Documents/Cam/For Sarah_Hives/nodes_937_938_941.csv"
EDGES = "/Users/sperez/Documents/Cam/For Sarah_Hives/edges_937_938_941.csv"
filter_nodes(NODES,EDGES)
    
    
