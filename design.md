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
    * A neighborhoud structure always in sync:
      * {Id_Node1 {IdNode2 : Id_Edge12, IdNode3 : IdEdge13, ...}}

## Unitary transformations

All graph transformations (GTs) have:

  * A destructice mode (``sideffect = True``) and a non destructive mode based on ``clone`` approach.
  * A unified interface
    * ``g_output, rootnode_output = gt(g_input, rootnode_input, sideeffect, params)``
    * ``params`` is a ``dict``
  * GTs can be composed: ``g_output, rootnode_output = gt1(*gt2(g_input, rootnode_input, sideeffect, params)``

### Filter GT

Remove void attributes/columns

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

## TODO

  * Who manages the position semantics?
  * Materialize subgraphs from within a graph?
  * Create specific edges for inter-domain relationships?

