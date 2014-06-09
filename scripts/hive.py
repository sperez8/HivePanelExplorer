'''
created  03/06/2014

by sperez

Hive class stores the nodes, edges and how they will be displayed
including node position, edge coloring, number of axes etc...
'''

#library imports
import numpy as np
from math import pi
import networkx as nx

class Hive():
    '''contains node and edge, coloring, position, etc...'''
    
    def __init__(self, numAxes = 3, doubleAxes = False, 
                 axisAssignRule = 'degree', axisPositRule = 'closeness', 
                 debug = True):
        '''Initializing defining parameters of the hive''' 
        self.numAxes = numAxes
        self.doubleAxes = doubleAxes
        self.axisAssignRule = axisAssignRule
        self.axisPositRule = axisPositRule
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
            print 'Nodes are: ', self.nodes
            print 'Node names are: ', self.nodeNames
            print 'Node properties are: ', self.nodeProperties
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
            print 'Sources are: ', self.sources
            print 'Targets are: ', self.targets
            print 'Edge properties are: ', self.edgeProperties
        return None

    def make_axes(self):
        '''creates axes and angles given the number of axes desired
        and whether the axes are being doubled or not'''
        angles = []
        if self.doubleAxes:
            #create a total of 3*self.numAxes to make spacing between the doubled axes
            allAngles = [2.0*pi/float(self.numAxes*3)*i for i in range(0,self.numAxes*3)]
            #re-center the axes for symmetry when the number of axes is odd
            if self.numAxes % 2 != 0:
                shiftBy = allAngles[1]/2.0
                allAngles = [a-shiftBy for a in allAngles]
            #remove the "spacer" axes
            for a in allAngles:
                if (allAngles.index(a)+1) % 3 != 0:
                    angles.append(a)
        else:
            angles = [2.0*pi/float(self.numAxes)*i for i in range(0,self.numAxes)]

        angles = [round(a,2) for a in angles]
        if self.debug:
            print "Axes angles are", angles   
        self.angles = angles
        return None

    def make_graph(self):
        '''Makes a graph using networkx package Graph instance'''
        self.check_input()
        G = nx.Graph()
        G.add_edges_from(zip(self.sources,self.targets))
        if self.debug:
            print 'Graph nodes:', G.nodes()
            print 'Graph edges:', G.edges()
        return G

    def node_assignment(self):
        '''determines on which axis the node should be placed
            depending on the rule. Integer valued rules indicate the use of
            node properties. Rules which are string values denote network 
            properties which need to be calculated.'''
        assignmentValues = {}
        if isinstance(self.axisAssignRule, int):
            try: 
                properties = self.nodeProperties[self.axisAssignRule-1]
            except ValueError:
                print 'Please choose a node assignment rule which is either a network'
                print 'feature or one of the {0} column(s) of the node properties in the input file'.format(len(nodeProperties))
                sys.exit()
            [assignmentValues.update({n:p}) for n,p in zip(self.nodes, properties)]
        if isinstance(self.axisAssignRule, str):
            #Need to make a graph instance using networkx
            G = self.make_graph()
            assignmentValues = self.node_analysis(G, self.axisAssignRule)
        
        #get values to be used to assign nodes
        #and partition into groups of nodes
        #make as many groups as self.numAxes
        #only works for numerical variables for now but will be improved for categorical ones
        
        values = assignmentValues.values()
        values.sort()
        cutoffs = [int(len(values)/self.numAxes)*i for i in range(1,self.numAxes+1)]
        cutoffValues = [values[c] for c in cutoffs] # to prevent nodes with the same value to be in different groups
        
        nodeAssignments = {}        
        
        for n in self.nodes:
            i = 0
            while i < len(cutoffValues):
                if assignmentValues[n] <= cutoffValues[i]:
                    nodeAssignments[n]=i
                    break
                else: i+=1
        if self.debug:
            print 'node assignments to axis:', nodeAssignments
        return None
    
    def node_position(self):
        return None
    
    def make_edges(self):
        return None
    
    def node_properties(self):
        return None
    
    def edge_properties(self):
        return None

    def check_input(self):
        '''IN DEVELOPMENT
        checks if all edges are connecting nodes which exist in the self.nodes'''
        return None

    @staticmethod
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
        

    @staticmethod
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
