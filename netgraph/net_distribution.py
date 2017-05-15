# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt

class DrawDistribution:
    COLORS = [
        '#F20010', '#FC4292', '#B94C4A', '#D19D39', '#A79D0F', '#A65FCC',
        '#9470E7', '#19CD1D', '#1DDF9A', '#52A79F', '#24B5D9', '#2080DC'
    ]
    def __init__(self):
        self.G = nx.Graph()
        self.min_node_size = 20
        self.max_node_size = 300

    def import_data(self, edges):
        self.G.add_weighted_edges_from(edges)
        self.degree = nx.degree(self.G)
        self.max_degree_value = max(self.degree.values())

    def one_node_size(self, n):
        d = self.degree[n]
        d = d / self.max_degree_value * self.max_node_size
        if d < self.min_node_size:
            d = self.min_node_size
        return d

    def get_nodes_size(self, nodes):
        return [self.one_node_size(n) for n in nodes]

    def one_node_color(self, n):
        d = self.degree[n]
        for index, color in enumerate(self.COLORS):
            if d * (index + 1) ** 2 >= self.max_degree_value:
                return color
        return self.COLORS[-1]

    def get_nodes_color(self, nodes):
        return [self.one_node_color(n) for n in nodes]

    def plot_networkx(self):
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_edges(self.G, pos, alpha=0.1)
        # nx.draw_networkx_labels(
        #     self.G, pos,
        #     font_size=6,
        #     font_color='r',
        #     alpha=0.2
        # )
        nx.draw_networkx_nodes(
            self.G, pos,
            node_size=self.get_nodes_size(self.G.nodes()),
            node_color=self.get_nodes_color(self.G.nodes()),
            alpha=0.8,
            label=True
        )
        plt.axis('off')
        plt.show()
