import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


Fitnesses = [[0,1,2,3,4], [10,20,30,40,50]]

paramss = [[[1], [2]]]
scheds = [1]
T0s = [10]



for sched_i in range(len(scheds)):
    sched  = scheds[sched_i]
    fig, axs = plt.subplots(len(paramss[sched_i]))
    fig.suptitle('Tuning per schedule')

    params_counter = 0
    for param in paramss[sched_i]:

        for T0 in T0s:

            fitnesses  = Fitnesses[params_counter]
            steps = list(range(len(fitnesses)))
            axs[params_counter].plot(steps, fitnesses)

        params_counter +=1
    plt.show()
