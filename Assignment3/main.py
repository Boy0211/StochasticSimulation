import numpy as np
import tsplib95

import pandas as pd
from map import Map
from anneal import SimAnneal

import matplotlib.pyplot as plt


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
    Creates a map from the Map class with the given nodes.

    Args:
        data    (tsp-object)    data object of imported tsp module with node data
        type    (string)        the type of datafile that is used
        data_tour (tsp-object)  data object of imported tsp module with tour data

    Returns:
        map (Map-object)        Map object
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

# parse data
data, data_tour = get_data(types[1])

# create map
map = create_map(data, type, data_tour)


# anneal
T0 =50
Nmax = 100000
sched = 3
B = 1
simAnneal = SimAnneal(map, T0, Nmax, sched, B)

fitnesses = simAnneal.annealing()
temps = simAnneal.temps
print(temps[-1])
print(fitnesses[-1])
#
plt.plot(list(range(Nmax)), fitnesses)
plt.plot(list(range(Nmax)), temps)
plt.show()

# # tests the swap function
inds = [50,3]
j = 3
i = 10

# map.swap_1node([i,j])
#
#
# print(map.nodes)
# print(map.nodes_list)
# print(len(map.nodes))
# plt.scatter(map.coords[:,0], map.coords[:,1])
# plt.plot(map.coords[:,0], map.coords[:,1])
# # plt.show()
