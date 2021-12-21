import numpy as np
import pandas as pd
import random
from map import Map
import tsplib95
from tqdm import trange


def get_data(type):
    """
    Obtains the data from the datafiles

    Args:
    type    (string)        the type of datafile that is used

    Returns:
    data    (tsp-object)    data object of imported tsp module with node data
    data_tour (tsp-object)  data object of imported tsp module with tour data

    """
    # print(type)
    data = tsplib95.load(f"data/{type}.tsp.txt")
    data_tour = tsplib95.load(f'data/{type}.opt.tour.txt')

    return data, data_tour

def coolsched1(T0, iteration, params=0.0005):
    """
    Caluclates temperature according to a cooling schedule

    Returns
        T   (float)             Temperature
    """
    if iteration == 0:
        T = T0
    else:
        T = T0 * np.exp(-iteration * params)

    return T

def coolsched2(T0, iteration, params=1):
    """
    Caluclates temperature according to a cooling schedule

    Returns
        T   (float)             Temperature
    """

    if iteration == 0:
        T = T0
    else:
        T = T0/(np.log(iteration + params))

    return T

class SimAnneal:
    """
    Class object to perform simulated annealing
    """
    def __init__(self, type, T0, sched, chain_length, method, params=None):
        """
        Initialization of the SimAnneal class.

        Args:

        map:    (map-object)       map of map object
        T0:     (float)            The T0
        Nmax:   (integer)          Maximal number of cycles
        sched:  (integer)          the cooling schedule to use
        B:      (float)            B parameter for cooling scheds
        """

        data, data_tour = get_data(type)
        self.Map = Map(type, data.node_coords, data_tour.tours[0])
        self.T0 = T0
        self.sched = sched
        self.chain_length = chain_length
        self.method = method
        self.params = params

        self.output_data = {'Distances': [self.Map.calculate_tour_length(self.Map.edges)],
                            'Iteration': [-1],
                            'Temperature': [self.T0]}

    def run(self, Nmax=10000, save=False):
        """
        Performs simulated annealing
        """

        for iteration in range(Nmax):
            T = self.coolscheds(self.sched, self.T0, iteration, self.params)
            for chain in range(self.chain_length):

                new_nodes, new_edges, new_distance = self.sampling_method(self.method)

                p = np.exp(-(new_distance - self.output_data['Distances'][-1])/T)

                if (new_distance < self.output_data['Distances'][-1]) | (p > np.random.uniform()):
                    self.Map.nodes = new_nodes
                    self.Map.edges = new_edges
                    self.output_data['Distances'].append(new_distance)
                else:
                    self.output_data['Distances'].append(self.output_data['Distances'][-1])

                self.output_data['Iteration'].append(iteration + chain)
                self.output_data['Temperature'].append(T)

        df = pd.DataFrame(self.output_data)

        if save == True:
            df.to_csv('output.csv')
        else:
            return df


    def coolscheds(self, sched, T0, iteration, params):
        """
        Calculates p according to cooling schedule

        Returns
            p   (float)             probability
        """

        if sched == 1:
            T = coolsched1(T0, iteration)

        elif sched == 2:
            T = coolsched2(T0, iteration)

        return T
        # elif sched == 3:
        #     T = self.coolsched3(T0, iteration, params)

    def sampling_method(self, method):

        if method == 1:
            new_nodes, new_edges, new_distance = self.Map._1SwapNode_()
        elif method == 2:
            new_nodes, new_edges, new_distance = self.Map._SwapNodes_()
        elif method == 3:
            new_nodes, new_edges, new_distance = self.Map._BreakChainNodes_()
        elif method == 4:
            new_nodes, new_edges, new_distance = self.Map._InverseNodes_()
        elif method == 5:
            new_nodes, new_edges, new_distance = self.Map._Hybrid_()

        return new_nodes, new_edges, new_distance
