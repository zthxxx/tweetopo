# -*- coding: utf-8 -*-
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class GraphAnalysis:
    def __init__(self, edges, measure='pagerank'):
        '''
        Class for analysis graph
        :param edges: weighted_edges The edges must be given as 3-tuples like (u,v,weight)
        :param measure: what measure for analysis to filter,
                        must be one of  'degree' or 'pagerank' or 'clustering'
        '''
        self.measure = measure
        self.G = nx.Graph()
        self.import_data(edges)

    def import_data(self, edges):
        self.G.add_weighted_edges_from(edges)
        self.pos = nx.spring_layout(self.G, iterations=100)
        self.get_measures()

    def get_degrees(self):
        self.degrees = dict(nx.degree(self.G))
        self.max_degree = max(self.degrees.values())

    def get_pageranks(self):
        self.pageranks = nx.pagerank(self.G)
        self.max_pagerank = max(self.pageranks.values())

    def get_clusterings(self):
        self.clusterings = nx.clustering(self.G)
        self.max_clustering = max(self.clusterings.values())

    def get_measures(self):
        self.get_degrees()
        self.get_pageranks()
        self.get_clusterings()
        measures = {'degree': (self.degrees, self.max_degree),
                    'pagerank': (self.pageranks, self.max_pagerank),
                    'clustering': (self.clusterings, self.max_clustering)}
        if self.measure in measures:
            self.ranks, self.max_rank = measures[self.measure]

    def node_rank(self, node):
        '''
        :param n:  node
        :return: Normalized value from 0 to 1, mean that the rank of the node
        '''
        rank = self.ranks[node] / self.max_rank
        return rank

    def filter_ranks(self, gate):
        '''
        delete some micro node which measure under the threshold
        :param gate: gate is a normalized threshold value from 0 to 1,
                     will filtered node out which measure less than it.
        '''
        if not gate:
            return
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
    def __init__(self, edges, **kwargs):
        super().__init__(edges, **kwargs)

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

    def plot_networkx(self, with_label=False, block=True):
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
        plt.show(block=block)
        plt.clf()

    def plot_pdf(self, signal, block=True):
        plt.hist(signal, len(signal)*2)
        plt.show(block=block)
        plt.clf()

    def plot_cdf(self, signal, block=True):
        plt.hist(signal, len(signal)*2, cumulative=True, histtype='step')
        plt.show(block=block)
        plt.clf()

    def plot_rank_pdf_cdf(self, block=True):
        signal = list(self.ranks.values())
        self.plot_pdf(signal, block=block)
        self.plot_cdf(signal, block=block)
