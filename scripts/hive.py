'''
created  03/06/2014

by sperez

Hive class stores the nodes, edges and how they will be displayed
including node position, edge coloring, number of axes etc...
'''

#library imports
import sys
import numpy as np
from math import pi
from graph_uttilities import *

#hive parameter defaults
AXIS_ASSIGN_RULE = 'degree', 
AXIS_POSIT_RULE = 'closeness',
EDGE_PALETTE = 'purple',
EDGE_STYLE_RULE = 'average connecting degree'

class Hive():
    '''contains node and edge, coloring, position, etc...'''
    
    def __init__(self, 
                 debug = True, 
                 numAxes = 3, 
                 doubleAxes = False, 
                 axisAssignRule = AXIS_ASSIGN_RULE, 
                 axisPositRule = AXIS_POSIT_RULE,
                 edgePalette = EDGE_PALETTE,
                 edgeStyleRule = EDGE_STYLE_RULE):
        '''Initializing defining parameters of the hive'''
        self.debug = debug 
        self.numAxes = numAxes
        self.doubleAxes = doubleAxes
        self.axisAssignRule = axisAssignRule
        self.axisPositRule = axisPositRule
        self.axisAssignRule = axisAssignRule 
        self.axisPositRule = axisPositRule
        self.edgePalette = edgePalette
        self.edgeStyleRule = edgeStyleRule
        return None
    
    def get_nodes(self,inputFile, delimiter = ','):
        '''gets nodes and their properties from csv file'''
        data = np.genfromtxt(inputFile, delimiter=delimiter, skiprows = 1, dtype='str')
        #get all the node data
        nodes = list(data[:,0])
        #double the number of nodes when axes are doubled
        if self.doubleAxes:
            self.nodes = [n+".1" for n in nodes]
            self.nodes.extend([n+".2" for n in nodes])
        else: 
            self.nodes = nodes
        nodeProperties = []
        for column in data[:,1:].T:
            print list(column)
            nodeProperties.append(list(column))

        #transform node names and properties into the numerical types if possible
        self.nodeProperties = [convert_type(p) for p in nodeProperties]
        
        if self.debug:
            print '    Nodes are: ', self.nodes
            print '    Node properties are: ', self.nodeProperties
        return None

    def get_edges(self,inputFile, delimiter = ','):
        '''gets edges and their properties from csv file'''
        data = np.genfromtxt(inputFile, delimiter=delimiter, skiprows = 1, dtype='str')
        #get all the edge data
        self.sources = list(data[:,0])        
        self.targets = list(data[:,1])
        edgeProperties = []
        for column in data[:,2:].T:
            edgeProperties.append(list(column))
        
        #transform it into the right data type
        self.edgeProperties = [convert_type(p) for p in edgeProperties]
        
        if self.debug:
            print '    Sources are: ', self.sources
            print '    Targets are: ', self.targets
            print '    Edge properties are: ', self.edgeProperties
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
        angles = [0.0001 if a == 0 else a for a in angles] #d3 code doesn't work with an angle of exactly zero
        if self.debug:
            print "Axes angles are", angles   
        self.angles = angles
        return None
    
    def node_assignment(self):
        '''determines on which axis the node should be placed
            depending on the rule. Integer valued rules indicate the use of
            node properties. Rules which are string values denote network 
            properties which need to be calculated. Nodes are partitioned into groups
            depending on their value related to the rule. There are as many groups
            as numAxes'''
        axisAssignment = {} 
        assignmentValues = self.get_assignment_values(self.axisAssignRule)
        values = assignmentValues.values()
        
        
        #check if styling values are numerical, otherwise treat as categorical
        #and recode into numerical variables
        categories = find_categories(values)
        if categories:
            if len(categories) != self.numAxes:
                print 'The number of node groups using the rule \'{0}\' is different than the number of axes!'
            else:
                [axisAssignment.update({n:categories.index(v)}) for n,v in assignmentValues.iteritems()] 
                [axisAssignment.update({n:i+1}) for n,i in axisAssignment.iteritems()] #want the node group to start at 1, not 0
                print '\n\n\n', axisAssignment
        else:            
            values.sort()
            cutoffs = [int(len(values)/self.numAxes)*i for i in range(1,self.numAxes+1)]
            cutoffValues = [values[c-1] for c in cutoffs] # to prevent nodes with the same value to be in different groups
                   
            for n in self.nodes:
                i = 0
                while i < len(cutoffValues):
                    if assignmentValues[n] <= cutoffValues[i]:
                        axisAssignment[n]=i+1 #want the node group to start at 1, not 0
                        break
                    else: i+=1
                
        if self.doubleAxes:
            #for the case of 3 doubled axis, the axis groups become 2,4,6 below
            [axisAssignment.update({n:i*2}) for n,i in axisAssignment.iteritems()]
            #for the node on the 'first' axis, we change its group to 1,2 or 3
            #so that nodes in group 1 are now on axis 1 or 2, group 2 in 3 or 4 and group 3 in 5 or 6.
            [axisAssignment.update({n:(i-1)}) if n[-2:] == '.1' else None for n,i in axisAssignment.iteritems()]
        
        self.axisAssignment = axisAssignment
        
        if self.debug:
            if categories:
                print '    Node Categories:', categories
            print '    Node assignments to axis:', axisAssignment
        return None
    
    def node_position(self):
        '''determines where on the axis the node should be placed
            depending on the rule. Integer valued rules indicate the use of
            node properties. Rules which are string values denote network 
            properties which need to be calculated. node positions are scaled
            equally for all axes'''
        nodePositions = {}
        assignmentValues = self.get_assignment_values(self.axisPositRule)
        
        #only works for numerical variables for now but will be improved for categorical ones
        maxValue = max(assignmentValues.values())
        
        for n,p in assignmentValues.iteritems():
            nodePositions[n] = round(float(p)/float(maxValue),3)
            
        self.nodePositions = nodePositions
        if self.debug:
            print '    Node positions on axis:', nodePositions
        return None

    def get_assignment_values(self, rule):
        assignmentValues = {}
        if isinstance(rule, int):
            #get assignment values from the column of node properties indicated by the interger "rule"
            try: 
                properties = self.nodeProperties[rule-1]
            except IndexError:
                print '\n\n            ***WARNING***'
                print '    Please choose a node assignment rule which is either a network'
                print '    feature or one of the {0} column(s) of the node properties in the input file'.format(len(self.nodeProperties))
                print '\n'
                sys.exit()
            if self.doubleAxes:
                [assignmentValues.update({n:p}) for n,p in zip(self.nodes, properties*2)]
            else:
                [assignmentValues.update({n:p}) for n,p in zip(self.nodes, properties)]
            return assignmentValues
        
        elif isinstance(rule, str):
            #Need to make a graph instance using networkx
            G = make_graph(self.sources, self.targets)
            assignmentValues = node_analysis(G, rule)
            if self.debug:
                print '    Assignment values for \'{0}\' node property: {1}'.format(rule,assignmentValues)
            if self.doubleAxes:
                newAssignmentValues = {}
                for n,v in assignmentValues.iteritems():
                    newAssignmentValues[n +'.1'] = v
                    newAssignmentValues[n +'.2'] = v
                return newAssignmentValues
            else:
                return assignmentValues
        else: 
            print "Rule could not be parsed"
            sys.exit()

    def make_edges(self):
        '''takes sources and edges and makes a list of 
        edges while assignment nodes to the correct axis in 
        the case of double axis.'''
        newSources = []
        newTargets = []
        axis = self.axisAssignment
        for s,t in zip(self.sources, self.targets):
            if self.doubleAxes:
                s1 = s + '.1'
                s2 = s + '.2'
                t1 = t + '.1'
                t2 = t + '.2'
                
                #if nodes are from same group we add edge
                #and it's symmetrical edge within the doubled Axes
                #works for non double axes as well
                if axis[s1] == axis[t1]:
                    newSources.extend([s1,t1])
                    newTargets.extend([t2,s2])
                #if nodes from different groups, we make an edge
                #between the '.1' or '.2' nodes nearest to each other
                elif axis[s1] == axis[t1] + 2:
                    newSources.append(s1)
                    newTargets.append(t2)
                elif axis[s1] + 2 == axis[t1]:
                    newSources.append(s2)
                    newTargets.append(t1)
                #the edges below loop back from the highest numbered axis to the first axis
                elif axis[s1] == 1 and axis[t2] == self.numAxes*2:
                    newSources.append(s1)
                    newTargets.append(t2)
                elif axis[t1] == 1 and axis[s2] == self.numAxes*2:
                    newSources.append(s2)
                    newTargets.append(t1)
                else:
                    pass
            else:
                #makes edges for nodes of neighboring axes,
                #doesn't include self nodes, nor nodes of same group
                #nor nodes from non-neighboring axes when numAxes >3
                if abs(axis[s]-axis[t]) == 1:
                    newSources.append(s)
                    newTargets.append(t)
                #gets edges that connect nodes on the 1st and last axes
                elif axis[s] == 1 and axis[t] == self.numAxes:
                    newSources.append(s)
                    newTargets.append(t)
                elif axis[t] == 1 and axis[t] == self.numAxes:
                    newSources.append(s)
                    newTargets.append(t)        
        self.edges = zip(newSources, newTargets)
        
        if self.debug:
            print '    The new edges are:', self.edges
            
        return None    
        
        
        
        return None
 
    def get_edge_properties(self, rule):
       values = {}
       if isinstance(rule, int):
           try: 
               properties = self.edgeProperties[rule-1]
           except IndexError:
               print '\n\n            ***WARNING***'
               print '    Please choose a edge grouping rule which is either a network'
               print '    feature or one of the {0} column(s) of the edge properties in the input file'.format(len(self.edgeProperties))
               print '\n'
               sys.exit()
           
           [values.update({e:p}) for e,p in zip(self.edges, properties)]
           return values
       
       elif isinstance(rule, str):
           #Need to make a graph instance using networkx
           G = make_graph(self.sources, self.targets)
           values = edge_analysis(G, rule)
           if self.debug:
               print '    Assignment values for \'{0}\' edge property: {1}'.format(rule,values)
           return values
       else: 
           print "The edge styling rule could not be parsed"
           sys.exit()
               
    def node_style(self, opacity = 0.9, color = 'purple', size = '7'):
        return None
    
    def edge_style(self, opacity = 0.9, color = 'purple', size = '7'):
        '''determines how the edges will look given different characteristics'''
        edgeStyling = {}
        if self.edgeStyleRule != EDGE_STYLE_RULE:
            edgeValues = self.get_edge_properties(self.edgeStyleRule)
            values = edgeValues.values()
            print values
            if self.edgePalette != EDGE_PALETTE:
                #check if styling values are numerical, otherwise treat as categorical
                categories = find_categories(values)
                if categories:
                    [edgeStyling.update({e:categories.index(edgeValues[e])}) for e in self.edges ]
                else:
                    values.sort()
                    cutoffs = [int(len(values)/len(self.edgePalette))*i for i in range(1,len(self.edgePalette)+1)]
                    cutoffValues = [values[c-1] for c in cutoffs] # to prevent nodes with the same value to be in different groups
                           
                    for e in self.edges:
                        i = 0
                        while i < len(cutoffValues):
                            if edgeValues[e] <= cutoffValues[i]:
                                edgeStyling[e]=i
                                break
                            else: i+=1
            
            else:
                [edgeStyling.update({e:EDGE_PALETTE}) for e in self.edges]
                print 'No edge coloring palette specified. Will default to palette: \'{0}\'.'.format(EDGE_PALETTE)
        else:
            [edgeStyling.update({e:EDGE_PALETTE}) for e in self.edges]
            print 'No edge coloring rule specified'
            
        self.edgeStyling = edgeStyling
        
        if self.debug:
            if categories:
                print '    Edge Categories:', categories
            print '    Edge styling:', edgeStyling
        return None

    def check_input(self):
        '''IN DEVELOPMENT
        checks if all edges are connecting nodes which exist in the self.nodes'''
        return True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    