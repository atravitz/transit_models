"""Convert GTFS data to a networkx graph"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import itertools


# import GTFS files ()
ROUTES = pd.read_csv('cta_data/routes.txt')
STOPS = pd.read_csv('cta_data/stops.txt')
TRIPS = pd.read_csv('cta_data/trips.txt')
STOP_TIMES = pd.read_csv('cta_data/stop_times.txt')

# Filter route data to only include "L" Train info
ROUTES_subway = ROUTES[ROUTES['route_type']==1]
route_ids_subway = ROUTES_subway['route_id'].values.tolist()

# Filter trips data to only include trips with "L" Train info
TRIPS_subway = TRIPS[TRIPS['route_id'].isin(route_ids_subway)]
trip_ids_subway = list(TRIPS_subway['trip_id'].values)

# Pick the first trip (order is arbitrary) for each route
# TODO: figure out a better way to avoid over-defining the network
trip_id_dict = {}
for route_id in route_ids_subway:
    trip_id_dict[route_id] = TRIPS_subway[TRIPS_subway['route_id']==route_id].iloc[0]['trip_id']

# Filter stop times data to include only
# one trip_id for each route (from above dict)
STOP_TIMES_subway = STOP_TIMES[STOP_TIMES['trip_id'].isin(trip_id_dict.values())].reset_index()
STOP_TIMES_subway[STOP_TIMES_subway['pickup_type'] == 0]

# Only track stations ('location_type'=1)
STOPS_stations = STOPS[STOPS['location_type']==1]

def get_parent(stop_id):
    """returns the parent station for a given stop."""
    parent = STOPS[STOPS['stop_id']==stop_id]['parent_station'].values
    if len(parent) == 0:
        return stop_id
    else:
        return int(parent[0])

STOP_TIMES_subway['station_id'] = STOP_TIMES_subway['stop_id'].apply(get_parent)

## determine graph edges
edges_list = []
for trip_id, group in STOP_TIMES_subway.groupby('trip_id'):
        for i in group.index[:-1]:
            origin_stop = STOP_TIMES_subway['station_id'][i]
            dest_stop = STOP_TIMES_subway['station_id'][i+1]
            ## only record edges that are 1 unit away
            if (STOP_TIMES_subway['stop_sequence'][i+1] - STOP_TIMES_subway['stop_sequence'][i]) == 1:
                edges_list.append((origin_stop, dest_stop))

## read in stops info
## TODO: get this info from GTFS data only
l_stops_raw = pd.read_csv("cta_data/CTA_-_System_Information_-_List_of__L__Stops_-_Map.csv")
# convert coords to a readable dict
locations = l_stops_raw.Location.apply(lambda x: x[1:-1].split(","))
coords = pd.DataFrame(locations.tolist(), columns=['lat', 'long']).astype('float')

l_stops = l_stops_raw.drop(['Location'], axis=1)
l_stops = l_stops.join(coords)

l_stops['STATION_ID'] = l_stops['STOP_ID'].apply(get_parent)

# read in stop colors
stop_colors = l_stops[['STATION_ID', 'RED', 'BLUE', 'G', 'BRN', 'P', 'Pexp', 'Y','Pnk', 'O']]

color_conversion = {'RED':'red', 'BLUE':'blue', 'G':'green', 'BRN':'brown', 'P':'purple', 'Pexp':'purple', 'Y':'yellow','Pnk':'pink', 'O':'orange'}

colors_dict = {}
for i in stop_colors.index:
    colors_list = []
    for c in stop_colors.columns.astype('str'):
        if stop_colors[c][i] == True:
            colors_list.append(color_conversion[c])
    if len(colors_list) == 0:
        colors_list.append('k')
    colors_dict[l_stops['STATION_ID'][i]] = colors_list



## build networkx graph
G = nx.Graph()

G.add_edges_from(edges_list)

for n in G.nodes:
    stop_row = STOPS[STOPS['stop_id']==n]
    G.nodes[n]['pos'] = (stop_row['stop_lon'].values[0],
                         stop_row['stop_lat'].values[0])
    G.nodes[n]['node_color'] = colors_dict[n][0]

nx.write_gml(G, 'cta.gml')
