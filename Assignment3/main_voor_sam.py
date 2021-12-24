import numpy as np
import tsplib95
import pickle
import pandas as pd
from map import Map
from anneal import SimAnneal
import time
from time import strftime, localtime
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
# data, data_tour = get_data(types[0])

# create map
# map = create_map(data, type, data_tour)


# anneal
# chain_length = 10
# T0 = 15
# # T0 = 40
# Nmax = 10
# sched = 2
# params = [0.005]
# chain_length = 200
# method=4
# simAnneal = SimAnneal(types[0], T0, sched, chain_length, method, params=None)
# #
# fitnesses = simAnneal.run(Nmax=Nmax)

# plt.plot(list(range(len(fitnesses['Distances']))), fitnesses['Distances'])
# plt.show()


# DEZE1
T0s = [10, 20, 50, 80]

Nmax = 10000
chain_lengths = [500]
scheds = [1, 2]
methods = [1, 2, 3, 4]


# Deze2
data_dict = {}
data_dict["all_params"] = {"T0s": T0s,
                            "chain_lengths": chain_lengths, "scheds": scheds,
                             "Nmax": Nmax, "methods":methods}
for T0 in T0s:
    print("T0:", T0, "out of", T0s)
    data_dict[T0] = {}

    for chain_length in chain_lengths:
        print(" chain_length:", chain_length, "out of", chain_lengths)

        data_dict[T0][chain_length] = {}

        for sched_i in range(len(scheds)):
            sched = scheds[sched_i]

            print("     sched", sched, "outof", scheds)

            data_dict[T0][chain_length][sched]  = {}

            for method in methods:
                data_dict[T0][chain_length][sched][method] = {}


                print("         method", method, "outof", methods)
                SA = SimAnneal(type="a280",
                               T0=T0,
                               sched=sched,
                               chain_length=chain_length,
                               method=method)

                fitnesses = SA.run(Nmax=Nmax)

                data_dict[T0][chain_length][sched][method] = {}
                data_dict[T0][chain_length][sched][method]["fitnesses"]  = fitnesses['Distances']
                data_dict[T0][chain_length][sched][method]["temps"] = fitnesses['Temperature']
                data_dict[T0][chain_length][sched][method]["Iters"] = fitnesses['Iteration']
                # data_dict[T0][chain_length][sched][method]["best_dist"] = map.lowest_distance
                # data_dict[T0][chain_length][sched][method]["best_tour"] = map.best_tour

# Deze3

time_form = strftime("%y_%m_%d_%H_%M_%S", localtime())

name = f'results/data_many_{time_form}'
outfile = open(name, 'ab')
pickle.dump(data_dict, outfile)
outfile.close()
