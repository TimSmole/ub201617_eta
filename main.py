import os
import time

from agent import Agent
from population import Population

population_size = 25
agent_size = 30
number_of_generations = 10
elite_size = 5

# FOR STATS
best_fitness = []
worst_fitness = []
avg_fitness = []


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


def write_stats_to_file(file_path):
    f = open(file_path, 'w+')
    f.write("POP. SIZE\n" + str(population_size) + "\n")
    f.write("AGENT.SIZE\n" + str(agent_size) + "\n")
    f.write("GENERATIONS\n" + str(number_of_generations) + "\n")
    f.write("ELITE SIZE\n" + str(elite_size) + "\n")
    f.write("BEST FITNESS\n")
    for b in best_fitness:
        f.write(str(b) + "\n")
    f.write("WORST FITNESS\n")
    for w in worst_fitness:
        f.write(str(w) + "\n")
    f.write("AVERAGE FITNESS\n")
    for a in avg_fitness:
        f.write(str(a) + "\n")
    f.close()


if __name__ == "__main__":
    start = time.time()

    population = Population(population_size=population_size, agent_size=agent_size,
                            elite_size=elite_size)
    population.generate_agents()

    padding = "=" * 26
    for i in range(number_of_generations):
        print "".join((padding, (" GENERATION " + str(i) + " "), padding))
        fitness = [a.async_compute_fitness() for a in population.agents]
        population_avg = sum(fitness) / len(fitness)
        for f in fitness:
            print("Agent fitness: " + str(f))
        agents_sorted = sorted(fitness)
        population_best = agents_sorted[0]
        population_worst = agents_sorted[len(agents_sorted) - 1]
        print("Best population fitness: " + str(population_best))
        print("Worst population fitness: " + str(population_worst))
        print("Average population fitness: " + str(population_avg))
        best_fitness.append(population_best)
        worst_fitness.append(population_worst)
        avg_fitness.append(population_avg)
        population.evolve(debug=False)

    print("".join((padding, (" FINISHED " + str(i) + " "), padding)))
    print("Execution time: " + str(time.time() - start))

    [a.async_compute_fitness() for a in population.agents]
    best = population.return_best(population.agents)
    print("==== BEST AGENT ====")

    file_path = './out/best_agent.txt'
    stats_path = './out/run_stats.txt'
    write_stats_to_file(stats_path)
    save_agent(best)
    best.solve_mazes()
