import time

from population import Population

start = time.time()

population_size = 10
number_of_generations = 10

population = Population(population_size=population_size)
population.generate_agents()

for i in range(number_of_generations):
    print("========================== GENERATION " + str(i) + " ==========================")

    fitness = [a.compute_fitness() for a in population.agents]
    population_fitness = sum(fitness) / len(fitness)
    for f in fitness:
        print("Agent fitness: " + str(f))
    print("Population fitness: " + str(population_fitness))

    population.evolve()
    break
print("========================== FINISHED ==========================")
print("Execution time: " + str(time.time() - start))
