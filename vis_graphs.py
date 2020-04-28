import transit_model as tm
import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
from matplotlib.animation import FuncAnimation



def animation(graphs, save=False):

    def update_graph(i):
        ax.clear()
        G = graphs[i]
        colors = [G.nodes[i]['population'] for i in G.nodes]
        nx.draw_networkx_nodes(G, node_coords,
                            ax=ax,
                            node_size=20,
                            node_color=[G.nodes[i]['nodecolor'] for i in G.nodes])
        nx.draw(G, node_coords,
                ax=ax, alpha=0.9,
                node_size=10,
                node_color=colors,
                cmap='Greys')
        plt.axis('equal')

    fig, ax = plt.subplots(dpi=150)
    ani = FuncAnimation(fig, update_graph, frames=len(graphs), repeat_delay=100)
    if save:
        ani.save('animation.gif', writer='imagemagick', dpi=120, fps=10)

    plt.show()


if __name__ == '__main__':
    g = nx.read_gml('cta.gml')

    node_coords = {}
    for n in g:
        node_coords[n] = g.nodes[n]['pos']

    g, passengers = tm.initialize(n_passengers=10, node_capacity=1000)
    transit_times, graphs = tm.update(g, passengers, max_run_steps=1000, graph_period=1)

    animation(graphs)