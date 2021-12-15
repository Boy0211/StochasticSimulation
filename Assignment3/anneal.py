import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
import random

class SimAnneal:
    """
    Class object to perform simulated annealing
    """

    def __init__(self, map, T0, Nmax, sched, B):
        """
        Initialization of the map class.

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
        self.B = B
        self.distances = []

    def coolsched1(self):
        """
        Caluclates temperature according to a cooling schedule

        Returns
            T   (float)             Temperature
        """

        T = self.T0/(np.log(self.N + self.B))

        return T


    def coolsched2(self):
        """
        Caluclates temperature according to a cooling schedule

        Returns
            T   (float)             Temperature
        """

        return T

    def coolscheds(self,sched, distance_before, distance_after):
        """
        Calculates p according to cooling schedule

        Returns
            p   (float)             probability
        """
        
        if sched == 1:

            T = self.coolsched1()

        if sched == 2:

            T = self.coolsched2()

        p = np.exp(-(distance_after - distance_before)/T)

        return p

    def annealing(self):
        """
        Performs simulated annealing

        Returns:

            self.distances (list)   list with all distances found
        """


        for N in range(self.Nmax):

            # choose random indices
            inds_range_max = max(self.map.nodes)

            inds = random.sample(range(0, inds_range_max), 2)

            # calculate distance before swap
            distance_before = self.map.current_distance

            # do the swap
            self.map.swap(inds)

            # calculate the distance after the swap
            distance_after = self.map.current_distance

            # check if distance before is smaller than after
            if distance_before < distance_after:
                p = self.coolscheds(self.sched, distance_before, distance_after)


                if p < random.random():
                    # don't accept, swap back to old list
                    self.map.swap(inds)

            self.distances.append(self.map.current_distance)
            self.N += 1

        return self.distances
