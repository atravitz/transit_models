import transit_model as tm
import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
from matplotlib.animation import FuncAnimation

g = nx.read_gml('cta.gml')
node_coords = {}
for n in g:
    node_coords[n] = g.nodes[n]['pos']

g, passengers = tm.initialize(n_passengers=1000, node_capacity=100)

transit_times, graphs = tm.update(g, passengers, max_run_steps=100, graph_period=1)

def update_graph(i):
    ax.clear()
    G = graphs[i]
    colors = [G.nodes[i]['population'] for i in G.nodes]
    nx.draw(G, node_coords,
            ax=ax, alpha=0.8,
            node_size=10,
            node_color=colors,
            cmap='PuBu')
    plt.axis('equal')
    # plt.grid(which='both')
    # plt.show()



fig, ax = plt.subplots(dpi=150)
ani = FuncAnimation(fig, update_graph, frames=len(graphs), repeat_delay=100)
ani.save('animation.gif', writer='imagemagick', fps=60)

plt.show()