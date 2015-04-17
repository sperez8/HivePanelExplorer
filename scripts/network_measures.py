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
import copy
#import scipy.stats

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx
from make_network import *

DECIMALS = 3 #for rounding measures
FACTOR = 2


def number_of_nodes(G):
	return G.number_of_nodes()

def number_of_edges(G):
	return G.number_of_edges()

def number_of_nodes_of_largest_connected_component(G):
    return nx.connected_component_subgraphs(G)[0].number_of_nodes()

def number_of_edges_of_largest_connected_component(G):
    return nx.connected_component_subgraphs(G)[0].number_of_edges()

def number_of_components(G):
    return nx.number_connected_components(G)

def size_of_components(G):
    cc = sorted(nx.connected_components(G), key = len, reverse=True)
    sizes = [str(len(c)) for c in cc]
    return ','.join(sizes)

def in_largest_connected_component(G):
    CC = nx.connected_component_subgraphs(G)[0].nodes()
    members = {n:(1 if n in CC else 0) for n in G.nodes()}
    return members

def node_degrees(G):
    return G.degree()

def average_degree(G):
    return round(np.mean(G.degree().values()), DECIMALS)

def connectance(G):
    return round(nx.density(G), DECIMALS)

def global_clustering_coefficient(G):
    return round(nx.average_clustering(G), DECIMALS)

def fraction_of_possible_triangles(G):
    return round(nx.transitivity(G), DECIMALS)

def size_of_largest_clique(G):
    return nx.graph_clique_number(G)

def degree_assortativity(G):
    return round(nx.degree_assortativity_coefficient(G), DECIMALS)

def diameter_of_largest_connected_component(G):
    H = nx.connected_component_subgraphs(G)[0]
    return nx.diameter(H)

def average_path_on_largest_connected_component(G):
    H = nx.connected_component_subgraphs(G)[0]
    return round(nx.average_shortest_path_length(H), DECIMALS)

def correlation_of_degree_and_betweenness_centrality(G):
    bc = nx.betweenness_centrality(G)
    d = nx.degree(G)
    bcn = []
    dn = []
    for n in G.nodes():
        bcn.append(bc[n])
        dn.append(d[n])

    r = scipy.stats.spearmanr(dn, bcn)
    return str((round(r[0],DECIMALS),round(r[1],5)))


### Ecological measures


def remove_headers(S):
    return S[1:-1,1:-1].astype(np.float)

def normalize(S):
    col_sums = S.sum(axis=0)
    nS = S / col_sums[np.newaxis,:]
    return nS


def richness(S):
    S = remove_headers(S)
    return S.shape[0]

def shannon_diversity(S):
    D = 0
    S = normalize(remove_headers(S))
    D = -sum(np.mean(row) * np.log(np.mean(row)) for row in S)    
    return D


########## Measures using an OTU table and features

def correlation_of_edge_depth(G,featureTable):
    feature = 'Soil Horizon avg'
    return compute_feature_correlation(G,feature,featureTable)


def correlation_of_degree_and_depth(G,featureTable):
    feature = 'Soil Horizon avg'
    return compute_feature_degree_correlation(G,feature,featureTable)
    
def compute_feature_degree_correlation(G,feature,featureTable):
    col = np.where(featureTable[0,:]==feature)[0][0]
    d = nx.degree(G)
    H = nx.Graph()
    degrees = []
    featureValues = []
    for n in d.keys():
        row = findRow(n,featureTable)
        if row:
            degrees.append(d[n])
            featureValues.append(featureTable[row][col])
        else: continue
    r = scipy.stats.spearmanr(degrees, featureValues)
    return str((round(r[0],DECIMALS),round(r[1],5)))


def compute_feature_correlation(G,feature,featureTable):
    col = np.where(featureTable[0,:]==feature)[0][0]
    iF = []
    jF = []
    for (i,j) in G.edges():
        irow = findRow(i,featureTable)
        jrow = findRow(j,featureTable)
        if irow and jrow:
            iF.append(featureTable[irow][col])
            jF.append(featureTable[jrow][col])
        else:
            continue
    r = scipy.stats.spearmanr(iF,jF)
    return str((round(r[0],DECIMALS),round(r[1],5)))



def findRow(otu,table):
    if 'Otu' in otu:
        row = np.where(table==otu.replace('OTU-',''))[0][0]
    else:
        row = None
    return row





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

def node_modularity(G,factor=FACTOR):
    '''gets modules using FAG-EC algorithm and returns a dictionary
    where keys are nodes and value is hte module it belongs to where
    0 = no module
    1 = largest module
    i = ith largets module
    '''
    modularity = {}
    modules = get_modules(G)
    modules.sort(key=lambda m: len(m),reverse=True) #order by size
    print "Found {0} modules with sizes: {1}".format(len(modules),','.join([str(len(m)) for m in modules]))
    for n in G.nodes():
        m = findSubgraph(modules,n)
        if m != None:
            m+=1  #start module index at 1
        else:
            m = 0 #for not in a module
        modularity[n]=m
    return modularity

def findSubgraph(subgraphs,n):
    for i,m in enumerate(subgraphs):
        if n in m:
            return i

def testModule(G,factor,subgraphNodes):
    isModule = False

    kin = 0
    kout = 0
    for s,t in G.edges():
        if s in subgraphNodes and t in subgraphNodes:
            kin+=1
        elif s in subgraphNodes or t in subgraphNodes:
            kout+=1

    #print 'degrees', kin,kout, G.degree(subgraphNodes)
    if kin>kout*factor:
        isModule = True
        #print "MODULE"

    return isModule

def edge_clustering(G):
    clusteringcoeffs = {}
    for s,t in G.edges():
        c = 0
        ns = set(nx.all_neighbors(G,s))
        nt = set(nx.all_neighbors(G,t))
        commons = ns.intersection(nt)
        ds = G.degree(s)
        dt = G.degree(t)
        c = (len(commons)+1)/float(min([ds,dt]))
        clusteringcoeffs[(s,t)] = c
    return clusteringcoeffs

def get_modules(G,factor=FACTOR):
    '''modularity algorithm from FAG-EC'''
    #initialize nodes as singleton clusters
    subgraphs = [[n] for n in G.nodes()]
    nonmergeable = []
    #get edge betweenness values and sort them by that value
    weights = edge_clustering(G)
    Sq = [(e,cc) for e,cc in weights.iteritems()]
    Sq.sort(key=lambda tup: tup[1],reverse=True)

    while len(Sq)>0:
        edge,cc = Sq.pop(0) #get mergeable edge with highest clustering coefficient
        s,t = edge[0],edge[1]
        mods = findSubgraph(subgraphs,s) #get index of the subgraph where node belongs
        modt = findSubgraph(subgraphs,t)

        if mods==modt: #already in the same subgraph
            continue
        #check if mergeable, ie. both not in nonmergeable modules
        elif findSubgraph(nonmergeable,s)==None and findSubgraph(nonmergeable,t)==None:
            ms = testModule(G,factor,subgraphs[mods])
            mt = testModule(G,factor,subgraphs[modt])
            if ms and mt: #if both modules, then non mergeable
                newmod = subgraphs[mods]
                nonmergeable.append(newmod)
                newmod = subgraphs[modt]
                nonmergeable.append(newmod)
            else: #merge
                newsubg = subgraphs.pop(mods)
                modt = findSubgraph(subgraphs,t) #need to do it again after poping
                s2 = subgraphs.pop(modt)
                newsubg.extend(s2)
                subgraphs.append(newsubg) #merging

        #THE FOLLOWING lines are consistent with the original algorithm,
        # which outputs all subgraphs, some modules some not.
        # elif findSubgraph(nonmergeable,s)==None:
        #     newmod = subgraphs[mods]
        #     nonmergeable.append(newmod)
        #     #set as non mergeable
        # elif findSubgraph(nonmergeable,t)==None:
        #     #set as non mergeable
        #     newmod = subgraphs[modt]
        #     nonmergeable.append(newmod)
        else: #both are modules, or one is a module so we continue
            continue

    return nonmergeable #return modules only, ie. not all nodes are returned.

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
    #G = main(*sys.argv[1:])
    #measures = measure_whole(G)
    #measures.update(measure_component(G))

    #to test modularity
    # G=nx.karate_club_graph()
    # m = node_modularity(G)
    # for i,n in m.iteritems():
    #     print i,n
    '''Use  commands like:
    nx.attribute_mixing_matrix(G, 'Gender')
    and
    nx.attribute_assortativity_coefficient(G, 'Gender')
    to find the assortativity between node attributes'''


