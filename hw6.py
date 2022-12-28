"""
COMP 614
Homework 6: DFS + PageRank
"""

import comp614_module6


def bfs_dfs(graph, start_node, rac_class):
    """
    Performs a breadth-first search on graph starting at the given node.
    Returns a two-element tuple containing a dictionary mapping each visited
    node to its distance from the start node and a dictionary mapping each
    visited node to its parent node.
    """
    parent = {}
    if rac_class == comp614_module6.Queue:
        # Initialize all data structures
        queue = comp614_module6.Queue()
        dist = {}

        # Initialize distances and parents; no nodes have been visited yet
        for node in graph.nodes():
            dist[node] = float("inf")
            parent[node] = None

        # Initialize start node's distance to 0
        dist[start_node] = 0
        queue.push(start_node)

        # Continue as long as there are new reachable nodes
        while queue:
            node = queue.pop()
            nbrs = graph.get_neighbors(node)

            for nbr in nbrs:
                # Only update neighbors that have not been seen before
                if dist[nbr] == float('inf'):
                    dist[nbr] = dist[node] + 1
                    parent[nbr] = node
                    queue.push(nbr)
        return parent

    if rac_class == comp614_module6.Stack:
        stack = comp614_module6.Stack()
        # dump records node that has been dumped from the stack
        dumped = []

        # initialize all nodes' parent to be None
        for node in graph.nodes():
            parent[node] = None
        # push the first node in stack
        stack.push(start_node)

        while stack:
            node = stack.pop()
            dumped.append(node)
            nbrs = graph.get_neighbors(node)

            for nbr in nbrs:
                # only update neighbors that have not been seen before
                if parent[nbr] is None and nbr not in dumped:
                    parent[nbr] = node
                    stack.push(nbr)
        return parent
    return parent


# print(bfs_dfs(comp614_module6.file_to_graph('test0.txt'), 'A', comp614_module6.Queue))
# print(bfs_dfs(comp614_module6.file_to_graph('test0.txt'), 'A', comp614_module6.Stack))


def recursive_dfs(graph, start_node, parent):
    """
    Given a graph, a start node from which to search, and a mapping of nodes to
    their parents, performs a recursive depth-first search on graph from the 
    given start node, populating the parents mapping as it goes.
    """
    nbrs = graph.get_neighbors(start_node)

    # base case: when all neighbor of start_node all in parent.keys()
    in_parent = True
    for nbr in nbrs:
        if nbr not in parent.keys():
            in_parent = False

    if in_parent:
        return

    # recursive case: if neighbor not in parent.keys(), keep finding
    for nbr in nbrs:
        if nbr not in parent.keys():
            parent[nbr] = start_node
            recursive_dfs(graph, nbr, parent)


# print(recursive_dfs(comp614_module6.file_to_graph('test0.txt'), 'A', {'A': None}))


def get_inbound_nbrs(graph):
    """
    Given a directed graph, returns a mapping of each node n in the graph to
    the set of nodes that have edges into n.
    """
    inbound_nbr = {}
    all_node = []
    for node in graph.nodes():
        # for each node, find their neighbor
        nbrs = graph.get_neighbors(node)
        # if inbound_nbr not in inbound_nbr, add neighbor as key and [node] as value
        # if neighbor already has key, append node in the list
        for nbr in nbrs:
            if nbr not in inbound_nbr:
                inbound_nbr[nbr] = [node]
            else:
                inbound_nbr[nbr].append(node)
            all_node.append(nbr)

    # for node that does not have inbound, make their value set()
    lst_diff = list(set(graph.nodes()) - set(all_node))
    for diff in lst_diff:
        inbound_nbr[diff] = set()

    inbound_nbr_return = inbound_nbr.copy()
    # convert list in values as set
    for key in inbound_nbr:
        inbound_nbr_return[key] = set(inbound_nbr[key])

    return inbound_nbr_return


def remove_sink_nodes(graph):
    """
    Given a directed graph, returns a new copy of the graph where every node that
    was a sink node in the original graph now has an outbound edge linking it to 
    every other node in the graph (excluding itself).
    """
    new_graph = graph.copy()

    for node in new_graph.nodes():
        nbrs = new_graph.get_neighbors(node)
        # check whether the neighbors are empty set
        # if empty set, add all nodes (except node itself) to the node's neighbor
        if nbrs == set():
            for node1 in new_graph.nodes():
                if node1 != node:
                    new_graph.add_edge(node, node1)

    return new_graph


def page_rank(graph, damping):
    """
    Given a directed graph and a damping factor, implements the PageRank algorithm
    -- continuing until delta is less than 10^-8 -- and returns a dictionary that
    maps each node in the graph to its page rank.
    """
    pr_dict = {}
    new_graph = remove_sink_nodes(graph)

    # initialize every page rank as 1/n
    for node in new_graph.nodes():
        pr_dict[node] = 1 / len(new_graph.nodes())

    flow_graph = get_inbound_nbrs(new_graph)

    delta = 1
    while delta >= 10 ** (-8):
        delta = 0
        val_lst = []
        for node in flow_graph:
            val = 0
            nbrs = flow_graph[node]
            for nbr in nbrs:
                # compute the inbound power
                val += pr_dict[nbr] / len(new_graph.get_neighbors(nbr))
            # add damping factor into calculation
            final_value = damping * val + (1 - damping) / len(new_graph.nodes())
            # compute and add up changes to the delta
            delta += abs(final_value - pr_dict[node])
            # put the new final value of this node into val_lst
            val_lst.append(final_value)

        # after we finish compute all the new power for nodes, update
        ite = 0
        for node in flow_graph:
            pr_dict[node] = val_lst[ite]
            ite += 1

    return pr_dict

# wiki_dict = page_rank(comp614_module6.file_to_graph("wikipedia_articles_streamlined.txt"), 0.85)
# a1_sorted_keys = sorted(wiki_dict, key=wiki_dict.get, reverse=True)
# for r in a1_sorted_keys:
#    print(r, wiki_dict[r])
