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

class TestStructures(unittest.TestCase):
    def test_node(self):
        n1 = Node("dom1","ECO",1)
        print(n1)
        self.assertTrue(True)
        n2 = Node("dom2","Part",125, \
                  {"field1": 25, "field2": 120, "field3": "Gloups"})
        print(n2)
        self.assertTrue(True)
    def test_edge(self):
        e1 = Edge(2, 1, "meca", "LINK", 4, \
                 {"rototo" : 12, "camion" : "vert"})
        print(e1)
        self.assertTrue(True)
    def test_graph(self):
        g = Graph("toto")
        g.add_node(Node("domain12","Part",125, \
                        {"length": 25, "width": 120, "captainage": "YGFY"}))
        g.add_node(Node("domain13","Part",89, \
                        {"length": 10, "width": 80, "captainage": "WTF"}))
        print(g)
        self.assertTrue(True)
    def test_pickledb(self):
        try:
            db = PickleDb("test.pgraph")
            # First time: we erase previous data with dump
            db.dump(Node("test domain 1","ECO",1))
            print("Node appended to DB")
            db.append(Node("test domain 1","ECO",2))
            print("Node appended to DB")
            db.append(Node("test domain 1","ECO",3))
            print("Node appended to DB")
            db.append(Edge(2, 1, "meca", "LINK", 4, \
                           {"rototo" : 12, "camion" : "vert"}))
            print("Edge appended to DB")
            g = Graph("toto")
            g.add_node(Node("domain12","Part",125, \
                           {"length": 25, "width": 120, "captainage": "YGFY"}))
            g.add_node(Node("domain13","Part",89, \
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
        g.add_node(Node("domain12","Part",125, \
                        {"length": 25, "width": 120, "captainage": "YGFY"}))
        g.add_node(Node("domain13","Part",89, \
                        {"length": 10, "width": 80, "captainage": "WTF"}))
        g.add_edge(Edge(125,89,"link","BELONGS_TO",236,{"item1":12}))
        g.graphrep()
        

if __name__ == "__main__":
    unittest.main()

