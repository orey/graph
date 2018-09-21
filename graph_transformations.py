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

def transform_interface(graph, rootnode, sideeffect, params):
    # Returns graph, rootnode
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
    def remove_fields_from_node(node, sideeffect, lis):
        n = None
        if not sideeffect:
            n = copy.deepcopy(node)
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
    if rootnode != None:
        print("Warning: rootnode provided but not taken into account. Returning None as rootnote")
    output = None
    if sideeffect == False:
        output = copy.deepcopy(graph)
    else:
        output = graph
    nodes = output.get_nodes()
    for n in nodes.values:
        remove_fields_from_node(n, Tue, l)
    return output, None

def test():
    g = Graph("toto")
    g.add_node(Node("test","Part",123,{"age":12, "field":"rheue"}))    
    g.add_node(Node("test","Part",124,{"age":13, "field":"bla"}))    
    g.add_node(Node("test","Part",125,{"age":14, "field":"bli"}))    
    g.add_node(Node("test","Part",126,{"age":15, "field":"blue"}))
    print(g)
    print("-------------")
    n1 = Node("gloups","ECR",2245,{"start":10, "end": 15, "color":"blue"})
    print(n1)
    print(gt_filter(None, n1, False, {GT_ATT:["start","color"]}))
    print(n1)
    print(gt_filter(None, n1, True, {GT_ATT:["start","color"]}))
    print(n1)
    n2 = Node("Perlin","Pimpim",4545,{"start":20, "end": 30, "color":"white"})
    print(gt_filter((gt_filter(None, n2, False, {GT_ATT:['start']})),False,{GT_ATT:['color']}))
    print("-------------")
    

if __name__ == "__main__":
    test()
