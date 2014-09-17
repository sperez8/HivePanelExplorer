'''
created  16/09/2014

by sperez

filter nodes not in edge file and vice versa to clean data
'''

import numpy as np

def get_nodes(nodeFile):
    nodeData = np.genfromtxt(nodeFile, delimiter=',', dtype='str', filling_values = 'None')
    nodeHeader = nodeData[0,:]
    return  nodeData, nodeHeader

def get_edges(edgeFile):
    edgeData = np.genfromtxt(edgeFile, delimiter=',', dtype='str', filling_values = 'None')
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
    
    
    
if __name__ == "__main__":

    nodeFile = "/Users/sperez/Documents/Cam/For Sarah_Hives/nodes_937_938_941.csv"
    edgeFile = "/Users/sperez/Documents/Cam/For Sarah_Hives/edges_937_938_941.csv"
    
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
    
    
    
    