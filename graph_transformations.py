#-------------------------------------------------------------------------------
# Name:        graph_transformations.py
# Purpose:     Basic graph transformations
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
# TODO : manage new numbering systems for nodes in mode without side effects

from graph import *
import copy

GT_ATT = "attributes"
GT_APPLIC = "applicability"

def graph_transformation_interface(graph, rootnode, sideeffect, params):
    '''
    Returns tuple graph, rootnode
    To compose use: g(*f, side_effect, params)
    '''
    pass

def check_params(graph, rootnode, sideeffect, params):
    if graph != None and type(graph) != Graph:
        raise TypeError("Expecting first parameter to be a Graph")
    if rootnode != None and type(rootnode) != Node:
        raise TypeError("Expecting second parameter to be a Node")
    if type(sideeffect) != bool:
        raise TypeError("Expecting third parameter to be a boolean")
    if type(params) != dict:
        raise TypeError("Expecting fourth parameter to be a dictionary")
     
def gt_filter(graph, rootnode, sideeffect, params):
    '''
    This graph transformation eleminates useless attributes from a Node
    or from a whole graph.
    Expecting params = {"attributes" : ["toto", "titi", "tutu"]}
    Three options are managed:
    1. graph = None, rootnode != None => filters the rootnode
    2. graph != None, rootnode = None => filters the whole nodes matching in the graph
    3. graph != None, rootnode = None, params = {"applicability" : "TYPE"}
    => filters only the Nodes with "TYPE" type
    '''
    def remove_fields_from_node(node, sideeffect, lis):
        n = None
        if not sideeffect:
            n = node.clone()
        else:
            n = node
        atts = n.get_attributes()
        for k in lis:
            del atts[k]
        return n
    check_params(graph, rootnode, sideeffect, params)
    # Expecting: params = {"attributes" : ["toto", "titi", "tutu"]}
    l = []
    if GT_ATT in params:
        l = params[GT_ATT]
        if type(l) != list:
            raise TypeError("Expecting list of fields in params")
    else:
        raise ValueError("Expecting key to be", GT_ATT)
    # Basic node case
    if graph == None:
        return None, remove_fields_from_node(rootnode, sideeffect, l)
    # Graph case
    # expecting {"applicability" : ["type1", "type2] } for type restrictions
    restrict = False
    la = []
    if GT_APPLIC in params:
        la = params[GT_APPLIC]
        if type(la) != list:
            raise TypeError("Expecting a list of types after applicability key")
        if len(la) == 0:
            print("Warning: List of applicable types is void")
        else:
            restrict = True
    output = None
    if sideeffect == False:
        # TODO: create the clone graph function
        output = copy.deepcopy(graph)
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

#def gt_changetype(


def main():
    print("Please, run the unit tests")

if __name__ == "__main__":
    main()
