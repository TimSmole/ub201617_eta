import time

import mazes
from population import Population
from simulator import simulate

start = time.time()

population_size = 10
number_of_generations = 10

population = Population(population_size=population_size)
population.generate_agents()

a = population.agents[0]
print("".join(a.to_program()))


# FIXME: ==========REMOVE ==========
import pylab as plt
plt.ion()
plt.clf()
print(mazes.mazes_train[0])
plt.imshow(mazes.mazes_train[0][4], cmap=plt.cm.binary, interpolation='nearest')
plt.pause(0.01)

simulate(mazes.mazes_train[0], a, verbose=False, graphics=True, delay=0.1, max_iter=10)
exit()


for i in range(number_of_generations):
    print("========================== GENERATION " + str(i) + " ==========================")

    fitness = [a.compute_fitness() for a in population.agents]
    population_fitness = sum(fitness) / len(fitness)
    for f in fitness:
        print("Agent fitness: " + str(f))
    print("Population fitness: " + str(population_fitness))

    population.evolve()

print("========================== FINISHED ==========================")
print("Execution time: " + str(time.time() - start))

best = population.return_best(population.agents)
best.solve_mazes()
