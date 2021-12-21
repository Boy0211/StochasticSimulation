import numpy as np
import tsplib95
import pickle
import pandas as pd
from map import Map
from anneal import SimAnneal
import time

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

def draw_2y_figure(fitnesses, temps, Nmax, save=False, filename=None):

    fig, axis = plt.subplots(figsize=(12, 8))
    axis.plot(list(range(Nmax)), fitnesses, color='blue', alpha=0.5)

    axis.set_xlabel('Iterations', fontsize=14)
    axis.set_ylabel('Fitnesses', fontsize=14)

    axis2 = axis.twinx()

    axis2.plot(list(range(Nmax)), temps, color='red', alpha=0.5)
    axis2.set_ylabel('Temps', fontsize=14)

    fig.suptitle('Fitness and temp over iterations', fontsize=16)
    plt.legend()

    if (save == True) & (filename != None):
        fig.savefig(f'overleaf/figures/{filename}.png')
    else:
        plt.show()

def draw_route(map, save=False, filename=None):

    fig, axis = plt.subplots(figsize=(12, 8))

    axis.scatter(map.coords[:,0], map.coords[:,1], marker='s')
    axis.plot(map.coords[:,0], map.coords[:,1], alpha=0.5)
    fig.suptitle('The route of the travelling salesman')

    if (save == True) & (filename != None):
        fig.savefig(f'../overleaf/figures/{filename}.png')
    else:
        plt.show()


# data file types
types = ["a280", "eil51", "pcb442"]

# parse data
data, data_tour = get_data(types[0])

# create map
# map = create_map(data, type, data_tour)


# anneal
chain_length = 10
T0 = 15
# T0 = 40
Nmax = 100000
sched = 3
params = [0.00005]
chain_length = 200
simAnneal = SimAnneal(map, T0, Nmax, sched, params, chain_length)
#
fitnesses = simAnneal.annealing()
temps = simAnneal.temps

plt.plot(list(range(Nmax)), fitnesses)
plt.show()
plt.plot(list(range(Nmax)), temps)
plt.show()

#DEZE1
# T0s = [1,5,10,20,50,80,100]
# Nmax = 1000
# Total_max = 100000
#
# chain_lengths = [1, 10, 50,100,500,1000]
# scheds = [1,2,3]
# paramss = [[[1]],
#             [[0]],
#             [[0.00005],[0.0005],[0.005], [0.05]]]



# draw_2y_figure(fitnesses, temps, Nmax)
# draw_route(map)
#
# T0s = [1,2]
# Nmax = 10000
# Total_max = 100
#
# chain_lengths = [1]
# scheds = [1,2,3]
# paramss = [[[1]],
#             [[1], [2], [3]],
#             [[2]]
#             ]




# T0 = 20
# Nmax =100
# Nmax = 500000
# Nmax = 1000000
# sched = 1
# params = [0.0006]
# params = [0.00004]
# params = [1]


# Deze2
# data_dict = {}
# data_dict["all_params"] = {"T0s": T0s,
#                             "chain_lengths": chain_lengths, "scheds": scheds,
#                             "paramss": paramss, "Total_max": Total_max}
# for T0 in T0s:
#     print("T0:", T0, "out of", T0s)
#     data_dict[T0] = {}
#
#     for chain_length in chain_lengths:
#         print(" chain_length:", chain_length, "out of", chain_lengths)
#         data_dict[T0][chain_length] = {}
#
#         for sched_i in range(len(scheds)):
#             sched = scheds[sched_i]
#
#             print("     sched", sched, "outof", scheds)
#
#             data_dict[T0][chain_length][sched]  = {}
#             for params in paramss[sched_i]:
#
#                 print("         params", params, "outof", paramss[sched_i])
#                 # map = create_map(data, type, data_tour)
#                 Nmax = int(Total_max/chain_length)
#
#
#                 simAnneal = SimAnneal(map, T0, Nmax, sched, params, chain_length)
#
#                 fitnesses = simAnneal.annealing()
#                 temps = simAnneal.temps
#
#                 params_key = str(params)
#                 data_dict[T0][chain_length][sched][params_key] = {}
#                 data_dict[T0][chain_length][sched][params_key]["fitnesses"]  = fitnesses
#                 data_dict[T0][chain_length][sched][params_key]["temps"] = temps
#                 data_dict[T0][chain_length][sched][params_key]["best_dist"] = map.lowest_distance
#                 data_dict[T0][chain_length][sched][params_key]["best_tour"] = map.best_tour

# Deze3
# # print(data_dict)
# name = f'results/data_many_{time.time()}'
# outfile = open(name, 'ab')
# pickle.dump(data_dict, outfile)
# outfile.close()



# infile = open(name, 'rb')
# db = pickle.load(infile)
# for keys in db:
#     print(keys, '=>', db[keys])
# infile.close()

# fitnesses = simAnneal.annealing()
# temps = simAnneal.temps
# print(temps[-1])
# print(temps[:10])
# print(fitnesses[-1], fitnesses[0])
# print(map.lowest_distance, "best found")
# #

# plt.plot(list(range(Nmax)), fitnesses)
# plt.show()
# plt.plot(list(range(Nmax)), temps)
# plt.show()

# # tests the swap function
# inds = [50,3]
# j = 3
# i = 10

# map.swap_1node([i,j])
# print(map.check_nodelist())
#
# print(map.nodes)
# print(map.nodes_list)
# print(len(map.nodes))
# plt.scatter(map.coords[:,0], map.coords[:,1])
# plt.plot(map.coords[:,0], map.coords[:,1])
# plt.show()
# plt.plot(map.optimal_tour_coords[:,0], map.optimal_tour_coords[:,1])
# plt.show()
