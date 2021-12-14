import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


class Map:
    def __init__(self, name, nodes, coords, optimal_tour,  opt_tour_dist):
        self.name = name
        self.nodes = nodes
        self.nodes_list = self.nodes_list()
        self.coords = coords
        self.coords_tups = self.coords_tups()
        self.distance_matrix = self.create_distance_matrix()
        self.current_distance = self.current_distance()
        self.optimal_tour = optimal_tour
        self.optimal_tour_coords = self.coords[self.optimal_tour - 1]
        self.opt_tour_dist = opt_tour_dist


    def create_distance_matrix(self):

        distance_mat = distance_matrix(self.coords, self.coords, p=2)

        return distance_mat


    def coords_tups(self):
        lst = self.coords
        coords_tups = [tuple(x) for x in lst]
        return coords_tups

    def nodes_list(self):

        nodes_list = []
        for i in range(len(self.nodes)):
            if i + 1 < len(self.nodes):
                a = i +1
            else:
                a = 0

            ls = [self.nodes[i], self.nodes[a]]

            nodes_list.append(ls)
        nodes_list = np.array(nodes_list)
        return nodes_list


    def current_distance(self):
        start_inds = self.nodes_list[:,0] - 1
        end_inds = self.nodes_list[:,1] - 1


        distances = np.round(self.distance_matrix[start_inds, end_inds])

        distance = distances.sum()


        return distance



    def swap(self, inds):
        ix1 = inds[0]
        ix2 = inds[1]


        self.nodes[ix1], self.nodes[ix2] =  self.nodes[ix2],  self.nodes[ix1]
        self.coords[[ix1, ix2]] = self.coords[[ix2, ix1]]
        self.coords_tups[ix1], self.coords_tups[ix2] =  self.coords_tups[ix2],  self.coords_tups[ix1]

        # swap within tuples
        # create cupholders
        vara = self.nodes_list[ix1][0]
        varb = self.nodes_list[ix2][0]

        # swap
        self.nodes_list[ix1][0] = varb
        self.nodes_list[ix1-1][1] = varb
        self.nodes_list[ix2][0] = vara
        self.nodes_list[ix2-1][1] = vara


    #
    #         def opt_tour_dist(self):
    #
    #             nodes_list = []
    #             for i in range(len(self.optimal_tour)):
    #                 if i + 1 < len(self.optimal_tour):
    #                     a = i +1
    #                 else:
    #                     a = 0
    #
    #                 ls = [self.optimal_tour[i], self.optimal_tour[a]]
    #
    #                 nodes_list.append(ls)
    #
    #             nodes_list = np.array(nodes_list)
    #
    #             start_inds = nodes_list[:,0] - 1
    #             end_inds = nodes_list[:,1] - 1
    #
    #             distances = np.round(self.distance_matrix[start_inds, end_inds])
    #             print(distances)
    #             distance = distances.sum()
    #
    #             print("optimal tour distance", distance)
    #
    #             return distance
