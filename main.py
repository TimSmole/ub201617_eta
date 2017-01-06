import time

from population import Population

start = time.time()
population_size = 200
agent_size = 20
number_of_generations = 10
elite_size = 5
padding = "=" * 26


def write_to_file(file_path, best):
    f = open(file_path, 'w+')
    f.write("".join(best.to_program()))
    f.flush()
    print("".join(best.to_program()))


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
        population_fitness = sum(fitness) / len(fitness)
        for f in fitness:
            print("Agent fitness: " + str(f))
        print("Population fitness: " + str(population_fitness))

        population.evolve()
    delimiter = "".join((padding, (" FINISHED " + str(i) + " "), padding))

    print(delimiter)
    print("Execution time: " + str(time.time() - start))

    best = population.return_best(population.agents)
    print("==== BEST AGENT ====")

    file_path = './out/best_agent.txt'
    write_to_file(file_path, best)
    best.solve_mazes()
