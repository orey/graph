#-------------------------------------------------------------------------------
# Name:        gt_fusion.py
# Purpose:     Fusioning 2 graphs graph transformation
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import copy, uuid
from graph import *
from gt_clone import *

GRAPH = 'graph'

def gt_fusion(root, sideeffect=True, **kwargs):
    """
    root: source Graph
    graph=secondGraph: Type Graph
    Warning: gt_fusion does not fusion attributes on existing nodes and edges
    It does nothing if node uuid and edge uuid is already in the Graph
    """
    def add_graph_to_graph(root, graph):
        # The root will be modified
        nodes = second.get_nodes()
        for node in nodes:
            root.add_node(node)
        edges = second.get_edges()
        for edge in edges:
            root.add_edge(edge)
        return root    
    gt_check_params(root, sideeffect)
    if len(kwargs) == 0:
        raise ValueError("gt_fusion: expected a second graph for the fusion")
    if not GRAPH in kwargs:
        raise ValueError("gt_fusion: expected " + GRAPH + " key in kwargs")
    second = kwargs[GRAPH]
    if type(second) != Graph or second == None:
        raise ValueError("gt_fusion: bad argument (not a graph)")
    if sideeffect:
        return add_graph_to_graph(root, second)
    else:
        g = gt_clone(root)
        return add_graph_to_graph(g, second)


def main():
    print('Please run the unit tests')


if __name__ == "__main__":
    main()
