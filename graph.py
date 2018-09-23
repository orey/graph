#-------------------------------------------------------------------------------
# Name:        graph.py
# Purpose:     Graph structures in python
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import sys, traceback, copy, uuid

DB = 'db.graph'

FIELDS = ["domain", "type", "ID"]
OPTIONS =["directed", "undirected"]

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

class Root():
    def __init__(self, domain, ntype, rest={}):
        self.attributes = {}
        if check_strfield(domain):
            self.attributes[FIELDS[0]] = domain
        if check_strfield(ntype):
            self.attributes[FIELDS[1]] = ntype
        self.attributes[FIELDS[2]] = uuid.uuid1()
        if not type(rest) == dict:
            raise TypeError("Field value must be a dictionary: " + str(rest))
        if len(rest) == 0:
            return
        else:
            for k in rest.keys():
                if check_strfield(k):
                    if k in FIELDS:
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
        return self.attributes[FIELDS[2]].int
    def __hash__(self):
        return self.attributes[FIELDS[2]].int
    def __eq__(self, other):
        if other == None:
            return False
        if other.get_id() == self.attributes[FIELDS[2]].int:
            return True
        else:
            return False
    def get_attributes(self):
        return self.attributes
    def get_uuid(self):
        return self.attributes[FIELDS[2]]
    def clone(self):
        # This will regenerate a UUID 
        obj = copy.deepcopy(self)
        obj.attributes[FIELDS[2]] = uuid.uuid1()
        return obj
    def get_type(self):
        return self.attributes[FIELDS[1]]

class Node(Root):
    def __init__(self, domain, ntype, rest={}):
        super().__init__(domain, ntype, rest)
    def __repr__(self):
        return "Node||" + super().get_descr() + '|'
        
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
        return "Edge||SourceID:" + str(self.source.int) + "|TargetID:" \
               + str(self.target.int) + super().get_descr() + '|'
    def get_source_target(self):
        return self.source, self.target
        
class Graph():
    '''
    A graph is a set of nodes, a set of edges and a neighbor tree based on ids
    Warning: the indexing is based on uuid.int
    Voisinage: {ID_Node1 : { ID_Node2 : ID_Edge1, ID_Node3 : ID_Edge 2}}
    Voisinage is used for opt
    We can have a multigraph.  
    '''
    def __init__(self, name):
        self.graph = {}
        if check_strfield(name):
            self.name = name
        self.nodes = {}
        self.edges = {}
        self.uuid = uuid.uuid1()
    def __repr__(self):
        chain = "Graph||ID=" + str(uuid.int) + '\n'
        chain += "||Nodes|" + self.nodes.__repr__() + '\n'
        chain += "||Edges|" + self.edges.__repr__() + '\n'
        return chain
    def add_node(self, node):
        if not type(node) == Node:
            raise TypeError("Expecting Node in graph")
        if node == None:
            raise ValueError("Node cannot be null")
        # Indexing is done on uuid.int and not on uuid
        id = node.get_id()
        if not id in self.nodes:
            self.nodes[node.get_id()] = node
            # There cannot be edges because the node is new in the graph
            self.graph[node.get_id()] = {}
        else:
            print("Warning: node is already in the graph")
    def get_node_by_id(self, id):
        if type(id) == int and id > 0:
            return self.nodes[id]
        else:
            return None
    def voisinage(self, source, target, id):
        # assuming source and target are in the graph
        self.graph[source][target] = id
        self.graph[target][source] = id
    def add_edge(self, edge):
        if not type(edge) == Edge:
            raise TypeError("Expected Edge in graph")
        if edge == None:
            raise ValueError("Edge cannot be null")
        id = edge.get_id()
        if not id in self.edges:
            # check the ref nodes are existing
            source, target = edge.get_source_target()
            if source.int in self.nodes and target.int in self.nodes:
                self.edges[id] = edge
                self.voisinage(source.int, target.int, id)
            else:
                raise ValueError("One of the referenced nodes " + \
                                 "is not in the graph", source.int, target.int)
        else:
            print("Edge already existing")
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
        return self.nodes
        
        
def main():
    print("Please, run the unit tests")

if __name__ == "__main__":
    main()
