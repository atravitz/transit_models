import networkx as nx
import random
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt


class Passenger:
    def __init__(self):
        self.fees = 0
        self.transit_time = 0


def initialize(n_passengers, node_capacity, itinerary=None):
    g = nx.read_gml('cta.gml')

    # number of passengers at a stop
    nx.set_node_attributes(g, 0, 'population')
    # passenger capacity of a stop
    nx.set_node_attributes(g, node_capacity, 'capacity')

    passengers = []
    for i in range(n_passengers):

        # assign a random direct-path itinerary
        p = Passenger()
        p.home = random.choice(list(g.nodes))
        p.work = random.choice(list(g.nodes))

        if itinerary is None:
            p.itinerary = [p.home, p.work, p.home]
        else: p.itinerary = itinerary

        p.itinerary_index = 0
        p.current = p.itinerary[p.itinerary_index]
        p.destination = p.itinerary[p.itinerary_index + 1]
        p.completed = False

        passengers.append(p)

        # populate the node
        g.nodes[p.current]['population'] += 1

        return(g, passengers)

def update(g, passengers, run_steps):

    for t in range(run_steps):
        for i in range(len(passengers)):
            p = passengers[i]
            # check to see if passenger has already completed their trip
            if p.completed == False:
                # update destination if needed
                if p.current == p.destination:
                    p.itinerary_index += 1
                    if p.itinerary_index == len(p.itinerary)-1:
                        print('complete, transit time is', p.transit_time)
                        p.completed = True
                        continue
                    else:
                        p.destination = p.itinerary[(p.itinerary_index + 1)]

                if p.current != p.destination:
                    path = nx.shortest_path(g, p.current, p.destination)
                    next_node = path[1]

                    if g.nodes[next_node]['population'] < g.nodes[next_node]['capacity']:
                        p.current = next_node

                p.transit_time = p.transit_time + 1


if __name__ == '__main__':
    initialize()
    for n in range(n_simulations):
        update(run_steps=timesteps)

