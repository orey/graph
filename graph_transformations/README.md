# READ ME

Some infos about the package.

## Warning

This is a work in  progress.

## graph.py

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

## Features of graph transformations

All graph transformations (GTs) have a common interface:

```
def gt_interface(graph, rootnode, sideeffect, **kwargs):

```

This interface:

  * Returns a tuple ``graph, rootnode``, in which elements can be ``None``;
  * All graph transformations can propose a "destructive" mode (``sideffect = True``) and a "non destructive" mode based on a cloning approach;
  * Graph transformations can be composed: ``g_output, rootnode_output = gt1(*gt2(g_input, rootnode_input, sideeffect, params))`` (* being used to transform the tuple into a list of arguments).

### Why having a tuple in inbound and outbound interface of a graph transformation?

A graph can be seen in two perspectives:

  1. A graph,
  1. A root node being the "attachment point" of the graph.

Sometimes, we need both information.

A graph transformation like ``gt_clone`` can be applied both to a graph (with options) or to a single ``Node``, in a mode with ou without side effects. With the option of cloning ``Node N`` inside the same ``Graph``, we can choose the option of linking the cloned node to the old one with a ``PREVIOUS`` relationship. In that case, the ``gt_clone`` graph transformation will return a graph whereas the input was a simple node. If a graph was provided with a node, with the appropriate option, the graph will be enriched by the subgraph created by the transformation.

Another use of this strange API is to tranform graphs while getting a "cursor" of the node that is interesting for us. The graph transformation can return the graph, but the node returned could be used to launch another graph transformation from this rootnode.

## Basic graph transformations

We believe that in the world of graphs, there are a limited number of graph transformations that can transform all graphs into whatever graph. This is more a philosophical statement than a real proof, but basic graph transformations can act as the basic "verbs" of a peculiar sort of DSL (domain specific language).

We will implement all those "basic" transformations and propose convenient ways to compose them in order to make more advanced graph transformations.

For a research background around those concepts, please refer to:

  * https://orey.github.io/papers/graph/first-article/
  * https://orey.github.io/papers/graph/staf-icgt2018/

### gt_filter_attributes

A common problem in graph transformations is that the node may have too many attributes, most of them being or ``None``, or "" or a random value.

This graph transformation removes the useless fields.

### gt_clone

This graph transformation:

  * Clones a node and returns a node or a graph;
  * Clones a graph (destructive and non destructive modes).

Note on graph cloning while staying in the same graph:

  * The business rules can be farely simple:
    * All nodes are cloned.
    * They are attached to their clone with the pattern ``original_node -PREVIOUS-> cloned_node``. In a way, the nodes are cloned "in the past": this is very important because it preserves the graph knowledge structure.
    * All edges are cloned.
    * The new edges are connected to old edges with the same pattern than nodes, through the concept of ``EdgePath``, an "edge between edges". This is a new concept (not really) that is really disturbing because it is not strictly speaking a graph concept, but this will be very useful for tracking and for semantic analysis. Note that it looks like web semantics hierarchy of verbs.

### gt_fusion

Thi graph transformation fusions two graphs in a destructive or not destructive mode.

### Other basic graph transformations to impelement

#### A column is a type indicator

Change type and remove attribute

#### A column is a foreign key

Remove attribute and create edge

#### Hidden references as labels

Remove attribute and create edge

#### Hidden references towards a concept that does not exist

Create the concept and solve the graph

#### Snapshot to the past

Create the ``PREVIOUS`` edge

#### A concept split on several nodes

Gather the concept in one single node and rebuild the graph topology.

## TODO

  * Who manages the position semantics?
  * Materialize subgraphs from within a graph?
  * Create specific edges for inter-domain relationships?

