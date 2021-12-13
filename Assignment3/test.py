from python_tsp.heuristics import solve_tsp_simulated_annealing
import numpy as np

from python_tsp.distances import great_circle_distance_matrix
import pandas as pd

def get_data(type):
    df = pd.read_csv("data/a280.tsp.txt", skiprows=5, sep="\t")
    print(df)

    return data
sources = np.array([
    [ 40.73024833, -73.79440675],
    [ 41.47362495, -73.92783272],
    [ 41.26591   , -73.21026228],
    [ 41.3249908 , -73.507788  ]
])
distance_matrix = great_circle_distance_matrix(sources)

# distance_matrix = np.array([
#     [0,  5, 4, 10],
#     [5,  0, 8,  5],
#     [4,  8, 0,  3],
#     [10, 5, 3,  0]
# ])
permutation, distance = solve_tsp_simulated_annealing(distance_matrix)

print(permutation, distance)

types = ["a280", "eli51", "pcb442"]

data = get_data(types[0])
