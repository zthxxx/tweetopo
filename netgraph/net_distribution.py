# -*- coding: utf-8 -*-
import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class DrawDistribution:
    def __init__(self):
        self.G = nx.Graph()
        self.degree = []
        self.max_degree_value = None
        self.min_node_size = 20
        self.max_node_size = 360

    def import_data(self, edges):
        self.G.add_weighted_edges_from(edges)
        self.degree = nx.degree(self.G)
        self.max_degree_value = max(self.degree.values())

    def node_size(self, n):
        d = self.degree[n]
        d = d / self.max_degree_value * self.max_node_size
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
        d = self.degree[n]
        deep = d / self.max_degree_value
        hex = self.hue_map(deep)
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
        pos = nx.spring_layout(self.G)

        nx.draw_networkx_edges(
            self.G, pos,
            edge_color=self.edges_color(self.G.edges()),
            alpha=0.07
        )
        # nx.draw_networkx_labels(
        #     self.G, pos,
        #     font_size=8,
        #     font_color='r',
        #     alpha=0.2
        # )
        nx.draw_networkx_nodes(
            self.G, pos,
            node_size=self.nodes_size(self.G.nodes()),
            node_color=self.nodes_color(self.G.nodes()),
            alpha=0.85
        )
        plt.axis('off')
        plt.show()
