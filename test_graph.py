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
from graph_transformations import *


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
    def test_gtfilter(self):
        print("------------- Filtering node attributes")
        n1 = Node("gloups","ECR",{"start":10, "end": 15, "color":"blue"})
        print("n1\n",n1)
        print("node filtering without side effect")
        g2, n1bis = gt_filter(None, n1, False, {GT_ATT:["start","color"]})
        self.assertEqual(g2, None)
        self.assertNotEqual(n1bis, n1)
        print(n1bis)
        g3, n1ter = gt_filter(None, n1, True, {GT_ATT:["start","color"]})
        self.assertEqual(g3, None)
        self.assertEqual(n1, n1ter)
        print(n1ter)
        n2 = Node("Perlin","Pimpim",{"start":20, "end": 30, "color":"white"})
        print("Composed transformations")
        g3, n2bis = gt_filter(*gt_filter(None, n2, False, {GT_ATT:['start']}), \
                    False, \
                    {GT_ATT:['color']})
        self.assertEqual(g3, None)
        self.assertNotEqual(n2bis, n2)
        print("------------- Filtering node attributes on graph")
        g = Graph("toto")
        g.add_node(Node("test","Part",{"age":12, "field":"rheue"}))    
        g.add_node(Node("test","Part",{"age":13, "field":"bla"}))    
        g.add_node(Node("test","Part",{"age":14, "field":"bli"}))    
        g.add_node(Node("test","Part",{"age":15, "field":"blue"}))
        print(g)
        print("filtered with side effect",n1)
    


if __name__ == "__main__":
    unittest.main()

