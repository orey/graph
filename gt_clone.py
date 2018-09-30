#-------------------------------------------------------------------------------
# Name:        gt_clone.py
# Purpose:     Cloning graph transformation
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import copy, uuid
from graph import *

DOMAIN = "TIMELINE"
TYPE   = "PREVIOUS"
NAME   = "CLONE"
UUID   = "uuid"
CLONED = "_cloned"
OPTION = "option"
BASIC  = 'basic'

def gt_clone(root, sideeffect=True, **kwargs):
    """
    Can clone a node and a graph.
    The is a basic mode for node cloning:
    clone = gt_clone(node, option="basic")
    """
    def clone_node(root):
        obj = copy.deepcopy(root)
        obj.attributes[UUID] = uuid.uuid1()
        return obj
    def clone_edge(e, source, target):
        clone = copy.deepcopy(e)
        e.attribues[UUID] = uuid.uuid1()
        e.override_source_target(source, target)
    gt_check_params(root, False)
    # Node case: clone and chain with a DatetimeTracking edge
    if type(root) == Node:
        if len(kwargs) != 0:
            if OPTION in kwargs and kwargs[OPTION] == BASIC:
                return clone_node(root)
        obj = clone_node(root)
        edge = DatetimeTracking(root.get_uuid(),obj.get_uuid(), DOMAIN, TYPE)
        g = Graph(NAME)
        g.add_node(root)
        g.add_node(obj)
        g.add_edge(edge)
        return g
    # Graph case
    else:
        name = root.get_name() + CLONED
        g = Graph(name)
        # table is old_id, new_id, ids being uuid-s
        table = {}
        nodes = root.get_nodes()
        edges = root.get_edges()
        for node in nodes:
            new = clone_node(node)
            g.add_node(new)
            table[node.get_uuid()] = new.get_uuid()
        for edge in edges:
            source, target = edge.get_source_target()
            new = clone_edge(edge, table[source], table[target])
            g.add_edge(new)
        return g

    
def main():
    print('Please run the unit tests')


if __name__ == "__main__":
    main()
