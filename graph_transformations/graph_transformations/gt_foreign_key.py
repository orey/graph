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

ATTNAME = "attribute_name"
TYPE    = "type"

def gt_foreign_key(graph, rootnode, sideeffect=False, **kwargs):
    """
    Manages foreign key and creates an edge instead. If id(B) is an
    attribute of A, we will have A -attribute_name-> B. This implies
    the relationships are the other way around in case of list.

    C{**kwargs} should be:

        1. C{attribute_name="name"} This means that the attribute name
        is the name of the type.
        2. C{attribute_name="name", type=Type}

    @param graph:      Instance of Graph or None
    @param rootnode:   Instance of Node or None
    @param sideeffect: bool. This parameter is not used in this GT
    @param kwargs:     Dict. See above for options
    @return:           tuple: graph, rootnode. The tuple returned can be
                       reinjected in another graph transformation

    """
    # Start
    gt_check_params(graph, rootnode, sideeffect)
    if kwargs == None or len(kwargs) == 0 or type(kwargs) != dict:
        raise ValueError("gt_foreign_key: Expecting arguments in **kwargs")
    attname = ""
    targettype = ""
    if not ATTNAME in kwargs:
        raise ValueError("gt_foreign_key: Expected " + ATTNAME + " in **kwargs")
    attname = kwargs[ATTNAME]
    if type(attname) != str:
        raise ValueError("gt_foreign_key: Expected string for " + ATTNAME)
    if TYPE in kwargs:
        targettype = kwargs[TYPE]
        # type must be a str
        if type(targettype) != str:
            raise TypeError("gt_foreign_key: expected string as type descriptor")
    else:
        targettype = attname
    # Continue here by the real transformation
        
            
        
        
