#-------------------------------------------------------------------------------
# Name:        gt_filter_attributes.py
# Purpose:     Filters attributes on single Node or Graph
#              Proposes a way to filter on types in the case of the graph
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
# TODO : manage new numbering systems for nodes in mode without side effects

import copy

from graph import *
from gt_clone import *


GT_ATT = "attributes"
GT_APPLIC = "applicability"

     
def gt_filter_attributes(root, sideeffect, **kwargs):
    '''
    This graph transformation eleminates useless attributes from a Node
    or from a whole graph.
    Expecting **kwarks: attributes=["toto", "titi", "tutu"]

    Three options are managed:
    1. graph = None, rootnode != None => filters the rootnode
    2. graph != None, rootnode = None => filters the whole nodes matching in the graph
    3. graph != None, rootnode = None, params = {"applicability" : "TYPE"}
    => filters only the Nodes with "TYPE" type
    '''
    # Inner function
    def remove_fields_from_node(node, sideeffect, lis):        
        n = None
        if not sideeffect:
            n = gt_clone(node, option='basic')
        else:
            n = node
        atts = n.get_attributes()
        for k in lis:
            del atts[k]
        return n
    # Beginning of main function
    gt_check_params(root, sideeffect)
    # Expecting: attributes=["toto", "titi", "tutu"] in **kwargs
    l = []
    if GT_ATT in kwargs:
        l = kwargs[GT_ATT]
        if type(l) != list:
            raise TypeError("Expecting list of fields in params")
    else:
        raise ValueError("Expecting key to be", GT_ATT)
    # Basic node case
    if type(root) == Node:
        return remove_fields_from_node(root, sideeffect, l)
    # Graph case
    # Expecting applicability=["type1", "type2"] in case of type restrictions
    restrict = False
    la = []
    if GT_APPLIC in kwargs:
        la = kwargs[GT_APPLIC]
        if type(la) != list:
            raise TypeError("Expecting a list of types after applicability key")
        if len(la) == 0:
            print("Warning: List of applicable types is void")
        else:
            restrict = True
    output = None
    if sideeffect == False:
        # TODO: create the clone graph function
        output = copy.deepcopy(root)
    else:
        output = root
    nodes = output.get_nodes()
    if not retrict:
        for n in nodes.values:
            remove_fields_from_node(n, True, l)
    else:
        for n in nodes.values:
            if n.get_type() in la: 
                remove_fields_from_node(n, True, l)
    return output

def main():
    print("Please, run the unit tests")

if __name__ == "__main__":
    main()
