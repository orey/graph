# Design principles

## Warning

This is a work in  progress.

## Basic structures

In: graph.py

``Node`` and ``Edge`` structures are inheritating from ``Root`` class:

  *  Their id is a UUID
  *  ``Root`` implements ``__hash__`` and ``__eq__`` based on uuid.int
  *  ``Root`` structure the elements by having:
    *  A ``domain`` attribute
    *  A ``type`` attribute
  * Basically a structure is an attribute dictionary
  * ``Graph`` contains:
    * A dictionary of nodes keyed by their uuid.int
    * A dictionary od edges keyed by their uuid.int
    * A neighborhood structure always in sync:
      * {Id_Node1 {Id_Node2 : Id_Edge12, Id_Node3 : Id_Edge13, ...}}
    * Note: ``add_node`` and ``add_edge`` are not updating nodes and edges that would already exist. The nodes and edges are not touched at all if their ``uuid`` did not change. This is especially true to ``gt_fusion``. Maybe a ``gt_update`` transformation would be required.

## Unitary transformations

All graph transformations (GTs) have:

  * A destructice mode (``sideffect = True``) and a non destructive mode based on ``clone`` approach.
  * A unified interface
    * ``g_output, rootnode_output = gt(g_input, rootnode_input, sideeffect, params)``
    * ``params`` is a ``dict``
  * GTs can be composed: ``g_output, rootnode_output = gt1(*gt2(g_input, rootnode_input, sideeffect, params))``

### Filter GT

Remove void attributes/columns => implemented

### A column is a type indicator

Change type and remove attribute

### A column is a foreign key

Remove attribute and create edge

### Hidden references as labels

Remove attribute and create edge

### Hidden references towards a concept that does not exist

Create the concept and solve the graph

### Snapshot to the past

Create the ``PREVIOUS`` edge

## The problem of graph cloning

It is very simple to do a "rough cloning" operation of a graph: ``h = g.clone()`` with ``clone`` being implemented with ``copy.deepcopy()``.

However, this is not satisfying. We must introduce the notion of "tracking". We'll define a tracking indicator as a comparable sequence of objects that support the ``>`` and ``<`` operators. Thus the tracking objects can be:
  * ``int`` or ``float`` types
  * ``datetime.datetime`` objects
  * Any other object supporting comparisons.

When cloned, a graph will attach all nodes to their ancestor: the node to node ancestor edge is a standard edge.

However, there is an option to also track edges to edges connectivity.


## TODO

  * Who manages the position semantics?
  * Materialize subgraphs from within a graph?
  * Create specific edges for inter-domain relationships?

