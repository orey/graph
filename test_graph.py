#-------------------------------------------------------------------------------
# Name:        test_graph.py
# Purpose:     Test graph structures
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import unittest, traceback, sys

from graph import *
from db_pickle import PickleDb

from gt_filter_attributes import *
from gt_clone             import *

class TestStructures(unittest.TestCase):
    def test_node(self):
        n1 = Node("dom1","ECO")
        print(n1)
        self.assertTrue(True)
        n2 = Node("dom2","Part", \
                  {"field1": 25, "field2": 120, "field3": "Gloups"})
        print(n2)
        self.assertTrue(True)
        e1 = Edge(n1.get_uuid(), n2.get_uuid(), "meca", "LINK", \
                 {"rototo" : 12, "camion" : "vert"})
        print(e1)
        self.assertTrue(True)
    def test_graph(self):
        g = Graph("toto")
        g.add_node(Node("domain12","Part", \
                        {"length": 25, "width": 120, "captainage": "YGFY"}))
        g.add_node(Node("domain13","Part", \
                        {"length": 10, "width": 80, "captainage": "WTF"}))
        print(g)
        self.assertTrue(True)
    def test_pickledb(self):
        try:
            db = PickleDb("test.pgraph")
            # First time: we erase previous data with dump
            db.dump(Node("test domain 1","ECO"))
            print("Node appended to DB")
            n2 = Node("test domain 1","ECO")
            db.append(n2)
            print("Node appended to DB")
            n3 = Node("test domain 1","ECO")
            db.append(n3)
            print("Node appended to DB")
            db.append(Edge(n2.get_uuid(), n3.get_uuid(), "meca", "LINK", \
                           {"rototo" : 12, "camion" : "vert"}))
            print("Edge appended to DB")
            g = Graph("toto")
            g.add_node(Node("domain12","Part", \
                           {"length": 25, "width": 120, "captainage": "YGFY"}))
            g.add_node(Node("domain13","Part", \
                           {"length": 10, "width": 80, "captainage": "WTF"}))
            db.append(g)
            print("Graph appended to DB")
        except Exception as e:
            self.assertTrue(False)
            traceback.print_exc(file=sys.stdout)
            print("Exception caught: ", type(e), e.args)
            exit(0)
        self.assertTrue(True)
        try:
            objects = db.read_items()
            for o in objects:
                print(o)
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
            traceback.print_exc(file=sys.stdout)
            print("Exception caught: ", type(e), e.args)
            exit(0)
    def test_graph(self):
        g = Graph("toto")
        n1 = Node("domain12","Part", \
                        {"length": 25, "width": 120, "captainage": "YGFY"})
        g.add_node(n1)
        n2 = Node("domain13","Part", \
                        {"length": 10, "width": 80, "captainage": "WTF"})
        g.add_node(n2)
        g.add_edge(Edge(n1.get_uuid(),n2.get_uuid(),"link","BELONGS_TO",{"item1":12}))
        g.graphrep()
        
class TestGraphTransfo(unittest.TestCase):
    def test_gt_filter_attributes(self):
        print("------------- Filtering node attributes")
        n1 = Node("gloups","ECR",{"start":10, "end": 15, "color":"blue"})
        print("n1\n",n1)
        print("node filtering without side effect")
        n1bis = gt_filter_attributes(n1, False, attributes=["start","color"])
        self.assertNotEqual(n1bis, n1)
        print(n1bis)

        n1ter = gt_filter_attributes(n1, True, attributes=["start","color"])
        self.assertEqual(n1, n1ter)
        print(n1ter)

        n2 = Node("Perlin","Pimpim",{"start":20, "end": 30, "color":"white"})

        print("Composed transformations")
        n2bis = gt_filter_attributes( \
                    gt_filter_attributes(n2, False, attributes=['start']), \
                    False, \
                    attributes=['color'])
        self.assertNotEqual(n2bis, n2)
        
        print("------------- Filtering node attributes on graph")
        g = Graph("toto")
        g.add_node(Node("test","Part",{"age":12, "field":"rheue"}))    
        g.add_node(Node("test","Part",{"age":13, "field":"bla"}))    
        g.add_node(Node("test","Part",{"age":14, "field":"bli"}))    
        g.add_node(Node("test","Part",{"age":15, "field":"blue"}))
        print(g)
        print("filtered with side effect",n1)
        # TODO Complete test
    def test_gt_clone(self):
        n = test_data_factory(1)
        g = gt_clone(n)
        print(n)
        print(g)
        # reprendre ici
        r = analyze_nodes(n1, n2)
        self.assertEqual(r, CLONES)
        
NOT_SAME_ATTRIBUTES = -1
NOT_SAME_VALUES = -2
NOT_SAME_NB_ATTRIBUTES = -3
SAME_ID_DIFFERENT_CONTENT = -4
DIFFERENT_ATTRIBUTES = -5
CLONES = 2
SAME_NODES = 1

def analyze_nodes(n1, n2):
    def analyze_field(f1, l1, l2):
        if f1 not in l2:
            print('Nodes dont have the same attributes')
            print(f1, "is not in node 2")
            return NOT_SAME_ATTRIBUTES
        if l1[f1] != l2[f1]:
            print('Nodes have the same attributes but not the same values')
            print("attribute", f1, "value 1", l1[f1], "value 2", l2[f1])
            return NOT_SAME_VALUES
        return True          
    l1 = n1.get_attributes()
    l2 = n2.get_attributes()
    if len(l1) != len(l2):
        print("The two nodes don't have the same number of attributes")
        return NOT_SAME_NB_ATTRIBUTES
    sameid = False
    if n1.get_id() == n2.get_id():
        sameid = True
    newl1 = dict((key,value) for key, value in l1.items() if key != "uuid")
    if sameid:
        for att1 in newl1:
            if not analyze_field(att1, newl1, l2):
                print('Nodes have the same id but they are not identical')
                return SAME_ID_DIFFERENT_CONTENT
        return SAME_NODES
    else:
        for att1 in newl1:
            if not analyze_field(att1, newl1, l2):
                print('Nodes are different')
                return DIFFERENT_ATTRIBUTES
        print("Nodes are probably clones: different id, same fields and values")
        return CLONES

def test_data_factory(i):
    if i == 1:
        return Node("test","Part",{"age":12, "field1":"rheue", "field2":"toto"})


if __name__ == "__main__":
    unittest.main()

