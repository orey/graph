#-------------------------------------------------------------------------------
# Name:        gt_foreign_key.py
# Purpose:     Managing foreign keys graph transformation
#
# Author:      O. Rey
#
# Created:     October 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import copy, uuid
from graph import *

SOURCEATT  = "source_attribute"
TARGETTYPE = "target_type"
TARGETATT  = "target_attribute"
RELTYPE    = "rel_type"

def gt_foreign_key(graph, rootnode, sideeffect=False, **kwargs):
    """
    Manages foreign key and creates an edge instead.

    This graph transformation transforms all source type elements defined
    by "rootnode" type in the graph. It needs 3 arguments to work:

      1. The source attribute where to find the IDs: C{source_attribute = "attribute"},
      2. The target type: C{target_type = "type"}
      3. The target attribute where to find the IDs: C{target_attribute = "attribute"}
      4. The type of relationships: C{rel_type = "type_name"}

    The attributes are removed from the source objet and from the target object
    and transformed into instances of relationships with the proper name.

    This graph transformation is well adapted to nodes that just come from
    a CSV import of relational data.

    @param graph:      Instance of Graph or None
    @param rootnode:   Instance of Node or None
    @param sideeffect: bool. This parameter is not used in this GT
    @param kwargs:     Dict. See above for options
    @return:           tuple: graph, rootnode. The tuple returned can be
                       reinjected in another graph transformation

    """
    def get_value_in_args(key, dict):
        if type(key) != str:
            raise TypeError("gt_foreign_key: key must be a string")
        if not key in dict:
            raise ValueError("gt_foreign_key: expected " + key + " in arguments")
        value = dict[key]
        if type(value) != str: 
            raise TypeError("gt_foreign_key: value should be a string")
        return value
    # Start
    gt_check_params(graph, rootnode, sideeffect)
    if graph == None:
        raise ValueError("gt_foreign_key: graph should not be None")
    if rootnode == None:
        raise ValueError("gt_foreign_key: rootnode should not be None")
    sourcetype = rootnode.get_type()
    if kwargs == None or len(kwargs) == 0 or type(kwargs) != dict:
        raise ValueError("gt_foreign_key: Expecting arguments in **kwargs")
    sourceatt  = get_value_in_args(SOURCEATT)
    # test the presence of attribute in the structure
    
    targettype = get_value_in_args(TARGETTYPE)
    targetatt  = get_value_in_args(TARGETATT)
    rel_type   = get_value_in_args(RELTYPE)
    snodes = graph.get_nodes_by_type(sourcetype)
    tnodes = graph.get_nodes_by_type(targettype)
    for n in snodes:
        
        
        
            
        
        
