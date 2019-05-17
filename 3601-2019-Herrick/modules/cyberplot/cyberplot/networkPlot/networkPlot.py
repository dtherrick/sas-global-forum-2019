import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors  # package includes utilities for color ranges
import matplotlib.cm as cmx
import networkx as nx  # to render the network graph


class networkPlot():
    def __init__(self, nodesTable, edgesTable):
        self.nodes = nodesTable
        self.edges = edgesTable

    def renderNetworkGraph(filterCommunity=-1, size=18, sizeVar="_HypGrp_", colorVar="", sizeMultipler=500):
        # build an array of node positions and related colors based on community
    nodes = table(name='nodes')
    if filterCommunity >= 0:
        nodes.where = "_Community_ EQ %F" % filterCommunity
    nodesOut = s.fetch(nodes, to=1000)
    nodes = nodesOut['Fetch']

    nodePos = {}
    nodeColor = {}
    nodeSize = {}
    communities = []
    i = 0
    for nodeId in nodes._Value_:
        nodePos[nodeId] = (nodes._AllXCoord_[i], nodes._AllYCoord_[i])
        if colorVar:
            nodeColor[nodeId] = nodes[colorVar][i]
            if nodes[colorVar][i] not in communities:
                communities.append(nodes[colorVar][i])
        nodeSize[nodeId] = max(nodes[sizeVar][i], 0.1)*sizeMultipler
        i += 1
    communities.sort()

    # build a list of source-target tuples
    edges = table(name='edges')
    if filterCommunity >= 0:
        edges.where = "_SCommunity_ EQ %F AND _TCommunity_ EQ %F" % (
            filterCommunity, filterCommunity)
    edgesOut = s.fetch(edges, to=1000)
    edges = edgesOut['Fetch']

    edgeTuples = []
    i = 0
    for p in edges._Source_:
        edgeTuples.append((edges._Source_[i], edges._Target_[i]))
        i += 1

    # Add nodes and edges to the graph
    plt.figure(figsize=(size, size))
    graph = nx.DiGraph()
    graph.add_edges_from(edgeTuples)

    # Size mapping
    getNodeSize = [nodeSize[v] for v in graph]

    # Color mapping
    jet = cm = plt.get_cmap('jet')
    getNodeColor = None
    if colorVar:
        getNodeColor = [nodeColor[v] for v in graph]
        cNorm = colors.Normalize(vmin=min(communities), vmax=max(communities))
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

        # Using a figure here to work-around the fact that networkx doesn't produce a labelled legend
        f = plt.figure(1)
        ax = f.add_subplot(1, 1, 1)
        for community in communities:
            ax.plot([0], [0], color=scalarMap.to_rgba(
                community), label="Community %s" % "{:2.0f}".format(community), linewidth=10)

    # render the graph
    nx.draw_networkx_nodes(
        graph, nodePos, node_size=getNodeSize, node_color=getNodeColor, cmap=jet)
    nx.draw_networkx_edges(graph, nodePos, width=1, alpha=0.5)
    nx.draw_networkx_labels(graph, nodePos, font_size=11,
                            font_family='sans-serif')

    if len(communities) > 0:
        plt.legend(loc='upper left', prop={'size': 11})

    plt.title('Hartford drug user social network', fontsize=30)
    plt.axis('off')
    plt.show()