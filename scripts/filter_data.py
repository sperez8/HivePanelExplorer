'''
created  16/09/2014

by sperez

filter nodes not in edge file and vice versa to clean data
'''

import numpy as np
import sys
import os
import argparse
from graph_utilities import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)

NODES = _root_dir + "/tests/test_nodes_friends.txt"
EDGES = _root_dir + "/tests/test_edges_friends.txt"

def get_nodes(nodeFile):
    delimiter = get_delimiter(nodeFile)
    nodeData = np.genfromtxt(nodeFile, delimiter=delimiter, dtype='str', filling_values = 'None')
    nodeHeader = nodeData[0,:]
    return  nodeData, nodeHeader

def get_edges(edgeFile):
    delimiter = get_delimiter(edgeFile)
    edgeData = np.genfromtxt(edgeFile, delimiter=delimiter, dtype='str', filling_values = 'None')
    print edgeData
    edgeHeader = edgeData[0,:]
    return  edgeData, edgeHeader

def filter_nodes(nodeData, edgeData):
    '''check that all nodes are found in the sources and targets and vice versa.
    Remove nodes such that all nodes are connected to another node.
    Remove edges whose nodes aren't found in the nodes file'''
    
    #find all nodes which aren't in an edge, as a target or a source
    sourceTest = np.in1d(nodeData[:,0], edgeData[:,0], assume_unique = False)
    targetTest = np.in1d(nodeData[:,0], edgeData[:,1], assume_unique = False)
    
    #filter them out
    newNode = nodeData[np.logical_or(sourceTest,targetTest),:]
    
    return newNode
            
def filter_edges(nodeData, edgeData):
    '''check that all nodes are found in the sources and targets and vice versa.
    Remove nodes such that all nodes are connected to another node.
    Remove edges whose nodes aren't found in the nodes file'''
    
    #find all sources and targets which aren't in the node file
    sourceTest = np.in1d(edgeData[:,0], nodeData[:,0], assume_unique = False)
    targetTest = np.in1d(edgeData[:,1], nodeData[:,0], assume_unique = False)
    
    #filter them out
    newEdge = edgeData[np.logical_and(sourceTest, targetTest),:]

    return newEdge

def save_filtered_nodes(old, newNode, nodeHeader, nodeFile):
    new = newNode.shape[0]
    newNode = np.concatenate((nodeHeader[np.newaxis,:], newNode), axis = 0)
    nodeFile = nodeFile[:-4] +  '_filtered' + nodeFile[-4:]
    np.savetxt(nodeFile, newNode, delimiter = ',', fmt="%s"+",%s"*(newNode.shape[1]-1))
    print "Of the {0} nodes, {1} were not found in the edges and removed".format(old, old-new)

def save_filtered_edges(old, newEdge, edgeHeader, edgeFile):
    new = newEdge.shape[0]
    newEdge = np.concatenate((edgeHeader[np.newaxis,:], newEdge), axis = 0)
    edgeFile = edgeFile[:-4] +  '_filtered' + edgeFile[-4:]
    np.savetxt(edgeFile, newEdge, delimiter = ',', fmt="%s"+",%s"*(newEdge.shape[1]-1))
    print "Of the {0} edges, {1} had a source or target not found in the node file and were removed".format(old, old-new)
    
def parse_args(*argv):
    parser = argparse.ArgumentParser(description='This scripts filters nodes and edges to clean data')
    parser.add_argument('-n', help='The node file', default = '')
    parser.add_argument('-e', help='The edge file', default = '')
    args = parser.parse_args()
    
    if (args.n == '' and args.e != '') or (args.n != '' and args.e == ''):
        print "\n***You must specify both a node and an edge file if specifying either.***\n"
        parser.print_help()
        sys.exit()

    nodeFile = args.n
    edgeFile = args.e
    
    if nodeFile and edgeFile:
        print "Using the following node file:\n{0}\nand edge file\n{1}".format(nodeFile, edgeFile)
        return nodeFile, edgeFile
    else:
        print "Using the test node file:\n{0}\nand test edge file\n{1}".format(NODES,EDGES)
        return NODES, EDGES
    
    
    
if __name__ == "__main__":
    nodeFile, edgeFile = parse_args(*sys.argv[1:])
    
    nodes, nodeHeader = get_nodes(nodeFile)
    edges, edgeHeader = get_edges(edgeFile)
    
    old_nodes = nodes.shape[0]-1
    old_edges = edges.shape[0]-1
    
    oldNodes = nodes
    oldEdges = edges
    
    unfiltered_nodes, unfiltered_edges = True, True
    i = 0
    #should only run the while loop 3 times
    while unfiltered_nodes or unfiltered_edges:
        newNodes = filter_nodes(oldNodes, oldEdges)
        newEdges = filter_edges(oldNodes, oldEdges)
        unfiltered_nodes = (newNodes.shape != oldNodes.shape)
        unfiltered_edges = (newEdges.shape != oldEdges.shape)
        oldNodes = np.copy(newNodes)
        oldEdges = np.copy(newEdges)
        i+=1
        
    print "It took {0} iterations to filter nodes and edges".format(i)
    if i > 3: print "Filtering loop ran more than 3 times. Please investigate."
    
    save_filtered_nodes(old_nodes, newNodes, nodeHeader, nodeFile)
    save_filtered_edges(old_edges, newEdges, edgeHeader, edgeFile)
    
    
    
    