import numpy as np
import tsplib95

import pandas as pd
from map import Map


def get_data(type):
    """
    Obtains the data from the datafiles

    Args:
    type    (string)        the type of datafile that is used

    Returns:
    data    (tsp-object)    data object of imported tsp module with node data
    data_tour (tsp-object)  data object of imported tsp module with tour data

    """

    data = tsplib95.load(f'data/{type}.tsp.txt')
    data_tour = tsplib95.load(f'data/{type}.opt.tour.txt')

    return data, data_tour

def create_map(data, type, data_tour):
    """
        node_dict   (dict)      dictionary of nodes and their coordinates
        coords  (nparray)      np array of coordinates
    """


    # make node dict of coordinates
    node_dict = data.node_coords

    # list of all nodes
    nodes = np.array(list(node_dict.keys()))

    # make a list of coordinates
    coords = np.array(list(node_dict.values()))

    optimal_tour = np.array(data_tour.tours[0])
    opt_tour_dist = data.trace_tours(data_tour.tours)

    name = type

    map = Map(name, nodes, coords, optimal_tour, opt_tour_dist)

    return map


# data file types
types = ["a280", "eil51", "pcb442"]

data, data_tour = get_data(types[1])


map = create_map(data, type, data_tour)

inds = [0,1]

map.swap(inds)
