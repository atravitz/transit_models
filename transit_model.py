import networkx as nx
import random
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt


class Passenger:
    def __init__(self):
        self.fees = 0
        self.transit_time = 0


def initialize(n_passengers, node_capacity, itinerary=None, intermediate_stops=0):
    g = nx.read_gml('cta.gml')

    # number of passengers at a stop
    nx.set_node_attributes(g, 0, 'population')
    # passenger capacity of a stop
    nx.set_node_attributes(g, node_capacity, 'capacity')

    passengers = []
    for i in range(n_passengers):
        # assign a random direct-path itinerary
        p = Passenger()

        if itinerary is None:
            p.home = random.choice(list(g.nodes))
            random_itinerary = [p.home]
            for i in range(intermediate_stops+1): # add 1 to represent work
                random_itinerary.append(random.choice(list(g.nodes)))
            random_itinerary.append(p.home)
            p.itinerary = random_itinerary
        else:
            p.itinerary = itinerary

        p.itinerary_index = 0
        p.current = p.itinerary[p.itinerary_index]
        p.destination = p.itinerary[p.itinerary_index + 1]
        p.completed = False

        passengers.append(p)

        # populate the node
        g.nodes[p.current]['population'] += 1
    return(g, passengers)


def update(g, passengers,
           max_run_steps, graph_period=None,
           time_penalty_capacity=3, time_penalty_transfer=3):
    transit_times = []
    timestep = 0
    graphs = []
    while len(transit_times) < len(passengers) and timestep < max_run_steps:
        for i in random.sample(list(range(len(passengers))), len(passengers)):
            p = passengers[i]
            # check to see if passenger has already completed their trip
            if p.completed == False:
                # update destination if needed
                if p.current == p.destination:
                    p.itinerary_index += 1
                    # if passenger has completed trip, remove from node and mark as complete
                    if p.itinerary_index == len(p.itinerary)-1:
                        transit_times.append(p.transit_time)
                        p.completed = True
                        g.nodes[p.current]['population'] -= 1
                        continue
                    else:
                        p.destination = p.itinerary[(p.itinerary_index + 1)]

                if p.current != p.destination:
                    path = nx.shortest_path(g, p.current, p.destination)
                    next_node = path[1]

                    # time penalize if transferring between lines
                    if  g.nodes[p.current]['nodecolor'] not in g.nodes[next_node]['allnodecolors']:
                        p.transit_time += time_penalty_transfer

                    # time penalize if station is over capacity
                    if g.nodes[next_node]['population'] >= g.nodes[next_node]['capacity']:
                        p.transit_time += time_penalty_capacity

                    # population balance
                    g.nodes[p.current]['population'] -= 1
                    p.current = next_node
                    g.nodes[p.current]['population'] += 1
                p.transit_time += 1

        if graph_period and timestep%graph_period == 0:
            graphs.append(g.copy())
        timestep += 1

    if graph_period:
        return(transit_times, graphs)
    else:
        return(transit_times)


def add_line(path, g, name):
    """add a new line to a networkx graph
       note: all nodes must already exist"""
    new_line = np.loadtxt(path, dtype=int)

    for i in range(len(new_line)-1):
        node_src = str(new_line[i])
        node_dst = str(new_line[i+1])
        g.add_edge(node_src, node_dst)

    for n in new_line:
        node_colors = g.nodes[str(n)]['allnodecolors']
        if 'lightblue' not in node_colors:
            if type(node_colors) == list:
                g.nodes[str(n)]['allnodecolors'] = g.nodes[str(n)]['allnodecolors'] + ['lightblue']
            elif type(node_colors) == str:
                g.nodes[str(n)]['allnodecolors'] = [g.nodes[str(n)]['allnodecolors'], 'lightblue']
    return(g)


if __name__ == '__main__':
    g, passengers = initialize(n_passengers=100, node_capacity=10, intermediate_stops=2)
    update(g, passengers, max_run_steps=10)


