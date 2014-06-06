'''
created  03/06/2014

by sperez

Contains HivePlot module used to produce the JavaScript files
needed to make a hive plot in D3 using Mike Bolstock's D3 hive module
'''
#library imports
import os
import sys
import csv
import numpy as np



class HivePlotter():
    '''creates files necessary to make a hive plot in D# given 
        a network with nodes and links stored in a csv file'''
    
    def __init__(self, debug = False):
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
        #transform it into the right data type
        self.nodes = self.convert_type(nodes)
        self.nodeNames = self.convert_type(nodeNames)
        self.nodeProperties = [self.convert_type(p) for p in nodeProperties]
        
        if self.debug:
            print self.nodes
            print self.nodeNames
            print self.nodeProperties
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
            
        


# I test stuff here
hive = HivePlotter()
hive.get_nodes('tests/test_nodes_friends.csv')
