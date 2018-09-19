import sys, traceback, pickle

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

class Root():
    def __init__(self, domain, ntype, ID, rest={}):
        self.attributes = {}
        if check_strfield(domain):
            self.attributes[FIELDS[0]] = domain
        if check_strfield(ntype):
            self.attributes[FIELDS[1]] = ntype
        if check_intfield(ID):
            self.attributes[FIELDS[2]] = ID
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
            chain += k + ": " + str(self.attributes[k]) + "; "
        return chain   
    def get_id(self):
        return self.attributes[FIELDS[2]]
    def __hash__(self):
        return self.attributes[FIELDS[2]]
    def __eq__(self, other):
        if other == None:
            return False
        if other.get_id() == self.attributes[FIELDS[2]]:
            return True
        else:
            return False
    

class Node(Root):
    def __init__(self, domain, ntype, ID, rest={}):
        super().__init__(domain, ntype, ID, rest)
    def __repr__(self):
        return "Node - " + super().get_descr()
        
class Edge(Root):
    '''
    Edge can be used for directed and undirected graphs
    '''
    def __init__(self, sourceID, targetID, domain, ntype, ID, rest={}):
        super().__init__(domain, ntype, ID, rest)
        if check_intfield(sourceID):
            self.source = sourceID
        if check_intfield(targetID):
            self.target = targetID
        #-- someone has to validate the edge in the graph
        self.invalid = True
    def is_invalid(self):
        return self.invalid
    def validate(self):
        self.invalid = False
    def __repr__(self):
        return "Edge - SourceID = " + str(self.source) + "; TargetID = " \
               + str(self.target) + "; " + super().get_descr()
        
class Graph():
    '''
    Voisinage oriented structure: {Node1 : { Node2 : Edge1, Node3 : Edge 2}}
    We can have a multigraph.    
    '''
    def __init__(self, name, option=OPTIONS[0]):
        self.graph = {}
        if check_strfield(name):
            self.name = name
        if option == OPTIONS[1]:
            self.option = option
        else:
            self.option = OPTIONS[0]
    def __repr__(self):
        chain = ""
        if len(self.graph) == 0:
            return "Graph is empty"
        for k, v in self.graph.items():
            chain += k.__repr__() + '\n'
            for i, j in v.values():
                chain += j.__repr__()
        return chain
    def add_node(self, node):
        if not type(node) == Node:
            raise TypeError("Expecting Node in graph")
        if node == None:
            raise ValueError("Node cannot be null")
        #-- Node has __hash__ and __eq__ methods
        if not node in self.graph:
            self.graph[node] = {}
        else:
            print("Warning: node is already in the graph")

        
def test():
    mfile = open(DB,'wb')
    try:
        pickle.dump(Node("test domain 1","ECO",1), mfile)
        pickle.dump(Node("test domain 1","ECO",2), mfile)
        pickle.dump(Node("test domain 1","ECO",3), mfile)
        pickle.dump(Edge(2, 1, "meca", "LINK", 4, {"rototo" : 12, "camion" : "vert"}), mfile)
        g = Graph("toto")
        g.add_node(Node("domain12","Part",125,{"length": 25, "width": 120, "captainage": "YGFY"}))
        g.add_node(Node("domain13","Part",89,{"length": 10, "width": 80, "captainage": "WTF"}))
        pickle.dump(g, mfile)
    except Exception as e:
        print(e)
        print("Exception caught: ", type(e), e.args)
        traceback.print_exc(file=sys.stdout)
        mfile.close()
        exit(0)
    mfile.close()

    mfile = open(DB, 'rb')
    objects = []
    count = 0
    try:
        while True:
            objects.append(pickle.load(mfile))
            count += 1
    except EOFError:
        print("Info: end of file reached. Found ", count, "items")
    for item in objects:
        print(item)
    mfile.close()
    


if __name__ == "__main__":
    test()
