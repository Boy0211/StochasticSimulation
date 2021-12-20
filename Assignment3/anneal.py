import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
import random

class SimAnneal:
    """
    Class object to perform simulated annealing
    """

    def __init__(self, map, T0, Nmax, sched, params, chain_length):
        """
        Initialization of the SimAnneal class.

        Args:

        map:    (map-object)       map of map object
        T0:     (float)            The T0
        Nmax:   (integer)          Maximal number of cycles
        sched:  (integer)          the cooling schedule to use
        B:      (float)            B parameter for cooling scheds
        """

        self.map = map
        self.T0 = T0
        self.Nmax = Nmax
        self.N = 0
        self.sched = sched
        self.params = params
        self.distances = []
        self.temps = []
        self.T = T0
        self.chain_length = chain_length

    def coolsched1(self):
        """
        Caluclates temperature according to a cooling schedule

        Returns
            T   (float)             Temperature
        """

        if self.N == 0:
            T = self.T0
        else:
            T = self.T0/(np.log(self.N + self.params[0]))

        self.temps.append(T)

        self.T = T
        return T


    def coolsched2(self):
        """
        Caluclates temperature according to a cooling schedule

        Returns
            T   (float)             Temperature
        """
        if self.N == 0:
            T = self.T0
        else:
            T = self.T0/self.N

        self.temps.append(T)

        return T


    def coolsched3(self):
        """
        Caluclates temperature according to a cooling schedule

        Returns
            T   (float)             Temperature
        """
        if self.N == 0:
            T = self.T0
        else:
            T = self.T0 * np.exp(-self.N *self.params[0])

        self.temps.append(T)

        return T

    def coolscheds(self,sched):
        """
        Calculates p according to cooling schedule

        Returns
            p   (float)             probability
        """

        if sched == 1:

            T = self.coolsched1()

        elif sched == 2:

            T = self.coolsched2()

        elif sched == 3:
            T = self.coolsched3()


        # if T == 0:
        #     p = 0
        # else:

        return T

    def annealing(self):
        """
        Performs simulated annealing

        Returns:

            self.distances (list)   list with all distances found over time
        """


        indices = np.arange(self.map.nodes.shape[0])
        np.random.shuffle(indices)

        # initialize randomly
        self.map.nodes = self.map.nodes[indices]
        self.map.coords = self.map.coords[indices]
        self.map.nodes_list = self.map.make_nodes_list(self.map.nodes)
        self.map.current_distance = self.map.calc_current_distance(self.map.nodes_list)
        self.map.lowest_distance = self.map.current_distance
        self.map.best_tour = self.map.nodes



        for N in range(self.Nmax):
            T = self.coolscheds(self.sched)

            for M in range(self.chain_length):
                # choose random indices
                inds_range_max = max(self.map.nodes)

                inds = random.sample(range(0, inds_range_max), 2)

                # calculate distance before swap
                distance_before = self.map.current_distance

                # do the swap
                self.map.swap_1node(inds)
                # self.map.swap(inds)


                # calculate the distance after the swap
                distance_after = self.map.current_distance



                p = np.exp(-(distance_after - distance_before)/T)

                # check if distance before is smaller than after

                if distance_after - distance_before > 0:
                    # print("inif")
                    # dont accept if:
                    if p < np.random.uniform():
                        # don't accept, swap back to old list
                        self.map.swap_1node([inds[1], inds[0]])
                        # self.map.swap(inds)

                if self.map.current_distance < self.map.lowest_distance:
                    self.map.lowest_distance = self.map.current_distance
                    self.map.best_tour = self.map.nodes.copy()


            #     else:
            #         print("accepted jeej", p, distance_after - distance_before)
            # else:
            #     print("accepted jeej", p, distance_after - distance_before)

            # print("distance_before", "distance_after", distance_before, distance_after, "current", self.map.current_distance)
            #     else:
            #         # print("accepted1", self.N, "N", p, "p")
            # else:
            #     # print("accepted2", self.N, "N", p, "p")

            # print(self.map.current_distance)
            self.distances.append(self.map.current_distance)
            self.N += 1
        # print(self.distances)

        return self.distances
