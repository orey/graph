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


ATTRIBUTES    = "attributes"
APPLICABILITY = "applicability"

     
def gt_filter_attributes(graph, rootnode, sideeffect=True, **kwargs):
    '''
    This graph transformation eleminates useless attributes from a Node
    or from a whole graph.

    @param graph:      Instance of Graph. Can be None if 'rootnode' is not.
    @param rootnode:   Instance of Node. Can be None if 'graph' is not.
    @param sideeffect: bool; default is True.
                       If False, a copy is returned.
    @param kwargs:     Expecting: C{attributes=["att_name1", "att_name2"]}
                       as a mandatory option.
                       Another option, in the case of graph filtering, is
                       the restriction to some types only. When filtering a
                       graph, the filtering can be restricted to a list of
                       Node types by using the following option:
                       C{applicability=["type1", "type2"]}
                       Types in the list are strings, corresponding to the value
                       of the 'type' attribute in Node and Edge classes.
    @return:           tuple: graph, rootnode. The tuple returned can be
                       reinjected in another graph transformation.
    '''
    # Inner function
    def remove_fields_from_node(node, sideeffect, lis):        
        n = None
        if not sideeffect:
            g, n = gt_clone(None, node)
        else:
            n = node
        atts = n.get_attributes()
        for k in lis:
            del atts[k]
        return n
    # Start
    gt_check_params(graph, rootnode, sideeffect)
    # Expecting: attributes=["toto", "titi", "tutu"] in **kwargs
    l = []
    if ATTRIBUTES not in kwargs or type(kwargs[ATTRIBUTES]) != list:
        raise TypeError("gt_filter_attributes: attributes not provided")
    l = kwargs[ATTRIBUTES]
    # Case on Node
    if graph == None and isinstance(rootnode,Node):
        return None, remove_fields_from_node(rootnode, sideeffect, l)
    # Case of Graph
    if instanceof(graph, Graph):
        restrict = False
        la = []
        # In case of restriction, get types
        if APPLICABILITY in kwargs:
            la = kwargs[APPLICABILITY]
            if type(la) != list:
                raise TypeError("gt_filter_attributes: Expecting a list " + \
                                "of types after applicability key")
        if len(la) == 0:
            print("Warning: List of applicable types is void")
        else:
            restrict = True
        output = None
        # See if we have to create a new graph
        if sideeffect == False:
            output = gt_clone(graph, False) # Default option, could be challenged
        else:
            output = graph
        nodes = output.get_nodes()
        if not retrict:
            for n in nodes.values:
                remove_fields_from_node(n, True, l)
        else:
            for n in nodes.values:
                if n.get_type() in la:
                    remove_fields_from_node(n, True, l)
        return output, None
    else:
        raise TypeError("gt_filter_attributes: Expected a graph")


def main():
    print("Please, run the unit tests")


if __name__ == "__main__":
    main()
