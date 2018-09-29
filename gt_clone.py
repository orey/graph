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

def gt_clone(root, **kwargs):
    def clone_node(root):
        obj = copy.deepcopy(root)
        obj.attributes["uuid"] = uuid.uuid1()
        return obj
    gt_check_params(root, False)
    # Node case: clone and chain with a DatetimeTracking edge
    if type(root) == Node:
        obj = clone_node(root)
        edge = DatetimeTracking(root.get_uuid(),obj.get_uuid(), DOMAIN, TYPE)
        g = Graph(NAME)
        g.add_node(root)
        g.add_node(obj)
        g.add_edge(edge)
        return g
    # Graph case
    else:
        raise TypeError("Graph clone not implemented")
        
    
def main():
    print('Please run the unit tests')


if __name__ == "__main__":
    main()
