import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt
import random
import tsplib95
import copy

class Map():
    """
    The map that holds all nodes and tours.
    """
    def __init__(self, name, coords, optimal_tour):
        """
        Initialization of the map class.

        Args:

        name:    (string)       the type of the map
        nodes:   (list)         the list of the nodes in order of the tour
        coords: (ndarray)       list with coordinate sets in the order of the tour
        optimal_tour: (ndarray) list of nodes in the order of the optimal tour
        """

        self.name = name
        self.coords = coords

        self.distance_matrix = self.create_distance_matrix()
        
        self.nodes = random.sample(list(self.coords.keys()), len(list(self.coords.keys())))
        self.edges = self.make_edges_of_tour(self.nodes)

        self.optimal_tour = optimal_tour

    def __repr__(self):

        fig, axis = plt.subplots(figsize=(14,10))
        axis.scatter(np.asarray(list(self.coords.values()))[:, 0], 
                     np.asarray(list(self.coords.values()))[:, 1], marker='s')
        axis.grid()
        x = []
        y = []
        for edge in self.edges:
            x.append(self.coords[edge[0]][0])
            y.append(self.coords[edge[0]][1])
        axis.plot(x, y, alpha=0.5)
        plt.show()
        print('Tour length: ', self.calculate_tour_length(self.edges))
        return 'No Error'

    def create_distance_matrix(self):

        distance_mat = distance_matrix(list(self.coords.values()), 
                                       list(self.coords.values()), p=2)
        return distance_mat

    def make_edges_of_tour(self, nodes):
        """
        Creates a list of edges

        Returns:
            nodes_list (ndarray)    list with edges
        """

        #loop through nodes list

        edges = [nodes, nodes[1:] + [nodes[0]]]
        nodes_list = np.asarray(edges).T

        return nodes_list

    def calculate_tour_length(self, edges):
        """
        Calculates the the distance of the current tour

        Returns:
            distance (float)    current distance of nodes in nodelist

        """

        # create indices to get the data from the distance matrix
        start_inds = edges[:,0] - 1
        end_inds = edges[:,1] - 1

        # obtain all distances
        distances = np.round(self.distance_matrix[start_inds, end_inds])

        # sum distances
        distance = distances.sum()

        return distance

    def _1SwapNode_(self):
        
        while True:
            inds = np.random.randint(0, len(self.nodes),size=2)
            if inds[0] != inds[1]:
                break
        ix1 = inds[0]
        ix2 = inds[1]

        new_nodes = copy.copy(self.nodes)
        selected_node = new_nodes[ix1]
        new_nodes.remove(selected_node)
        new_nodes.insert(ix2, selected_node)

        new_edges = self.make_edges_of_tour(new_nodes)
        new_distance = self.calculate_tour_length(new_edges)
        return new_nodes, new_edges, new_distance

    def _SwapNodes_(self):
        """
        Swaps two nodes and all values that are linked to these nodes

        Args:
            inds (tuple)    indices of two nodes that will be swapped
        """

        while True:
            inds = np.random.randint(0, len(self.nodes),size=2)
            if inds[0] != inds[1]:
                break
        ix1 = inds[0]
        ix2 = inds[1]

        new_nodes = copy.copy(self.nodes)
        new_nodes[ix1], new_nodes[ix2] = new_nodes[ix2], new_nodes[ix1]

        new_edges = self.make_edges_of_tour(new_nodes)
        new_distance = self.calculate_tour_length(new_edges)
        return new_nodes, new_edges, new_distance

    def _BreakChainNodes_(self):

        while True:
            inds = np.random.randint(0, len(self.nodes), size=2)
            if inds[0] != inds[1]:
                break
        ix1 = min(inds)
        ix2 = max(inds)

        new_nodes = copy.copy(self.nodes)
        a, b, c = new_nodes[:ix1], new_nodes[ix1:ix2], new_nodes[ix2:]

        _ = np.random.uniform()
        if _ < 0.34:
            new_nodes = a + c + b
        elif (_ >= 0.34) & (_ < 0.67):
            new_nodes = b + a + c
        elif _ >= 0.67:
            new_nodes = c + b + a

        new_edges = self.make_edges_of_tour(new_nodes)
        new_distance = self.calculate_tour_length(new_edges)
        return new_nodes, new_edges, new_distance

    # def _InverseNodes_(self):
        
    #     while True:
    #         inds = np.random.randint(0, len(self.nodes),size=2)
    #         if inds[0] != inds[1]:
    #             break
    #     ix1 = min(inds)
    #     ix2 = max(inds)
                    
    #     new_nodes = copy.copy(self.nodes)
    #     a, b, c = new_nodes[:ix1], new_nodes[ix1:ix2], new_nodes[ix2:]
    #     b.reverse()
    #     new_nodes = a + b + c


    #     new_edges = self.make_edges_of_tour(new_nodes)
    #     new_distance = self.calculate_tour_length(new_edges)
    #     return new_nodes, new_edges, new_distance

    def _Combined_(self):

        _ = np.random.uniform()
        if _ < 0.34:
            new_nodes, new_edges, new_distance = self._1SwapNode_()
        elif (_ >= 0.34) & (_ < 0.67):
            new_nodes, new_edges, new_distance = self._SwapNodes_()
        elif _ >= 0.67:
            new_nodes, new_edges, new_distance = self._BreakChainNodes_() 
        
        return new_nodes, new_edges, new_distance




