import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt


name = "results/data_many_21_12_21_16_19_35"

infile = open(name, 'rb')
data_dict = pickle.load(infile)

infile.close()


# print(data_dict["all_params"])

T0s = data_dict["all_params"]["T0s"]
chain_lengths =  data_dict["all_params"]["chain_lengths"]
scheds = data_dict["all_params"]["scheds"]
methods = data_dict["all_params"]["methods"]
# paramss = data_dict["all_params"]["paramss"]
# Total_max = data_dict["all_params"]["Total_max"]

# df_dict  = {"T0": [], "chain_length":[], "sched": [], "params": [], "fitnesses":[]}

chain_length = 200

for sched_i in range(len(scheds)):
    sched = scheds[sched_i]
    fig, axs = plt.subplots(len(methods))
    fig.suptitle(f'Tuning per schedule, sched={sched}')



    for method in methods:

        for T0 in T0s:
            try:
                fitnesses = data_dict[T0][chain_length][sched][method]["fitnesses"]
                steps = list(range(len(fitnesses)))

                axs[method-1].plot(steps, fitnesses, label=f"T0={T0}")
            except:
                continue

            # # else:
            # plt.plot(steps, fitnesses, label=f"T0={T0}")


            # params_counter += 1
    plt.legend()
    plt.show()
