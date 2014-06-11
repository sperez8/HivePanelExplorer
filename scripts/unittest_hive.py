'''
created  03/06/2014

by sperez

tests all the methods in Hive class
'''
#library imports
import os
import sys
from math import pi
import unittest
from hive import Hive

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)


class TestHive(unittest.TestCase):
    def setUp(self):
        #example hive
        self.emptyhive = Hive(debug = False)
        self.friendsHive = Hive(debug = False)
        self.friendsHiveDouble = Hive(debug = False, doubleAxes = True)
        nodefile = _root_dir + '/tests/test_nodes_friends.csv'
        edgefile = _root_dir + '/tests/test_edges_friends.csv'

        self.friendsHive.get_nodes(nodefile)
        self.friendsHive.get_edges(edgefile)
        self.friendsHiveDouble.get_nodes(nodefile)
        self.friendsHiveDouble.get_edges(edgefile)
        
        
        self.axesOptions = {(False,2):[0,pi], (False,3):[0, pi*2/3, pi*4/3], (False,4):[0,pi/2,pi,pi*3/2], (False,5):[0,pi*2/5,pi*4/5,pi*6/5,pi*8/5], (True,2):[-pi/6,pi/6,pi*5/6,pi*7/6], (True,3):[-pi/9,pi/9,pi*5/9,pi*7/9,pi*11/9,pi*13/9]}
        
        
        self.rules = [(),2,'degree', 'clustering', 'closeness', 'centrality', 'betweeness','average neighbor degree']

    def test_make_axes(self):
        hive = self.emptyhive
        for (doubleAxes, numAxes), angles in self.axesOptions.iteritems():
            hive.doubleAxes = doubleAxes
            hive.numAxes = numAxes
            hive.make_axes()
            angles = [0.0001 if a == 0 else round(a,2) for a in angles]
            self.assertListEqual(angles, hive.angles)

    def test_get_assignment_values(self):
        
        hive = self.friendsHive
        values = hive.get_assignment_values(1)
        correctValues = {'Daniella': 'girl', 'George': 'alien', 'Fatima': 'girl', 'Cam': 'boy', 'Bob': 'boy', 'Alice': 'girl', 'Eric': 'boy'}
        self.assertEqual(values, correctValues)

        hive = self.friendsHiveDouble
        values = hive.get_assignment_values(1)
        correctValues = {'Eric.2': 'boy', 'Cam.2': 'boy', 'Cam.1': 'boy', 'Daniella.1': 'girl', 'Daniella.2': 'girl', 'George.2': 'alien', 'Fatima.2': 'girl', 'Fatima.1': 'girl', 'Eric.1': 'boy', 'Alice.1': 'girl', 'Alice.2': 'girl', 'Bob.2': 'boy', 'George.1': 'alien', 'Bob.1': 'boy'}
        self.assertEqual(values, correctValues)
        
        hive = self.friendsHive
        values = hive.get_assignment_values(2)
        correctValues = {'Daniella': 0.8, 'George': 0.9, 'Fatima': 0, 'Cam': 0.9, 'Bob': 0.2, 'Alice': 1.9, 'Eric': 1.6}
        self.assertEqual(values, correctValues)
        
        hive = self.friendsHiveDouble
        values = hive.get_assignment_values(2)
        correctValues = {'Eric.2': 1.6, 'Cam.2': 0.9, 'Cam.1': 0.9, 'Daniella.1': 0.8, 'Daniella.2': 0.8, 'George.2': 0.9, 'Fatima.2': 0, 'Fatima.1': 0, 'Eric.1': 1.6, 'Alice.1': 1.9, 'Alice.2': 1.9, 'Bob.2': 0.2, 'George.1': 0.9, 'Bob.1': 0.2}
        self.assertEqual(values, correctValues)
        
        hive = self.friendsHive
        values = hive.get_assignment_values('degree')
        correctValues = {'Alice': 4, 'Eric': 2, 'Daniella': 2, 'Fatima': 3, 'Cam': 3, 'Bob': 4, 'George': 2}
        self.assertEqual(values, correctValues)     

        hive = self.friendsHiveDouble
        values = hive.get_assignment_values('degree')
        correctValues = {'Bob.1': 4, 'Cam.2': 3, 'Cam.1': 3, 'Daniella.1': 2, 'Daniella.2': 2, 'George.2': 2, 'Fatima.2': 3, 'Fatima.1': 3, 'Bob.2': 4, 'Alice.1': 4, 'Alice.2': 4, 'Eric.1': 2, 'George.1': 2, 'Eric.2': 2}
        self.assertEqual(values, correctValues)  

if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    