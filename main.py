import os
import time

from agent import Agent
from population import Population

population_size = 200
agent_size = 25
number_of_generations = 40
elite_size = 5


def save_agent(agent):
    filename = './out/agent_' + str(population_size) + '_' + \
               str(agent_size) + '-' + str(number_of_generations) + '-' + \
               str(elite_size) + '-' + str(agent.fitness) + '.txt'
    f = open(filename, 'w+')
    f.write("".join(agent.to_program()))
    f.flush()
    print("".join(agent.to_program()))


def read_agent(filename):
    return Agent.generate_from_file_or_string("./out/" + filename)


def read_best_agent():
    fitness = []
    for f in os.listdir("./out/"):
        if os.path.isfile(os.path.join("./out/", f)) and 'agent_' in f:
            fitness.append(float(f.split("_")[-1].split(".txt")[0]))
    best_fitness = sorted(fitness)[0]
    return read_agent([f for f in os.listdir("./out/") if str(best_fitness) in f][0])


def solve_with_best():
    agent = read_best_agent()
    agent.solve_mazes()


if __name__ == "__main__":
    start = time.time()

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

    padding = "=" * 26
    for i in range(number_of_generations):
        print "".join((padding, (" GENERATION " + str(i) + " "), padding))
        population.evolve()

    print("".join((padding, (" FINISHED " + str(i) + " "), padding)))
    print("Execution time: " + str(time.time() - start))

    [a.compute_fitness() for a in population.agents]
    best = population.return_best(population.agents)
    print("==== BEST AGENT ====")

    save_agent(best)
    best.solve_mazes()
