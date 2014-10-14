'''
created  10/10/2014

by sperez

Panel class stores the hive plots to be displayed
'''

#library imports
import sys
import os
import numpy as np

from hive import Hive

SIZE = (2,2) #assignment by position rules
ASSIGNMENT_RULES = ('degree', 'centrality')
POSITION_RULES = ('clustering', 'betweeness')

class Panel():
    '''contains a set of hives'''
    
    def __init__(self, 
                 size = SIZE,
                 debug = True,
                 numAxes = 3,
                 assignmentRules = ASSIGNMENT_RULES,
                 positionRules = POSITION_RULES,
                 edgePalette = EDGE_PALETTE,
                 edgeStyleRule = EDGE_STYLE_RULE,
                 nodeColor = NODE_COLOR
                 ):
        '''Initializing defining parameters of the hive'''
        
        self.debug = debug
        self.size = size
        self.numAxes = numAxes
        self.assignmentRules = assignmentRules
        self.positionRules = positionRules
        self.edgePalette = edgePalette
        self.edgeStyleRule = edgeStyleRule
        self.nodeColor = nodeColor
        self.valuesEdges = None
        self.totalNodes = 0
        self.totalEdges = 0
                
        return None
    
    def make_panel(self):
        '''makes the hive plots and returns the needed assignment values'''
        if not self.size_rules_agree():
            print "the size and rules specified don't agree"
            sys.exit()
        
    def size_rules_agree(self):
        if size[0] != len(assignmentRules):
            return False
        if size[1] != len(positionRules):
            return False
        else:
            return True
        












