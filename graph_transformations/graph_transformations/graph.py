#-------------------------------------------------------------------------------
# Name:        graph.py
# Purpose:     Graph structures in python
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import sys, traceback, copy, uuid, datetime

DB = 'db.graph'

DOMAIN = 'domain'
TYPE   = 'type'
UUID   = 'uuid'

OPTIONS =["directed", "undirected"]

#-------------------------------------------
# Check methods
#-------------------------------------------

def check_strfield(name):
    if not type(name) == str:
        raise TypeError("Field value is not a string: " + str(name))
    if len(name) == 0:
        raise ValueError("Field cannot be a void string")
    return True

def check_intfield(value):
    if not type(value) == int:
        raise TypeError("Field value must be an integer: " + str(value))
    if value <= 0:
        raise ValueError("Field value cannot be null of negative")
    return True

def check_uuidfield(value):
    if not type(value) == uuid.UUID:
        raise TypeError("Field value must be uuid.UUID: " + str(value))
    return True


#-------------------------------------------
# Root, Node, Edge
#-------------------------------------------

class Root():
    def __init__(self, domain, ntype, rest={}):
        self.attributes = {}
        if check_strfield(domain):
            self.attributes[DOMAIN] = domain
        if check_strfield(ntype):
            self.attributes[TYPE] = ntype
        self.attributes[UUID] = uuid.uuid1()
        if not type(rest) == dict:
            raise TypeError("Field value must be a dictionary: " + str(rest))
        if len(rest) == 0:
            return
        else:
            for k in rest.keys():
                if check_strfield(k):
                    if k in [DOMAIN, TYPE, UUID]:
                        raise ValueError("Field name is already reserved: " + k)
                    else:
                        self.attributes[k] = rest[k]
    def add_attribute(self, pair):
        #-- Pair is a list [key, value]
        if pair == None or pair == []:
            raise ValueError("Argument canot be null")
        elif not type(pair) == list:
            raise TypeError("Field should be a pair: " + str(pair))
        elif len(pair) != 2:
            raise ValueError("List length should be 2")
        elif not type(pair[0]) == str:
            raise TypeError("First item of the list should be a string: " + str(pair[0]))
        elif pair[0] == "":
            raise ValueError("First item of the list cannot be a null string")
        else:
            self.attributes[pair[0]] = pair[1]
    def get_descr(self):
        chain = ""
        for k in self.attributes.keys():
            chain += k + ":" + str(self.attributes[k]) + "|"
        return chain   
    def get_id(self):
        return self.attributes[UUID].int
    def __hash__(self):
        return self.attributes[UUID].int
    def __eq__(self, other):
        if other == None:
            return False
        if other.get_id() == self.attributes[UUID].int:
            return True
        else:
            return False
    def get_attributes(self):
        return self.attributes
    def get_uuid(self):
        return self.attributes[UUID]
    #def clone(self):
    #    # This will regenerate a UUID 
    #    obj = copy.deepcopy(self)
    #    obj.attributes[FIELDS[2]] = uuid.uuid1()
    #    return obj
    def get_type(self):
        return self.attributes[TYPE]
    def override_uuid(self, uuid):
        self.attributes[UUID] = uuid

class Node(Root):
    def __init__(self, domain, ntype, rest={}):
        super().__init__(domain, ntype, rest)
    def __repr__(self):
        return "\nNode||" + super().get_descr() + '|'
        
class Edge(Root):
    '''
    Edge can be used for directed and undirected graphs.
    source and target are here to define the direction of the edge but
    the edge being in the graph structure, it could be without source and
    target
    '''
    def __init__(self, sourceUUID, targetUUID, domain, ntype, rest={}):
        super().__init__(domain, ntype, rest)
        if check_uuidfield(sourceUUID):
            self.source = sourceUUID
        if check_uuidfield(targetUUID):
            self.target = targetUUID
        #-- the graph will have to validate the edge in the graph
        self.invalid = True
    def is_invalid(self):
        return self.invalid
    def validate(self):
        self.invalid = False
    def __repr__(self):
        return ">>Edge||SourceID:" + str(self.source.int) + "|TargetID:" \
               + str(self.target.int) + '||' + super().get_descr() + '|'
    def get_source_target(self):
        return self.source, self.target
    def override_source_target(self, source, target):
        self.source = source
        self.target = target

#-------------------------------------------
# Graph
# TODO remove clone method
#-------------------------------------------
        
class Graph():
    '''
    A graph is a set of nodes, a set of edges and a neighbor tree based on ids
    Warning: the indexing is based on uuid.int
    graph: {ID_Node1 : { ID_Node2 : ID_Edge1, ID_Node3 : ID_Edge 2}}
    graph is used for optimization of neighbourhood
    '''
    def __init__(self, name):
        self.graph = {}
        if check_strfield(name):
            self.name = name
        self.nodes = {}
        self.edges = {}
        self.uuid = uuid.uuid1()
        self.edgebridges = {}
    def get_name():
        return self.name
    def __repr__(self):
        chain = "Graph||ID=" + str(self.uuid.int) + '\n'
        chain += "||Nodes|" + self.nodes.__repr__() + '\n'
        chain += "||Edges|" + self.edges.__repr__() + '\n'
        return chain
    def add_node(self, node):
        if not type(node) == Node:
            raise TypeError("Graph.add_node: Expecting Node in graph")
        if node == None:
            raise ValueError("Graph.add_node: ode cannot be null")
        # Indexing is done on uuid.int and not on uuid
        id = node.get_id()
        if not id in self.nodes:
            self.nodes[node.get_id()] = node
            # There cannot be edges because the node is new in the graph
            self.graph[node.get_id()] = {}
        else:
            print("Info: node is already in the graph. No node added.")
    def get_node_by_id(self, id):
        if type(id) == int and id > 0:
            return self.nodes[id]
        else:
            return None
    def add_edge(self, edge):
        if not isinstance(edge, Edge):
            raise TypeError("Expected Edge in graph. Type is:", type(edge))
        if edge == None:
            raise ValueError("Edge cannot be null")
        id = edge.get_id()
        if not id in self.edges:
            # check the ref nodes are existing
            source, target = edge.get_source_target()
            if source.int in self.nodes and target.int in self.nodes:
                # adding edge in edges
                self.edges[id] = edge
                # enriching graph neighboorhood
                self.graph[source.int][target.int] = id
                self.graph[target.int][source.int] = id
            else:
                raise ValueError("One of the referenced nodes " + \
                                 "is not in the graph", source.int, target.int)
        else:
            print("Info: Edge already existing. Nothing done.")
    def graphrep(self):
        for k, v in self.graph.items():
            print('--', k)
            for i, j in v.items():
                print('----', j, '->>-', i)
    def clone(self):
        cl = copy.deepcopy(self)
        cl.uuid = uuid.uuid1()
        return cl
    def get_nodes(self):
        return self.nodes.values()
    def get_edges(self):
        return self.edges.values()
    def add_bridgeedge(self, bridge):
        if bridge.get_uuid().int not in self.edgebridges:
            self.edgebridges[bridge.get_uuid().int] = bridge
        else:
            print("Info: bridge always in the graph.", bridge)

#-------------------------------------------
# Utilities for Graph Transformations
# prefix is gt_*
#-------------------------------------------

def gt_interface(graph, rootnode, sideeffect, **kwargs):
    '''
    graph is a Graph
    rootnode is a Node
    Returns a tuple "graph, rootnode"
    To compose use: g(*f(graph, rootnode, sideeffect, args), sideeffect2, args2)
    '''
    pass

def gt_check_params(graph, rootnode, sideeffect):
    """
    graph or rootnode can be None
    """
    if graph != None:
        if not isinstance(graph, Graph):
            raise TypeError("gt_check_params: graph should be a Graph")
    if rootnode != None:
        if not isinstance(rootnode, Node):
            raise TypeError("gt_check_params: rootnode should be a Node")
    if type(sideeffect) != bool:
        raise TypeError("gt_check_params: sideeffect should be bool")

#-------------------------------------------
# Util sub classes
#-------------------------------------------

class DatetimeTrackingEdge(Edge):
    def __init__(self, sourceUUID, targetUUID, domain, etype):
        super().__init__(sourceUUID, targetUUID, domain, etype, \
                       {"datetime":datetime.datetime.now()})

class EdgeBridge(Edge):
    """
    Warning, this is an unconventional concept. 
    """
    def __init__(self, e_source, e_target, domain):
        super().__init__(e_source.get_uuid(), e_target.get_uuid(), domain, \
                         "PREVIOUS", {"datetime":datetime.datetime.now()})
        self.e_source = e_source
        self.e_target = e_target
    def __repr__(self):
        return ">>EdgePath||SourceID:" + str(self.source.int) + "|TargetID:" \
               + str(self.target.int) + '||' + super().get_descr() + '|'



#-------------------------------------------
# Main
#-------------------------------------------
        
def main():
    print("Please, run the unit tests")

if __name__ == "__main__":
    main()
