import matplotlib.pyplot as plt
import numpy as np
import time
def parse_file(file_name):
    print "Reading file "+file_name
    avg_fit=[]
    best_fit=[]
    worst_fit=[]
    #TODO Parse file
    with open(file_name) as f:
        data = f.readlines()
    generations = int(data[2].replace("\n", "").split(" ")[1])
    print generations
    best_offset = 8
    worst_offset = best_offset+generations+3
    avg_offset = worst_offset+generations+3
    for i in range(0, generations):
        best_fit.append(float(data[i+best_offset].replace("\n", "")))
        worst_fit.append(float(data[i+worst_offset].replace("\n", "")))
        avg_fit.append(float(data[i+avg_offset].replace("\n", "")))
    return (avg_fit, best_fit, worst_fit)

def draw_graph_pair(captionA, captionB, dataA, dataB):
    xA = np.arange(len(dataA))
    xB = np.arange(len(dataB))
    plt.plot(xA, dataA)
    plt.plot(xB, dataB)
    plt.legend([captionA, captionB])
    plt.show()

def draw_graph_multi(captions, data, outputFile=""):
    fig = plt.figure()
    if len(data) != len(captions):
        print "Data and caption size does not match!"
        pass
    for dat in data:
        x = np.arange(len(dat))
        plt.plot(x, dat)
    plt.xlabel("Number of generations")
    plt.ylabel("Fitness score")
    plt.legend(captions)
    plt.show()
    if outputFile == "":
        outputFile = str(time.time())+".png"
    fig.savefig('graphs/'+outputFile)


#You have to specify file names manually"
file_evolve = "out/run_stats_50_30_20_5_1483890390.25.txt"
file_non_evolve = "out/run_stats_50_30_20_5_1483891776.92.txt"

(avg_fit_ev, best_fit_ev, worst_fit_ev) = parse_file(file_evolve)
(avg_fit_nev, best_fit_nev, worst_fit_nev) = parse_file(file_non_evolve)
print len(avg_fit_ev), len(best_fit_ev), len(worst_fit_ev)
#AVG. FITNESS
draw_graph_multi(["Avg. evolve", "Avg. random"], [avg_fit_ev, avg_fit_nev], "avg_compare.png")
#BEST. FITNESS
draw_graph_multi(["Best evolve", "Best random"], [best_fit_ev, best_fit_nev], "best_compare.png")
#WORST. FITNESS
draw_graph_multi(["Worst evolve", "Worst random"], [worst_fit_ev, worst_fit_nev], "worst_compare.png")
#MULTIPLE GRAPHS
draw_graph_multi(["Avg. evolve", "Avg. random", "Best evolve", "Best random"], [avg_fit_ev, avg_fit_nev, best_fit_ev, best_fit_nev], "multi_compare.png")