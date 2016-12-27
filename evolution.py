from population import Population

population = Population()
population.generate_agents()

for a in population.agents:
    fitness = a.compute_fitness()
    print("Agent fitness: " + str(fitness))
