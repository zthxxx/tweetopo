# -*- coding: utf-8 -*-
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class GraphAnalysis:
    def __init__(self, edges):
        self.G = nx.Graph()
        self.import_data(edges)

    def import_data(self, edges):
        self.G.add_weighted_edges_from(edges)
        self.pos = nx.spring_layout(self.G, iterations=100)
        self.get_measures()

    def get_measures(self):
        self.degrees = dict(nx.degree(self.G))
        self.max_degree = max(self.degrees.values())
        self.pageranks = nx.pagerank(self.G)
        self.max_pagerank = max(self.pageranks.values())
        self.clusterings = nx.clustering(self.G)
        self.max_clustering = max(self.clusterings.values())

    def node_rank(self, node):
        '''
        :param n:  node
        :return: Normalized value from 0 to 1, mean that the rank of the node
        '''
        # rank = self.degrees[node] / self.max_degree
        # rank = math.log(self.degrees[node]+1, self.max_degree+1)
        rank = self.pageranks[node] / self.max_pagerank
        # rank = self.clusterings[node] / self.max_clustering
        return rank

    def filter_nodes(self, gate):
        deserts = [node for node in self.G.nodes()
                       if self.node_rank(node) < gate]
        self.G.remove_nodes_from(deserts)


    def get_nodes(self):
        nodes = self.G.nodes()
        users = [(n , self.degrees[n], self.pageranks[n], self.clusterings[n])  for n in nodes]
        return users

class DrawDistribution(GraphAnalysis):
    MIN_NODE_SIZE = 20
    MAX_NODE_SIZE = 360
    def __init__(self, edges):
        super().__init__(edges)

    def node_size(self, n):
        rank = self.node_rank(n)
        d = rank * self.MAX_NODE_SIZE
        if d < self.MIN_NODE_SIZE:
            d = self.MIN_NODE_SIZE
        return d

    def nodes_size(self, nodes):
        return [self.node_size(n) for n in nodes]

    def hue_map(self, value):
        '''
        :param value: number 0 to 1, map to hue 0.6 - 0 (blue to red, like heatmap)
                      more highter the value, more warm the color
        :return: hex of rgb
        '''
        HUE_MAX = 0.6
        hue = pow(1 - value, 2) * HUE_MAX
        rgb = colors.hsv_to_rgb((hue, 1, 1))
        hex = colors.to_hex(rgb)
        return hex

    def node_color(self, n):
        rank = self.node_rank(n)
        hex = self.hue_map(rank)
        return hex

    def nodes_color(self, nodes):
        return [self.node_color(n) for n in nodes]

    def edge_color(self, edge):
        degrees = self.degrees
        node1 = edge[0]
        node2 = edge[1]
        node = node1 if degrees[node1] < degrees[node2] else node2
        return self.node_color(node)

    def edges_color(self, edges):
        return [self.edge_color(edge) for edge in edges]

    def plot_networkx(self, with_label=False):
        nx.draw_networkx_edges(
            self.G, self.pos,
            edge_color=self.edges_color(self.G.edges()),
            alpha=0.08
        )
        if with_label:
            nx.draw_networkx_labels(
                self.G, self.pos,
                font_size=8,
                font_color='r',
                alpha=0.2
            )
        nodes = self.G.nodes()
        nx.draw_networkx_nodes(
            self.G, self.pos,
            node_size=self.nodes_size(nodes),
            node_color=self.nodes_color(nodes),
            alpha=0.85
        )
        plt.axis('off')
        plt.show()

    def plot_pdf(self, signal):
        plt.hist(signal, len(signal)*2)
        plt.show()

    def plot_cdf(self, signal):
        plt.hist(signal, len(signal) * 2, cumulative=True, label='CDF DATA', histtype='step', alpha=0.55, color='purple')
        plt.show()

    def plot_rank_pdf_cdf(self):
        '''
        ranklist:
            self.degrees
            self.pageranks
            self.clusterings
        '''
        signal = list(self.clusterings.values())
        signal = np.asarray(signal)
        self.plot_pdf(signal)
        self.plot_cdf(signal)
