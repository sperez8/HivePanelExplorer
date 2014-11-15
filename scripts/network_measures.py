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
import hive as hive

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx


def make_graph_from_graphml(graphmlFile):
    #parse graphml file
    G = nx.read_graphml(graphmlFile)
    return G

def make_graph_from_2_files(nodeFile, edgeFile):
    '''make a networkx graph from a csv or tsv using methods from the hive class'''
    hive = hive.Hive()
    hive.get_nodes(nodeFile)
    hive.get_edges(edgeFile)
    
    sources, targets, nodes = hive.sources, hive.targets, hive.nodes
    G = make_graph(sources, targets, nodes)
    
    return G

def measure_all(G):
    '''measure all interesting global network measures'''
    measure = {}
    
    return measures

def convert_graphml(graphmlFile):
    G = make_graph_from_graphml(graphmlFile)
    sources, targets, edgeProperties = zip(*G.edges(data=True))
    fileName = graphmlFile.split('.graphml')[0]
    nodeFile = fileName+'_nodes.csv'
    edgeFile = fileName+'_edges.csv'
    nf = open(nodeFile,'w')
    keys = []
    for node, nodeProperties in G.nodes(data=True):
        print nodeProperties.keys()
        new_keys = nodeProperties.keys()
        if new_keys != keys:
            keys.extend(new_keys)
    
    keys = set(keys)
    print keys
    
    #write header
    nf.write('Node'+','.join(keys))
    
    for node, nodeProperties in G.nodes(data=True):
        row = []
        row.append(node)
        for k in keys:
            if k in nodeProperties.keys():
                row.append(str(nodeProperties[k]))
            else:
                row.append('None')
        print row
        nf.write('\n' + ','.join(row))
    
    nf.close()
    
    ef = open(edgeFile,'w')
    keys = []
    for source,target, edgeProperties in G.edges(data=True):
        print edgeProperties.keys()
        new_keys = edgeProperties.keys()
        if new_keys != keys:
            keys.extend(new_keys)
    
    keys = set(keys)
    print keys
    
    ef.write('source' + ',' + 'target' + ','.join(keys))
    for source, target, edgeProperties in G.edges(data=True):
        row = []
        row.append(source)
        row.append(target)
        for k in keys:
            if k in edgeProperties.keys():
                row.append(str(edgeProperties[k]))
            else:
                row.append('None')
        print row
        ef.write('\n' + ','.join(row))
    
    print "writing nodefile", nodeFile
    print "writing edgefile", edgeFile
    return None    

file = "C:\Users\Sarah\Desktop\c.elegans.herm_pharynx_1.graphml"
convert_graphml(file)





