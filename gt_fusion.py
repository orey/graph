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

def gt_fusion(graph, rootnode, sideeffect=True, **kwargs):
    """
    Fusion two graphs (with options)

    @param graph:      Instance of Graph. Should not be None.
    @param rootnode:   Should be None. To add a node to a Graph, use Graph API.
    @param sideeffect: bool; default is True, which means the resulting
                       graph is 'graph'. If 'sideeffect=False',
                       then the returned graph is a new graph
    @param kwargs:     Expecting: C{graph= the_graph}
                       If no option is provided, the fusion is a simple one.
    @return:           tuple: graph, rootnode. The tuple returned can be
                       reinjected in another graph transformation.

    Warning: gt_fusion does not fusion attributes on existing nodes and edges
    It does nothing if node uuid and edge uuid are already in the Graph
    """
    def add_graph_to_graph(root, second):
        # The root will be modified
        nodes = second.get_nodes()
        for node in nodes:
            root.add_node(node)
        edges = second.get_edges()
        for edge in edges:
            root.add_edge(edge)
        return root    
    # Start
    gt_check_params(graph, rootnode, sideeffect)
    if len(kwargs) == 0:
        raise ValueError("gt_fusion: expected a second graph for the fusion")
    if GRAPH in kwargs and isinstance(kwargs[GRAPH], Graph):
        second = kwargs[GRAPH]
        if sideeffect:
            return add_graph_to_graph(graph, second)
        else:
            g = gt_clone(graph)
            return add_graph_to_graph(g, second)
    else:
        raise ValueError("gt_fusion: expected " + GRAPH + " key in kwargs")


def main():
    print('Please run the unit tests')


if __name__ == "__main__":
    main()
