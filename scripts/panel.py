'''
created  10/10/2014

by sperez

Panel class stores the hive plots to be displayed
'''

#library imports
import sys
import os
import numpy as np
import webbrowser
from hive import *
from html_writer import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

SIZE = (4,4) #assignment by position rules
ASSIGNMENT_RULES = ['degree', 'betweeness', 'clustering', 'centrality', 'component']
POSITION_RULES = ['degree', 'betweeness', 'clustering', 'centrality', 'component']

class Panel():
    '''contains a set of hives'''
    
    def __init__(self, 
                 size = SIZE,
                 debug = False,
                 numAxes = 3,
                 doubleAxes = False,
                 assignmentRules = ASSIGNMENT_RULES,
                 positionRules = POSITION_RULES,
                 edgePalette = EDGE_PALETTE,
                 edgeStyleRule = EDGE_STYLE_RULE,
                 nodeColor = NODE_COLOR,
                 rawMeasures = False
                 ):
        '''Initializing defining parameters of the hive'''
        
        self.debug = debug
        self.size = size
        self.numAxes = numAxes
        self.doubleAxes = False
        self.assignmentRules = assignmentRules
        self.positionRules = positionRules
        self.edgePalette = edgePalette
        self.edgeStyleRule = edgeStyleRule
        self.nodeColor = nodeColor
        self.valuesEdges = None
        self.rawMeasures = rawMeasures
        self.totalNodes = 0
        self.totalEdges = 0
                
        return None
    
    def make_panel(self, nodefile, edgefile):
        '''makes the hive plots and returns the needed assignment values'''
        if not self.size_rules_agree():
            print "The number of rules and the specified size of the panel don't agree."
            sys.exit()
        self.rulePairs = self.cross_rules(self.assignmentRules, self.positionRules)
        Hives = {}
        for a,p in self.rulePairs:
            hive = Hive(debug = self.debug,
                    numAxes = self.numAxes,
                    doubleAxes = self.doubleAxes, 
                    axisAssignRule = a, 
                    axisPositRule = p,
                    edgePalette = self.edgePalette, 
                    edgeStyleRule = self.edgeStyleRule,
                    nodeColor = self.nodeColor,
                    rawMeasures = self.rawMeasures
                    )
            
            if nodefile.split('.')[-1] == 'graphml':
                hive.make_hive(nodefile, None, makeAllEdges = True, graphml = True) 
            else:
                hive.make_hive(nodefile, edgefile, makeAllEdges = True) 
            Hives[(a,p)] = hive
            hive = None
        
        self.Hives = Hives
        return None
    
    def open_panel(self, title, folder, only_input_files = False):
        url = make_panel_html(title, self.Hives, self.size, rules = self.rulePairs, only_input_files = only_input_files)
        if only_input_files:
            sys.exit()
        webbrowser.open("file://"+url, new=2)
        
    def size_rules_agree(self):
        if self.size[0] != len(self.assignmentRules):
            return False
        if self.size[1] != len(self.positionRules):
            return False
        else:
            return True
        
    @staticmethod
    def cross_rules(asgRules, posRules):
        rules = []
        for a in asgRules:
            for p in posRules:
                rules.append((a,p))
        return rules










