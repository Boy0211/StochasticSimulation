import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# name = "results/data_many_tuning.6313229"
name = "results/data_many_tuning2.113056"
infile = open(name, 'rb')
data_dict = pickle.load(infile)
# for keys in db:
#     print(keys, '=>', db[keys])
infile.close()


# print(data_dict["all_params"])

T0s = data_dict["all_params"]["T0s"]
chain_lengths =  data_dict["all_params"]["chain_lengths"]
scheds = data_dict["all_params"]["scheds"]
paramss = data_dict["all_params"]["paramss"]
Total_max = data_dict["all_params"]["Total_max"]


df_dict  = {"T0": [], "chain_length":[], "sched": [], "params": [], "fitnesses":[]}

chain_length = 10

for sched_i in range(len(scheds)):

    if len(paramss[sched_i]) > 1:
        fig, axs = plt.subplots(len(paramss[sched_i]))
        fig.suptitle('Tuning per schedule')


    sched = scheds[sched_i]

    params_counter = 0

    for params in paramss[sched_i]:

        params_key = str(params)

        for T0 in T0s:

            fitnesses = data_dict[T0][chain_length][sched][params_key]["fitnesses"]
            steps = list(range(len(fitnesses)))


            if len(paramss[sched_i]) > 1:
                axs[params_counter].plot(steps, fitnesses, label=f"T0={T0}")

            else:
                plt.plot(steps, fitnesses, label=f"T0={T0}")


        params_counter += 1
    plt.legend()
    plt.show()
