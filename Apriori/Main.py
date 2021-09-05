from frequent_itemset_miner import *
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

if __name__ == "__main__":
    accident = "accidents.dat"
    toy = "toy.dat"
    chess = "chess.dat"
    connect = "connect.dat"
    mushroom = "mushroom.dat"
    pumsb = "pumsb.dat"
    pumsb_star = "pumsb_star.dat"
    retail = "retail.dat"
    #################################
    dataset = Dataset(chess)
    print("Number of transactions:", dataset.trans_num())
    print("Number of different items:", dataset.items_num())
    ############################################
    #       Execution of both algorithms       #
    ############################################

    times = []
    times2 = []
    x_scale = [0.95, 0.96, 0.97, 0.98, 0.99]
    for i in tqdm(x_scale):
        start_time = time.time()
        apriori(connect, i)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        start_time2 = time.time()
        alternative_miner(connect, i)
        elapsed_time2 = time.time() - start_time2
        times2.append(elapsed_time2)
    print(times)
    print(times2)

    #################################
    #       Graphics of time        #
    #################################
    # times_chess = [791.7056040763855, 283.1978702545166, 90.43126797676086, 28.0169734954834, 6.907203197479248, 0.6592669486999512]
    # times2_chess = [53.88921070098877, 20.42059350013733, 7.643372058868408, 2.502119541168213, 0.4828453063964844, 0.0904545783996582]
    # x_scale = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    plt.plot(x_scale, times, color="black", label="Apriori")
    plt.plot(x_scale, times2, color="red", label="ECLAT")
    plt.title("Time of execution on Mushroom dataset")
    plt.xlabel("Minimum Frequency")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()
