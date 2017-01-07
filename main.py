import time

from population import Population

start = time.time()
population_size = 200
agent_size = 20
number_of_generations = 50
elite_size = 5
padding = "=" * 26

#FOR STATS
best_fitness = []
worst_fitness = []
avg_fitness = []


def write_to_file(file_path, best):
    f = open(file_path, 'w+')
    f.write("".join(best.to_program()))
    f.flush()
    print("".join(best.to_program()))

def write_stats_to_file(file_path):
    f = open(file_path, 'w+')
    f.write("POP. SIZE\n"+str(population_size)+"\n")
    f.write("AGENT.SIZE\n"+str(agent_size)+"\n")
    f.write("GENERATIONS\n"+str(number_of_generations)+"\n")
    f.write("ELITE SIZE\n"+str(elite_size)+"\n")
    f.write("BEST FITNESS\n")
    for b in best_fitness:
        f.write(str(b)+"\n")
    f.write("WORST FITNESS\n")
    for w in worst_fitness:
        f.write(str(w)+"\n")
    f.write("AVERAGE FITNESS\n")
    for a in avg_fitness:
        f.write(str(a)+"\n")
    f.close()



if __name__ == "__main__":
    population = Population(population_size=population_size, agent_size=agent_size,
                            elite_size=elite_size)
    population.generate_agents()

    # FIXME: ==========REMOVE ==========
    # a = population.agents[0]
    # print("".join(a.to_program()))
    #
    # import pylab as plt
    # import mazes
    # from simulator import simulate
    #
    # plt.ion()
    # plt.clf()
    # plt.imshow(mazes.mazes_train[0][4], cmap=plt.cm.binary, interpolation='nearest')
    # plt.pause(0.01)
    #
    # simulate(mazes.mazes_train[0], a, verbose=False, graphics=True, delay=0.1, max_iter=10)
    # exit()

    for i in range(number_of_generations):

        delimiter = "".join((padding, (" GENERATION " + str(i) + " "), padding))
        print delimiter

        fitness = [a.compute_fitness() for a in population.agents]
        population_avg = sum(fitness) / len(fitness)
        for f in fitness:
            print("Agent fitness: " + str(f))
        population_best = sorted(fitness, reverse=False)[0]
        population_worst = sorted(fitness, reverse=True)[0]
        print("Best population fitness: " + str(population_best))
        print("Worst population fitness: " + str(population_worst))
        print("Average population fitness: " + str(population_avg))
        best_fitness.append(population_best)
        worst_fitness.append(population_worst)
        avg_fitness.append(population_avg)

        population.evolve(debug=False)
    delimiter = "".join((padding, (" FINISHED " + str(i) + " "), padding))

    print(delimiter)
    print("Execution time: " + str(time.time() - start))

    best = population.return_best(population.agents)
    print("==== BEST AGENT ====")

    file_path = './out/best_agent.txt'
    stats_path = './out/run_stats.txt'
    write_to_file(file_path, best)
    write_stats_to_file(stats_path)
    best.solve_mazes()
