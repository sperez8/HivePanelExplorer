'''
created  03/06/2014

by sperez

Hive class stores the nodes, edges and how they will be displayed
including node position, edge coloring, number of axes etc...
'''

#library imports
import sys
import os
import numpy as np

from math import pi
from hive_utilities import *
import string

#hive parameter defaults when not using GUI
AXIS_ASSIGN_RULE = 'degree'
AXIS_POSIT_RULE = 'closeness'
EDGE_PALETTE = 'grey'
EDGE_STYLE_RULE = 'average connecting degree'
NODE_COLOR = 'grey'
PALETTE = ['blue', 'cornflowerblue', 'darkblue', 'deepskyblue', 'darkturquoise',
               'midnightblue', 'navy', 'dodgerblue', 'lightblue', 'lightskyblue', 'cadetblue', 'teal',
               'paleturquoise', 'aquamarine', 'azure', 'aqua', 'lightsteelblue', 'powderblue']

class Hive():
    '''contains node and edge, coloring, position, etc...'''
    
    def __init__(self, 
                 debug = True,
                 filter = False,
                 numAxes = 3, 
                 doubleAxes = False, 
                 axisAssignRule = AXIS_ASSIGN_RULE, 
                 axisPositRule = AXIS_POSIT_RULE,
                 edgePalette = EDGE_PALETTE,
                 edgeStyleRule = EDGE_STYLE_RULE,
                 nodeColor = NODE_COLOR,
                 rawMeasures = False
                 ):
        '''Initializing defining parameters of the hive'''
        
        self.debug = debug
        self.numAxes = numAxes
        self.doubleAxes = doubleAxes
        self.axisAssignRule = axisAssignRule 
        self.axisPositRule = axisPositRule
        self.edgePalette = edgePalette
        self.edgeStyleRule = edgeStyleRule
        self.nodeColor = nodeColor
        self.valuesEdges = None
        self.rawMeasures = rawMeasures
        self.totalNodes = 0
        self.totalEdges = 0
        
        try:
            self.axisAssignRule = int(axisAssignRule)
        except ValueError: 
            self.axisAssignRule = axisAssignRule
        
        try:
            self.axisPositRule = int(axisPositRule)
        except ValueError: 
            self.axisPositRule = axisPositRule
        
        return None
 
    
    def make_hive(self, nodeFile, edgeFile, cutoffValues = None, filter = False, makeAllEdges = False, graphml = False):
        '''runs Hive methods to create an instance from user input'''  
        
        if graphml:
            self.get_graphml(nodeFile)
        else:
            self.get_nodes(nodeFile)
            self.get_edges(edgeFile)               
        #XXX
        #self.check_nodes(self.sources, self.targets, self.nodes, self.doubleAxes, self.debug)
        self.make_axes()
        self.node_assignment(cutoffValues = cutoffValues)
        self.node_position()
        self.node_style()
        self.make_edges(makeAllEdges = makeAllEdges)


        self.edge_style()
        self.fix_color_palette()
        return None


    def get_nodes(self,inputFile):
        '''gets nodes and their properties from csv file'''
        
        delimiter = get_delimiter(inputFile)

        data = np.genfromtxt(inputFile, delimiter=delimiter, dtype='str', filling_values = 'None')
        
        #get properties and format as strings
        properties = data[0,1:]
        properties = self.format_properties(properties, self.debug)
        
        #remove first row with column names
        data = data[1:,]
        
        #get all the node data
        nodes = list(data[:,0])
        
        #take note of number of nodes
        self.totalNodes = len(nodes)
        
        #double the number of nodes when axes are doubled
        if self.doubleAxes:
            self.nodes = [n+".1" for n in nodes]
            self.nodes.extend([n+".2" for n in nodes])
        else: 
            self.nodes = nodes
        
        #transform node properties into the numerical types if possible
        nodeProperties = {}

        for i, column in enumerate(data[:,1:].T):
            values = convert_type(list(column))
            nodeProperties[properties[i]] = values
        self.nodeProperties = nodeProperties
        
        if self.debug:
            print '    There are {0} nodes.'.format(len(self.nodes))
            print '    These are the Node properties: "{0}"'.format(', '.join(self.nodeProperties.keys()))

        return self.nodeProperties


    def get_edges(self,inputFile):
        '''gets edges and their properties from csv file'''
        
        delimiter = get_delimiter(inputFile)
        data = np.genfromtxt(inputFile, delimiter=delimiter, dtype='str', filling_values = 'None')
        
        #get properties and format as strings
        properties = data[0,2:]
        properties = self.format_properties(properties, self.debug)
        
        #remove first row with column names
        data = data[1:,]
        
        #get all the edge data
        self.sources = list(data[:,0])        
        self.targets = list(data[:,1])
        
        #take note of number of edges:
        self.totalEdges = len(self.sources)

        #transform edge properties into the numerical types if possible
        edgeProperties = {}

        for i, column in enumerate(data[:,2:].T):
            values = convert_type(list(column))
            edgeProperties[properties[i]] = values
        self.edgeProperties = edgeProperties
        
        #store the name of the edge properties
        self.edgePropertyList = edgeProperties.keys()
            
        if self.debug:
            print '    There are {0} edges in this network.'.format(self.totalEdges)
            print '    The properties of the edges:  "{0}"'.format(', '.join(self.edgePropertyList))
        

        return self.edgeProperties

    def get_graphml(self, inputFile):
        graph = nx.read_graphml(inputFile)
        self.nodes = graph.nodes()
        edges = graph.edges()
        self.sources, self.targets = zip(*edges)
        print self.nodes, self.sources

    def make_axes(self):
        '''creates axes and angles given the number of axes desired
        and whether the axes are being doubled or not'''
        
        angles = []
        if self.doubleAxes:
            #create a total of 3*self.numAxes to create spacing between the doubled axes
            allAngles = [2.0*pi/float(self.numAxes*3)*i for i in range(0,self.numAxes*3)]
            
            #re-center the axes for symmetry
            shiftBy = allAngles[1]/2.0
            allAngles = [a-shiftBy for a in allAngles]
            
            #remove the "spacer" axes
            for a in allAngles:
                if (allAngles.index(a)+1) % 3 != 0:
                    angles.append(a)
        else:
            angles = [2.0*pi/float(self.numAxes)*i for i in range(0,self.numAxes)]

        angles = [round(a,2) for a in angles]
        angles = [0.0001 if a == 0 else a for a in angles] #d3 code won't work with an angle of zero...
        
        if self.numAxes==2: #hive plots with 2 axis are better viewed horizontally so we rotate them
            angles = [a-pi/2 for a in angles]
        
        if self.debug:
            print "Axes angles are", angles   
        
        self.angles = angles
        
        return None


    def node_assignment(self, assignmentValues = None, cutoffValues = []):
        '''determines on which axis the node should be placed
            depending on the rule. Integer valued rules indicate the index of a
            node property in the list of properties. Rules which are string values denote network 
            properties which need to be calculated. Nodes are partitioned into groups
            depending on their value related to the rule. There are as many groups
            as numAxes'''
        
        axisAssignment = {} 
        if not assignmentValues:
            assignmentValues = self.get_assignment_values(self.axisAssignRule)
        
        values = assignmentValues.values()
        if self.rawMeasures:
            self.axisAssignment = assignmentValues
            return None
        else:
            #check if styling values are numerical, otherwise treat as categorical
            # and recode into numerical variables
            categories = find_categories(values)
            if categories:
                if len(categories) != self.numAxes:
                    print 'The number of node groups using the rule \'{0}\' is different than the number of axes ({1})!'.format(self.axisAssignRule, self.numAxes)
                for n,v in assignmentValues.iteritems():
                    axisAssignment[n] = categories.index(v) + 1 #want the node group to start at 1, not 0
                #save categories values to be displayed on plot
                self.valuesAssignment = categories
            else:
                if not cutoffValues:      
                    values.sort()
                    if len(set(values)) < self.numAxes:
                        print "\nPlease choose a different rule for assigning nodes to axes. There aren't enough unique values for all {1} axes".format(self.edgeStyleRule, self.numAxes)
                        sys.exit()
                    cutoffIndexes = [int(len(values)/self.numAxes)*i for i in range(1,self.numAxes)]
                    cutoffValues = [values[c] for c in cutoffIndexes] # to prevent nodes with the same value to be in different groups
                if values[-1] not in cutoffValues:
                    cutoffValues.append(values[-1]) #add greatest value as a cutoff
                    
                j = 0
                for n in self.nodes:
                    i = 0
                    while i < len(cutoffValues):
                        if n not in assignmentValues.keys():
                            j+=1
                            break
                        elif assignmentValues[n] <= cutoffValues[i]:
                            axisAssignment[n]=i #want the node group to start at 0
                            break
                        else: i+=1
                        
                #save cutoff values to be displayed on plot
                self.valuesAssignment = self.reformat(cutoffValues)
            
            if self.doubleAxes:
                newAssignment = {}
                #for the case of 3 doubled axis, the axis groups become 2,4, or 6 for nodes ending in '.2'
                #and 1,3,or 5 for nodes ending in '.1'
                for n,i in axisAssignment.iteritems():
                    if  n[-2:] == '.1':
                        newAssignment[n] = i*2 - 1
                    else:
                        newAssignment[n] = i*2
                axisAssignment = newAssignment
        
            self.axisAssignment = axisAssignment
    
            if self.debug:
                if categories:
                    print '    Node Categories:', categories
                print '    For the rule "{0}", the cut off values for assigning nodes to axes are: {1}'.format(self.axisAssignRule, self.valuesAssignment)
                
            return None


    def node_position(self):
        '''determines where on the axis the node should be placed
            depending on the rule. Integer valued rules indicate the use of
            node properties. Rules which are string values denote network 
            properties which need to be calculated. node positions are scaled
            equally for all axes'''
        
        nodePositions = {}
        assignmentValues = self.get_assignment_values(self.axisPositRule)
        
        if self.rawMeasures:
            self.nodePositions = assignmentValues
            return None
        else:
            values = assignmentValues.values()
            #check if styling values are numerical, otherwise treat as categorical
            # and recode into numerical variables
            categories = find_categories(values)
            if categories:
                categories.sort() # sorts strings alphabetically
                maxValue = len(categories) #index of last element in categories + 1
                for n,p in assignmentValues.iteritems():
                    nodePositions[n] = round(float(categories.index(p))/float(maxValue),3)
                #save categories values to be displayed on plot
                self.valuesPosition = categories
            else:    
                maxValue = max(values)
                for n,p in assignmentValues.iteritems():
                    nodePositions[n] = round(float(p)/float(maxValue),3)
                #save min,max values pf positions to be displayed on plot
                self.valuesPosition = [str(min(values)),str(maxValue)]
                    
            self.nodePositions = nodePositions
            if self.debug:
                if categories:
                    print '    For the rule "{0}", the values for positioning nodes onto axes are categorical values: {1}'.format(self.axisPositRule, self.valuesPosition)
                else:
                    print '    For the rule "{0}", the values for positioning nodes onto axes occur in this range: {1}'.format(self.axisPositRule, self.valuesPosition)
            
            return None


    def get_assignment_values(self, rule):
        '''get the values to be used to assign nodes to axes.
            If the rule is a network property, then a networkx graph is created
            and analyzed. Otherwise, assignment values are organized in a dictionary'''
        
        assignmentValues = {}
        if rule in self.nodeProperties.keys():
            #get assignment values from the column of node properties indicated by the "rule"
            properties = self.nodeProperties[rule]
            if self.doubleAxes:
                [assignmentValues.update({n:p}) for n,p in zipper(self.nodes, properties*2)]
            else:
                [assignmentValues.update({n:p}) for n,p in zipper(self.nodes, properties)]
            return assignmentValues
        
        elif isinstance(rule, str):
            #Need to make a graph instance using networkx
            G = make_graph(self.sources, self.targets, self.nodes)
            assignmentValues = node_analysis(G, rule)
            if self.doubleAxes:
                newAssignmentValues = {}
                for n,v in assignmentValues.iteritems():
                    newAssignmentValues[n +'.1'] = v
                    newAssignmentValues[n +'.2'] = v
                return newAssignmentValues
            else:
                return assignmentValues
        else: 
            print "\nRule could not be parsed"
            sys.exit()


    def make_edges(self, makeAllEdges = False):
        '''takes sources and edges and makes a list of 
        edges while assignment nodes to the correct axis in 
        the case of double axis. also keeps track of edge properties.'''
        
        newSources = []
        newTargets = []
        newProperties = []
        axis = self.axisAssignment
        keys = []
        properties = []
        for k,v in self.edgeProperties.iteritems():
            keys.append(k)
            properties.append(v)
        
        reorganizedProperties = zip(*properties)
        self.edgeKeys = keys

        if makeAllEdges:
            self.edgeProperties = reorganizedProperties
            self.edges = zipper(self.sources, self.targets)
            return None

        for s,t,p in zipper(self.sources, self.targets, reorganizedProperties):
            if self.doubleAxes:
                s1 = s + '.1'
                s2 = s + '.2'
                t1 = t + '.1'
                t2 = t + '.2'

                #if nodes are from same group we add edge
                #and it's symmetrical edge within the doubled Axes
                if axis[s1] == axis[t1]:
                    newSources.extend([s1,s2])
                    newTargets.extend([t2,t1])
                    newProperties.append(p)
                    newProperties.append(p) #add properties twice for both symmetric edges
                #if nodes from different groups, we make an edge
                #between the '.1' or '.2' nodes nearest to each other
                elif axis[s1] == axis[t1] + 2:
                    newSources.append(s1)
                    newTargets.append(t2)
                    newProperties.append(p)
                    if self.numAxes == 2 and self.doubleAxes: #need symmetry for 2 axes plots
                        newSources.append(t1)
                        newTargets.append(s2)
                        newProperties.append(p) 
                elif axis[s1] + 2 == axis[t1]:
                    newSources.append(s2)
                    newTargets.append(t1)
                    newProperties.append(p)
                    if self.numAxes == 2 and self.doubleAxes: #need symmetry for 2 axes plots
                        newSources.append(s1)
                        newTargets.append(t2)
                        newProperties.append(p) 
                #the edges below loop back from the highest numbered axis to the first axis
                elif axis[s1] == 1 and axis[t2] == self.numAxes*2:
                    newSources.append(s1)
                    newTargets.append(t2)
                    newProperties.append(p)
                elif axis[t1] == 1 and axis[s2] == self.numAxes*2:
                    newSources.append(s2)
                    newTargets.append(t1)
                    newProperties.append(p)
                else:
                    pass
            else:
                
                #makes edges for nodes of neighboring axes,
                #doesn't include self nodes, nor nodes of same group
                #nor nodes from non-neighboring axes when numAxes >3
                if abs(axis[s]-axis[t]) == 1:
                    newSources.append(s)
                    newTargets.append(t)
                    newProperties.append(p)
                #gets edges that connect nodes on the 1st and last axes when there are 2 axes
                elif axis[s] == 1 and axis[t] == self.numAxes:
                    newSources.append(s)
                    newTargets.append(t)
                    newProperties.append(p)
                elif axis[t] == 1 and axis[s] == self.numAxes:
                    newSources.append(s)
                    newTargets.append(t)   
                    newProperties.append(p)     
        
        #save the new edges and their properties
        self.edges = zipper(newSources, newTargets)
        self.edgeProperties = newProperties
        
        #update the number of edges
        self.totalEdges = len(self.edges)
        
        if self.totalEdges == 0:
            print "\nUsing this axis assignment rule, there were no edges found between the different axes."
            print "Please choose a different rule."
            sys.exit()
        
        if self.debug:
            print '    There are now {0} edges that will be drawn'.format(self.totalEdges)
            
        return None


    def get_edge_properties(self, rule):
        '''Organize edge properties in a dictionary to be used to color the edges'''
         
        values = {}
        if rule in self.edgeKeys:
            i = self.edgeKeys.index(rule)
            properties = zip(*self.edgeProperties)
            properties = properties[i]
            [values.update({e:p}) for e,p in zipper(self.edges, properties)]
            return values
        else: 
            print "The edge styling rule could not be parsed"
            sys.exit()


    def node_style(self, opacity = 0.9, color = 'purple', size = '7'):
        '''In development...'''
        return None

    
    def edge_style(self, opacity = 0.9, color = EDGE_PALETTE, size = '7'):
        '''determines how the edges will look given different characteristics'''
        
        edgeStyling = {}
        categories = None
        if self.edgeStyleRule != EDGE_STYLE_RULE and self.edgeStyleRule != None:
            edgeValues = self.get_edge_properties(self.edgeStyleRule)
            values = edgeValues.values()
            if self.edgePalette != EDGE_PALETTE:
                #check if styling values are numerical, otherwise treat as categorical
                categories = find_categories(values)
                if categories:
                    [edgeStyling.update({e:categories.index(edgeValues[e])}) for e in self.edges ]
                    #save categories values to be displayed on plot
                    self.valuesEdges = categories
                else:
                    values.sort()
                    cutoffs = [int(len(values)/float(len(self.edgePalette)))*i for i in range(1,len(self.edgePalette))]
                    cutoffValues = [values[c-1] for c in cutoffs] # to prevent nodes with the same value to be in different groups
                    cutoffValues.append(values[-1])
                    for e in self.edges:
                        i = 0
                        while i < len(cutoffValues):
                            if edgeValues[e] <= cutoffValues[i]:
                                edgeStyling[e]=i
                                break
                            else: i+=1
                    #save cutoff values to be displayed on plot
                    self.valuesEdges = self.reformat(cutoffValues)
            
            else:
                [edgeStyling.update({e:0}) for e in self.edges]
        else:
            #No edge coloring rule specified
            [edgeStyling.update({e:0}) for e in self.edges]
            
        self.edgeStyling = edgeStyling
        
        if self.debug:
            if categories:
                print '    Edge Categories:', categories
            print '    For the rule "{0}", the cut off values for styling edges are: {1}'.format(self.edgeStyleRule, self.valuesEdges)
            
        return None


    def fix_color_palette(self):
        '''fix edge palette so it can be plotted'''
        
        if not isinstance(self.edgePalette, list) or len(self.edgePalette) < len(set(self.edgeStyling.values())):
            if self.debug:
                print 'Not enough colors for number of types of edges. Using default color palette'
            self.edgePalette  = PALETTE[:len(set(self.edgeStyling.values()))]
        
        return None

    @staticmethod
    def format_properties(properties, debug = False):
        '''takes a list of property names and removes all punctuation and numbers'''
        
        numbers = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten'}
        
        def convert_word(word):
            '''remove punctuation and numbers from a word'''
            w = word
            word = ''.join(word.split()) #removes all whitespace (tabs, newlines, spaces...)
            for c in string.punctuation + string.digits:
                word = word.replace(c,'')
            if w != word:
                if debug:
                    print "The property \'{0}\' contains spaces, punctuation or digits and has been renamed '{1}'".format(w,word)
            return word
             
        newProperties = []
        i = 1
        for prop in properties:
            newProp = convert_word(prop)
            if not newProp:
                #if property isn't named, we give it one
                newProperties.append('unNamedProperty' + numbers[i] + '')
                i += 1
            elif newProp in newProperties:
                newProperties.append(newProp + 'second')
            else:
                newProperties.append(newProp)
                
        return newProperties
    
    @staticmethod
    def reformat(cutoffValues):
        '''brocken. Being fixed...'''
#         cutoffValues.insert(0,0)
#         d = 2
#         badlyRounded = True
#         if isinstance(cutoffValues[1], int):
#            roundedValues = cutoffValues
#         else:
#             while badlyRounded:
#                 roundedValues = [round(val,d) for val in cutoffValues]
#                 newValues = [roundedValues[i-1] - val for i,val in enumerate(roundedValues)]
#                 if 0 not in newValues[1:]:
#                     badlyRounded = False
#                 d += 1
#         valuesAssignment = [str(roundedValues[i-1])+'-'+str(val) for i,val in enumerate(roundedValues)]
#         valuesAssignment.pop(0)
#         
#         return valuesAssignment  

        return [str(c) for c in cutoffValues]

    @staticmethod
    def check_nodes(sources, targets, nodes, double, debug):
        '''check that all nodes are found in the sources and targets'''
        newNodes = []
        
        if double:
            for n in nodes:
                if n[:-2] in sources:
                    newNodes.append(n)
                elif n[:-2] in targets:
                    newNodes.append(n)
                else:
                    pass
            old = len(nodes)/2
            new = len(newNodes)/2
        else:
            for n in nodes:
                if n in sources:
                    newNodes.append(n)
                elif n in targets:
                    newNodes.append(n)
                else:
                    pass
            old = len(nodes)
            new = len(newNodes)
        
        if new == 0:
            print "No nodes were found in the edge file! Please check that the names of the nodes are the same in both files"
            print "Exiting..."
            sys.exit()  
            
        elif new < old:
            if debug:
                print "\n\n***WARNING: {0} of the {1} nodes were not found in the edge file! You may filter them out using filter_data.py and rerun HivePlotter or continue.***".format(old-new,old)                        
            
        return None
    
if __name__ == "__main__":
    hive = Hive()
    for d in [True, False]:
        for a in [2,3,4]:
            print d, a
            hive.numAxes = a
            hive.doubleAxes = d
            hive.make_axes()
            print hive.angles

