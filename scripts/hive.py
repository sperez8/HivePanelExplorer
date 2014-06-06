'''
created  03/06/2014

by sperez

Hive class stores the nodes, edges and how they will be displayed
including node position, edge coloring, number of axes etc...
'''

#library imports
import numpy as np



class Hive():
    '''contains node and edge, coloring, position, etc...'''
    
    def __init__(self, debug = True):
        self.debug = debug
        return None
    
    def get_nodes(self,inputFile, delimiter = ','):
        '''gets nodes and their properties from csv file'''
        data = np.genfromtxt(inputFile, delimiter=delimiter, skiprows = 1, dtype='str')
        #get all the node data
        nodes = data[:,0]        
        nodeNames = data[:,1]
        nodeProperties = []
        for column in data[:,2:].T:
            nodeProperties.append(list(column))
        if len(nodeProperties) == 1: 
            nodeProperties=nodeProperties[0] #avoid having a list of one list when there is only 1 property 
        
        #transform it into the right data type
        self.nodes = self.convert_type(nodes)
        self.nodeNames = self.convert_type(nodeNames)
        self.nodeProperties = [self.convert_type(p) for p in nodeProperties]
        
        if self.debug:
            print self.nodes
            print self.nodeNames
            print self.nodeProperties
        return None

    def get_edges(self,inputFile, delimiter = ','):
        '''gets edges and their properties from csv file'''
        data = np.genfromtxt(inputFile, delimiter=delimiter, skiprows = 1, dtype='str')
        #get all the edge data
        sources = data[:,0]        
        targets = data[:,1]
        edgeProperties = []
        for column in data[:,2:].T:
            edgeProperties.append(list(column))
        
        if len(edgeProperties) == 1: 
            edgeProperties=edgeProperties[0] #avoid having a list of one list when there is only 1 property 
            
        #transform it into the right data type
        self.sources = self.convert_type(sources)
        self.targets = self.convert_type(targets)
        self.edgeProperties = [self.convert_type(p) for p in edgeProperties]
        
        if self.debug:
            print self.sources
            print self.targets
            print self.edgeProperties
        return None

    def check_input(self):
        '''IN DEVELOPMENT
        checks if all edges are connecting nodes which exist in the self.nodes'''
        
        return None

    @staticmethod
    def convert_type(data):
        try:
            convertedData = [int(d) for d in data]
            return convertedData
        except ValueError:
            try:
                convertedData = [float(d) for d in data]
                return convertedData
            except ValueError:
                return data
    