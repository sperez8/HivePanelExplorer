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
from graph_utilities import *
import string

#hive parameter defaults when not using GUI
AXIS_ASSIGN_RULE = 'degree'
AXIS_POSIT_RULE = 'closeness'
EDGE_PALETTE = 'purple'
EDGE_STYLE_RULE = 'average connecting degree'
NODE_COLOR = 'blue'
PALETTE = ['blue', 'cornflowerblue', 'darkblue', 'deepskyblue', 'darkturquoise',
               'midnightblue', 'navy', 'dodgerblue', 'lightblue', 'lightskyblue', 'cadetblue', 'teal',
               'paleturquoise', 'aquamarine', 'azure', 'aqua', 'lightsteelblue', 'powderblue']

class Hive():
    '''contains node and edge, coloring, position, etc...'''
    
    def __init__(self, 
                 debug = True,
                 numAxes = 3, 
                 doubleAxes = False, 
                 axisAssignRule = AXIS_ASSIGN_RULE, 
                 axisPositRule = AXIS_POSIT_RULE,
                 edgePalette = EDGE_PALETTE,
                 edgeStyleRule = EDGE_STYLE_RULE,
                 nodeColor = NODE_COLOR
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
        
        try:
            self.axisAssignRule = int(axisAssignRule)
        except ValueError: 
            self.axisAssignRule = axisAssignRule
        
        try:
            self.axisPositRule = int(axisPositRule)
        except ValueError: 
            self.axisPositRule = axisPositRule
        
        return None
 
    
    def make_hive(self, nodefile, edgefile, cutoffValues = None):
        '''runs Hive methods to create an instance from user input'''  
            
        self.get_nodes(nodefile)
        self.get_edges(edgefile)
        self.make_axes()
        self.node_assignment(cutoffValues = cutoffValues)
        self.node_position()
        self.node_style()
        self.make_edges()
        self.edge_style()
        self.fix_color_palette()
        return None


    def get_nodes(self,inputFile):
        '''gets nodes and their properties from csv file'''
        
        delimiter = self.get_delimiter(inputFile)
        data = np.genfromtxt(inputFile, delimiter=delimiter, dtype='str')
        
        #get properties and format as strings
        properties = data[0,1:]
        properties = self.format_properties(properties)
        
        #remove first row with column names
        data = data[1:,]
        
        #get all the node data
        nodes = list(data[:,0])
        
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
            print '    Nodes are: '
            print ','.join(self.nodes)
            print '    Node properties are: '
            for k,v in self.nodeProperties.iteritems():
                print k, v
                
        return self.nodeProperties


    def get_edges(self,inputFile):
        '''gets edges and their properties from csv file'''
        
        delimiter = self.get_delimiter(inputFile)
        data = np.genfromtxt(inputFile, delimiter=delimiter, dtype='str')
        
        #get properties and format as strings
        properties = data[0,2:]
        properties = self.format_properties(properties)
        
        #remove first row with column names
        data = data[2:,]
        
        #get all the edge data
        self.sources = list(data[:,0])        
        self.targets = list(data[:,1])

        #transform edge properties into the numerical types if possible
        edgeProperties = {}
        for i, column in enumerate(data[:,2:].T):
            values = convert_type(list(column))
            edgeProperties[properties[i]] = values
        self.edgeProperties = edgeProperties
        
        #store the name of the edge properties
        self.edgePropertyList = edgeProperties.keys()
            
        if self.debug:
            print '    Sources are: ', self.sources
            print '    Targets are: ', self.targets
            print '    Edge properties are: ', self.edgeProperties
            
        return self.edgeProperties


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
        #check if styling values are numerical, otherwise treat as categorical
        # and recode into numerical variables
        categories = find_categories(values)
        if categories:
            if len(categories) != self.numAxes:
                print 'The number of node groups using the rule \'{0}\' is different than the number of axes ({1})!'.format(self.axisAssignRule, self.numAxes)
            [axisAssignment.update({n:categories.index(v)}) for n,v in assignmentValues.iteritems()] 
            [axisAssignment.update({n:i+1}) for n,i in axisAssignment.iteritems()] #want the node group to start at 1, not 0
            #save categories values to be displayed on plot
            self.valuesAssignment = categories
        else:
            if not cutoffValues:      
                values.sort()
                cutoffIndexes = [int(len(values)/self.numAxes)*i for i in range(1,self.numAxes)]
                cutoffValues = [values[c] for c in cutoffIndexes] # to prevent nodes with the same value to be in different groups
            if values[-1] not in cutoffValues:
                cutoffValues.append(values[-1]) #add greatest value as a cutoff
                
            for n in self.nodes:
                i = 0
                while i < len(cutoffValues):
                    if assignmentValues[n] <= cutoffValues[i]:
                        axisAssignment[n]=i+1 #want the node group to start at 1, not 0
                        break
                    else: i+=1
            #save cutoff values to be displayed on plot
            cutoffValues.insert(0,0)
            self.valuesAssignment = [str(cutoffValues[i-1])+'-'+str(val) for i,val in enumerate(cutoffValues)]
            self.valuesAssignment.pop(0)
                
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
            print '    Node positions on axis:', nodePositions
        
        return None


    def get_assignment_values(self, rule):
        '''get the values to be used to assign nodes to axes.
            If the rule is a network property, then a networkx graph is created
            and analyzed. Otherwise, assignment values are organized in a dictionary'''
        
        assignmentValues = {}
        if rule in self.nodeProperties.keys():
            #get assignment values from the column of node properties indicated by the interger "rule"
            properties = self.nodeProperties[rule]
            if self.doubleAxes:
                [assignmentValues.update({n:p}) for n,p in zipper(self.nodes, properties*2)]
            else:
                [assignmentValues.update({n:p}) for n,p in zipper(self.nodes, properties)]
                
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
                elif axis[t] == 1 and axis[t] == self.numAxes:
                    newSources.append(s)
                    newTargets.append(t)   
                    newProperties.append(p)     
        
        #save the new edges and their properties
        self.edges = zipper(newSources, newTargets)
        self.edgeProperties = newProperties
        
        if self.debug:
            print '    The new edges with their properties are:', self.edges
            print '    ', self.edgeProperties
            
        return None


    def get_edge_properties(self, rule):
        '''Organize edge properties in a dicitonary to be used to color the edges'''
         
        values = {}
        if rule in self.edgeKeys:
            i = self.edgeKeys.index(rule)
            properties = zip(*self.edgeProperties)[i]
            [values.update({e:p}) for e,p in zipper(self.edges, properties)]
            return values
        else: 
            print "The edge styling rule could not be parsed"
            sys.exit()


    def node_style(self, opacity = 0.9, color = 'purple', size = '7'):
        '''In development...'''
        return None

    
    def edge_style(self, opacity = 0.9, color = 'purple', size = '7'):
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
                    cutoffValues.insert(0,0)
                    self.valuesEdges = [str(cutoffValues[i-1])+'-'+str(val) for i,val in enumerate(cutoffValues)]
                    self.valuesEdges.pop(0)
            
            else:
                [edgeStyling.update({e:0}) for e in self.edges]
                print 'No edge coloring palette specified. Will default to palette: \'{0}\'.'.format(EDGE_PALETTE)
        else:
            #No edge coloring rule specified
            [edgeStyling.update({e:0}) for e in self.edges]
            
        self.edgeStyling = edgeStyling
        
        if self.debug:
            if categories:
                print '    Edge Categories:', categories
            print '    Edge styling:', edgeStyling
            
        return None


    def fix_color_palette(self):
        '''fix edge palette so it can be plotted'''
        
        if not isinstance(self.edgePalette, list) or len(self.edgePalette) < len(set(self.edgeStyling.values())):
            print 'Using default color palette'
            self.edgePalette  = PALETTE[:len(set(self.edgeStyling.values()))]
        
        return None


    @staticmethod
    def get_delimiter(inputFile):
        '''detect if input file is a tab or comma delimited file
            and return delimiter.'''
        
        ext = os.path.splitext(os.path.basename(inputFile))[1]
        
        if 'tab' in ext or 'tsv' in ext:
            return '\t'
        elif 'csv' in ext:
            return ','
        elif 'txt' in ext:
            #detects delimeter by counting the number of tabs and commas in the first line
            f = open(inputFile, 'r')
            first = f.read()
            if first.count(',') > first.count('\t'):
                return ','
            elif first.count(',') < first.count('\t'):
                return '\t'
            else:
                print "Couldn't detect a valid file extension: ", inputFile
                return ','
        else:
            print "Couldn't detect a valid file extension: ", inputFile
            return ','


    @staticmethod
    def format_properties(properties):
        '''takes a list of property names and removes all punctuation and numbers'''
        
        numbers = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten'}
        
        def convert_word(word):
            '''remove punctuation and numbers from a word'''
            w = word
            for c in string.punctuation + string.digits:
                word = word.replace(c,'')
            if w != word:
                print "The property \'{0}\' contained punctuation or digits which were removed".format(w)
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

        