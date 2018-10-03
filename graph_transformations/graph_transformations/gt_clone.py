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

DOMAIN = 'TIMELINE'
TYPE   = 'PREVIOUS'
NAME   = 'CLONE'
UUID   = 'uuid'
CLONED = '_cloned'
OPTION = 'option'
CHAIN  = 'chain'
SAME   = 'same'

def gt_clone(graph, rootnode, sideeffect=False, **kwargs):
    """
    Clones a node or a graph

    This graph transformation implements several options.

        1. Basic cloning Node
            C{g_none, new = gt_clone(None, n)}

            'g_none' will stay None. 'new' is totally separated from 'n'. 

        2. Cloning node with chaining
            C{g, new = gt_clone(None, n, False, option='chain')}

            Creates a subgraph with the original node 'n' and a new one 'new'
            connected by an edge in domain. Note that 'new' is provided to be
            immediately accessible. Note also that we clone in the past.

            'rootnode -PREVIOUS-> new'

        3. Basic Graph clone
            C{new_g, n_none = gt_clone(g, None)}

            Creates a new graph, cloned from the previous one.

        4. Graph cloned inside the same graph with links
            C{new_g, n_none = gt_clone(g, None, option='same')}

            This option creates also BridgeEdge objects inside the graph.

    @param graph:      Instance of Graph or None
    @param rootnode:   Instance of Node or None
    @param sideeffect: bool. This parameter is not used in this GT
    @param kwargs:     Dict. See above for options
    @return:           tuple: graph, rootnode. The tuple returned can be
                       reinjected in another graph transformation
    

    """
    def clone_node(root):
        obj = copy.deepcopy(root)
        obj.attributes[UUID] = uuid.uuid1()
        return obj
    def clone_edge(e, source, target):
        clone = copy.deepcopy(e)
        e.attribues[UUID] = uuid.uuid1()
        e.override_source_target(source, target)
    # Start
    gt_check_params(graph, rootnode, sideeffect)
    # Node case: clone and chain with a DatetimeTrackingEdge edge
    if graph == None:
        if rootnode == None:
            raise ValueError("gt_clone: graph and rootnode arguments are None")
        # Analyze options
        if len(kwargs) == 0:
            # Basic clone
            return None, clone_node(rootnode)
        elif OPTION in kwargs and kwargs[OPTION] == CHAIN:
            obj = clone_node(rootnode)
            edge = DatetimeTrackingEdge(rootnode.get_uuid(),obj.get_uuid(), \
                                    DOMAIN, TYPE)
            g = Graph(NAME)
            g.add_node(rootname)
            g.add_node(obj)
            g.add_edge(edge)
            return g, obj
        else:
            raise ValueError("gt_clone: unrecognized options in cloning Node " \
                             +  str(kwargs))
    # Graph case
    else:
        if len(kwargs) == 0:
            # Clone into a new graph
            name = graph.get_name() + CLONED
            g = Graph(name)
            # table is old_id, new_id, ids being uuid-s
            table = {}
            nodes = graph.get_nodes()
            edges = graph.get_edges()
            for node in nodes:
                new = clone_node(node)
                g.add_node(new)
                table[node.get_uuid()] = new.get_uuid()
            for edge in edges:
                source, target = edge.get_source_target()
                new = clone_edge(edge, table[source], table[target])
                g.add_edge(new)
            return g, None
        elif OPTION in kwargs and kwargs[OPTION] == SAME:
            table = {}
            nodes = graph.get_nodes()
            edges = graph.get_edges()
            for node in nodes:
                new = clone_node(node)
                graph.add(new)
                table[node.get_uuid()] = new.get_uuid()
            for edge in edges:
                source, target = edge.get_source_target()
                new = clone_edge(edge, table[source], table[target])
                graph.add_edge(new)
                bridge = EdgeBridge(edge, new, DOMAIN)
                # Not sure if this will be used
                graph.add_bridgeedge(bridge)
            return graph, None
        else:
            raise ValueError("gt_clone: unrecognized options in cloning Graph " \
                             +  str(kwargs))

    
def main():
    print('Please run the unit tests')


if __name__ == "__main__":
    main()
