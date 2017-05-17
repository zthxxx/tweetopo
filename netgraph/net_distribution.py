# -*- coding: utf-8 -*-
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class DrawDistribution:
    def __init__(self):
        self.G = nx.Graph()
        self.degree = None
        self.pageranks = None
        self.max_pagerank = None
        self.max_degree = None
        self.pos = None
        self.min_node_size = 20
        self.max_node_size = 360

    def import_data(self, edges):
        self.G.add_weighted_edges_from(edges)
        self.pos = nx.spring_layout(self.G, iterations=100)
        self.degree = dict(nx.degree(self.G))
        self.pageranks = nx.pagerank(self.G)
        self.clustering = nx.clustering(self.G)
        self.max_degree = max(self.degree.values())
        self.max_pagerank = max(self.pageranks.values())
        self.max_clustering = max(self.clustering.values())
        # self.filter_nodes()

    def filter_nodes(self):
        micro_nodes = [node for node, deg in self.degree.items() if deg < 8]
        self.G.remove_nodes_from(micro_nodes)

    def node_rank(self, node):
        '''
        :param n:  node
        :return: Normalized value from 0 to 1, mean that the rank of the node
        '''
        # rank = self.degree[node] / self.max_degree
        # rank = math.log(self.degree[node]+1, self.max_degree+1)
        rank = self.pageranks[node] / self.max_pagerank
        # rank = self.clustering[node] / self.max_clustering
        return rank

    def node_size(self, n):
        rank = self.node_rank(n)
        d = rank * self.max_node_size
        if d < self.min_node_size:
            d = self.min_node_size
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
        degrees = self.degree
        node1 = edge[0]
        node2 = edge[1]
        node = node1 if degrees[node1] < degrees[node2] else node2
        return self.node_color(node)

    def edges_color(self, edges):
        return [self.edge_color(edge) for edge in edges]

    def plot_networkx(self):
        nx.draw_networkx_edges(
            self.G, self.pos,
            edge_color=self.edges_color(self.G.edges()),
            alpha=0.08
        )
        # nx.draw_networkx_labels(
        #     self.G, self.pos,
        #     font_size=8,
        #     font_color='r',
        #     alpha=0.2
        # )
        nx.draw_networkx_nodes(
            self.G, self.pos,
            node_size=self.nodes_size(self.G.nodes()),
            node_color=self.nodes_color(self.G.nodes()),
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
            self.degree
            self.pageranks
            self.clustering
        '''
        signal = list(self.clustering.values())
        signal = np.asarray(signal)
        self.plot_pdf(signal)
        self.plot_cdf(signal)
