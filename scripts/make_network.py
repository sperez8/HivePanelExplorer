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
import hive as Hive
from hive_utilities import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import networkx as nx


def import_graphml(graphmlFile):
    #parse graphml file
    G = nx.read_graphml(graphmlFile)
    return G

def import_graph(nodeFile, edgeFile):
    '''make a networkx graph from a csv or tsv using methods from the hive class'''
    hive = Hive.Hive(debug=False)
    hive.get_nodes(nodeFile)
    hive.get_edges(edgeFile)
    
    sources, targets, nodes, nodeProperties, edgeProperties = hive.sources, hive.targets, hive.nodes, hive.nodeProperties, hive.edgeProperties
    G = make_graph(sources, targets, nodes)
    for i,n in enumerate(nodes):
        for p,v in nodeProperties.iteritems():
            G.node[n][p] = v[i]

    for i,e in enumerate(zip(sources, targets)):
        for p,v in edgeProperties.iteritems():
            G[e[0]][e[1]][p] = v[i]


    return G

def measure_all(G):
    '''measure all interesting global network measures'''
    measure = {}
    
    return measures

def convert_graphml(graphmlFile):
    G = make_graphml(graphmlFile)
    fileName = graphmlFile.split('.graphml')[0]
    convert_graph(G,fileName)

def convert_graph(G,fileName):
    sources, targets, edgeProperties = zip(*G.edges(data=True))
    nodeFile = fileName+'_nodes.csv'
    edgeFile = fileName+'_edges.csv'
    nf = open(nodeFile,'w')
    keys = []
    for node, nodeProperties in G.nodes(data=True):
        new_keys = nodeProperties.keys()
        if new_keys != keys:
            keys.extend(new_keys)
    
    keys = set(keys)
    
    #write header
    if keys:
        nf.write('Node'+','+','.join(keys))
    else:
        nf.write('Node')        
    
    for node, nodeProperties in G.nodes(data=True):
        row = []
        row.append(node)
        for k in keys:
            if k in nodeProperties.keys():
                row.append(str(nodeProperties[k]).replace(',', ';'))
            else:
                row.append('None')
        nf.write('\n' + ','.join([str(r) for r in row]))
    
    nf.close()
    
    ef = open(edgeFile,'w')
    keys = []
    for source,target, edgeProperties in G.edges(data=True):
        new_keys = edgeProperties.keys()
        if new_keys != keys:
            keys.extend(new_keys)
    
    keys = set(keys)
    
    if keys:
        ef.write('source' + ',' + 'target' + ',' +','.join(keys))
    else: 
        ef.write('source' + ',' + 'target')

    for source, target, edgeProperties in G.edges(data=True):
        row = []
        row.append(source)
        row.append(target)
        for k in keys:
            if k in edgeProperties.keys():
                row.append(str(edgeProperties[k]))
            else:
                row.append('None')
        ef.write('\n' + ','.join([str(r) for r in row]))
    
    print "writing nodefile", nodeFile
    print "writing edgefile", edgeFile
    return None





#file = "C:\Users\Sarah\Dropbox\\0-HalLab\Hive panel examples\C.elegans\c.elegans.herm_pharynx_1.graphml"
#convert_graphml(file)





