from random import randint, uniform
from agent import Agent
from enum import Enum


class Mutation(Enum):
    RANDOM = 'random'
    SWAP = 'SWAP'


class Population:
    def __init__(self, population_size=10, agent_size=20, tournament_size=5,
                 mutation=Mutation.RANDOM, mutation_rate=0.015, elite_size=1):
        self.population_size = population_size
        self.agent_size = agent_size
        self.agents = None
        self.mutation_rate = mutation_rate
        self.mutation = mutation
        self.tournament_size = tournament_size
        self.elite_size = elite_size
        self.cmd_size = Agent.get_parser()

    def generate_agents(self):
        self.agents = [Agent.generate_random(self.agent_size) for _ in range(self.population_size)]

    def evolve(self):
        fitness = [a.compute_fitness() for a in self.agents]
        population_fitness = sum(fitness) / len(fitness)
        for f in fitness:
            print("Agent fitness: " + str(f))
        print("Population fitness: " + str(population_fitness))

        new_agents = []
        for _ in range(self.elite_size):
            best = self.return_best(self.agents)
            new_agents.append(best)
            self.agents.remove(best)
        for _ in range(self.elite_size, self.population_size):
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            child = self.cross_agents(parent1, parent2)
            new_agents.append(self.mutate(child))
        self.agents = new_agents

    # def cross_agents(self, parent_a, parent_b):
    #     child = Agent([0 for _ in range(self.agent_size)])
    #     start_pos = randint(0, self.agent_size - 1)
    #     end_pos = randint(0, self.agent_size - 1)
    #     for i in range(0, self.agent_size):
    #         if start_pos < end_pos and start_pos < i < end_pos:
    #             child.vector[i] = parent_a.vector[i]
    #         elif start_pos > end_pos:
    #             if not (start_pos > i > end_pos):
    #                 child.vector[i] = parent_a.vector[i]
    #     for i in range(0, self.agent_size):
    #         if not parent_b.vector[i] in child.vector:
    #             for ii in range(0, len(child.vector)):
    #                 if child.vector[ii] == 0:
    #                     child.vector[ii] = parent_b.vector[i]
    #                     break
    #     return child

    def cross_agents(self, parent_a, parent_b):
        parents = [parent_a, parent_b]
        return Agent([parents[randint(0, 1)].vector[i] for i in range(self.agent_size)])

    @staticmethod
    def return_best(candidates):
        return sorted(candidates, key=lambda x: x.fitness, reverse=False)[0]

    def mutate(self, agent):
        if self.mutation == Mutation.RANDOM:
            max_command = len(agent.get_parser())
            for i in range(0, len(agent.vector)):
                if uniform(0, 1) < self.mutation_rate:
                    agent.vector[i] = randint(0, max_command - 1)
            return agent
        elif self.mutation == Mutation.SWAP:
            for cursor in range(0, self.agent_size):
                if uniform(0, 1) < self.mutation_rate:
                    change_position = randint(0, self.agent_size - 1)
                    swap_a = agent.vector[cursor]
                    swap_b = agent.vector[change_position]
                    agent.vector[cursor] = swap_b
                    agent.vector[change_position] = swap_a
            return agent

    def tournament_selection(self):
        tournament = []
        for i in range(0, self.tournament_size):
            random_id = randint(0, self.agents - 1)
            tournament.append(self.agents[random_id])
        fittest = self.return_best(tournament)
        return fittest
